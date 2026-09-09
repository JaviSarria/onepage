"""Motores y sesiones de las dos bases de datos SQLite."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import EVOLUTIVOS_DB_URL, INCIDENCIAS_DB_URL


class EvolutivosBase(DeclarativeBase):
    """Base declarativa de la base de datos de evolutivos."""


class IncidenciasBase(DeclarativeBase):
    """Base declarativa de la base de datos de incidencias."""


evolutivos_engine = create_engine(
    EVOLUTIVOS_DB_URL, connect_args={"check_same_thread": False}
)
incidencias_engine = create_engine(
    INCIDENCIAS_DB_URL, connect_args={"check_same_thread": False}
)


@event.listens_for(evolutivos_engine, "connect")
@event.listens_for(incidencias_engine, "connect")
def _enable_foreign_keys(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


EvolutivosSession = sessionmaker(bind=evolutivos_engine, autoflush=False, expire_on_commit=False)
IncidenciasSession = sessionmaker(bind=incidencias_engine, autoflush=False, expire_on_commit=False)


def get_evolutivos_db() -> Iterator[Session]:
    db = EvolutivosSession()
    try:
        yield db
    finally:
        db.close()


def get_incidencias_db() -> Iterator[Session]:
    db = IncidenciasSession()
    try:
        yield db
    finally:
        db.close()


def init_databases() -> None:
    """Crea el esquema de ambas bases de datos si no existe."""
    from . import models  # noqa: F401  (registra los modelos en las bases declarativas)

    EvolutivosBase.metadata.create_all(bind=evolutivos_engine)
    IncidenciasBase.metadata.create_all(bind=incidencias_engine)
    _migrate_existing_databases()


def _migrate_existing_databases() -> None:
    """Añade columnas nuevas a instalaciones SQLite creadas por versiones anteriores."""
    migrations = (
        (evolutivos_engine, "evolutivos", "investigacion_previa"),
        (incidencias_engine, "incidencias", "investigacion_previa"),
    )
    for engine, table, column in migrations:
        if column not in {item["name"] for item in inspect(engine).get_columns(table)}:
            with engine.begin() as connection:
                connection.execute(
                    text(f'ALTER TABLE "{table}" ADD COLUMN "{column}" TEXT NOT NULL DEFAULT \'\'')
                )

    for engine in (evolutivos_engine, incidencias_engine):
        columns = {item["name"] for item in inspect(engine).get_columns("tareas_seguimiento")}
        tenia_nombre = "nombre" in columns
        missing = {
            "nombre": 'VARCHAR(255) NOT NULL DEFAULT \'\'',
            "descripcion": 'TEXT NOT NULL DEFAULT \'\'',
            "completada": "BOOLEAN NOT NULL DEFAULT 0",
        }
        with engine.begin() as connection:
            for column, definition in missing.items():
                if column not in columns:
                    connection.execute(
                        text(f'ALTER TABLE "tareas_seguimiento" ADD COLUMN "{column}" {definition}')
                    )
            if "tarea_codigo" in columns and not tenia_nombre:
                connection.execute(
                    text(
                        'UPDATE "tareas_seguimiento" SET "nombre" = "tarea_codigo" '
                        'WHERE "nombre" = \'\''
                    )
                )
            elif "tarea_codigo" in columns and tenia_nombre:
                connection.execute(
                    text(
                        'UPDATE "tareas_seguimiento" SET "nombre" = "tarea_codigo" '
                        'WHERE "nombre" = \'\' AND "tarea_codigo" <> \'\''
                    )
                )

    for engine in (evolutivos_engine, incidencias_engine):
        columns = {item["name"] for item in inspect(engine).get_columns("tareas_desarrolladas")}
        if {"codigo", "causa_raiz", "actividades"}.issubset(columns):
            parent = "evolutivo_id" if engine is evolutivos_engine else "incidencia_id"
            with engine.begin() as connection:
                connection.execute(text("PRAGMA foreign_keys=OFF"))
                connection.execute(
                    text(
                        f'''CREATE TABLE "tareas_desarrolladas_new" (
                            "{parent}" INTEGER NOT NULL,
                            "id" INTEGER NOT NULL PRIMARY KEY,
                            "tarea_id" INTEGER,
                            "estado" VARCHAR(32) NOT NULL DEFAULT 'Pendiente',
                            "orden" INTEGER NOT NULL DEFAULT 0,
                            FOREIGN KEY("{parent}") REFERENCES "{'evolutivos' if parent == 'evolutivo_id' else 'incidencias'}"("id") ON DELETE CASCADE,
                            FOREIGN KEY("tarea_id") REFERENCES "tareas"("id") ON DELETE CASCADE
                        )'''
                    )
                )
                connection.execute(
                    text(
                        f'''INSERT INTO "tareas_desarrolladas_new" ("{parent}", "id", "tarea_id", "estado", "orden")
                        SELECT old."{parent}", old."id",
                            (SELECT tarea.id FROM "tareas" AS tarea
                             WHERE tarea."{parent}" = old."{parent}" AND tarea."codigo" = old."codigo" LIMIT 1),
                            old."estado", old."orden"
                        FROM "tareas_desarrolladas" AS old'''
                    )
                )
                connection.execute(text('DROP TABLE "tareas_desarrolladas"'))
                connection.execute(
                    text('ALTER TABLE "tareas_desarrolladas_new" RENAME TO "tareas_desarrolladas"')
                )
                connection.execute(text("PRAGMA foreign_keys=ON"))

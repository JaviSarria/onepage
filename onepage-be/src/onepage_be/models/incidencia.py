"""Modelo de datos de la base de datos de incidencias."""

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import IncidenciasBase as Base
from .mixins import (
    AccionReunionMixin,
    ActividadMixin,
    ActividadDesarrolloMixin,
    BaseDatosAfectadaMixin,
    BloquesComunesMixin,
    CabeceraMixin,
    CambioMixin,
    CasoPruebaMixin,
    CriterioMixin,
    DespliegueMixin,
    DodMixin,
    EjecucionMixin,
    OrdenMixin,
    PkMixin,
    PlanificacionMixin,
    ProyectoMixin,
    RecursoMixin,
    RepositorioMixin,
    ReunionMixin,
    SeguimientoMixin,
    TareaMixin,
    TareaDesarrolloMixin,
    TimestampMixin,
    TrazabilidadMixin,
)

_INC_FK = "incidencias.id"


def _inc_fk() -> Mapped[int]:
    return mapped_column(ForeignKey(_INC_FK, ondelete="CASCADE"), nullable=False, index=True)


class Proyecto(ProyectoMixin, TimestampMixin, Base):
    __tablename__ = "proyectos"

    incidencias: Mapped[list["Incidencia"]] = relationship(
        back_populates="proyecto", cascade="all, delete-orphan"
    )


class Incidencia(PkMixin, CabeceraMixin, BloquesComunesMixin, OrdenMixin, TimestampMixin, Base):
    __tablename__ = "incidencias"

    proyecto_id: Mapped[str] = mapped_column(
        ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    severidad: Mapped[str] = mapped_column(String(32), default="Media", nullable=False)
    version_afectada: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    entorno_deteccion: Mapped[str] = mapped_column(String(32), default="PROD", nullable=False)
    fecha_deteccion: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    incidencia_jira: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    descripcion_problema: Mapped[str] = mapped_column(Text, default="", nullable=False)
    impacto: Mapped[str] = mapped_column(Text, default="", nullable=False)
    pasos_reproducir: Mapped[str] = mapped_column(Text, default="", nullable=False)
    comportamiento_actual: Mapped[str] = mapped_column(Text, default="", nullable=False)
    comportamiento_esperado: Mapped[str] = mapped_column(Text, default="", nullable=False)
    alcance_correccion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    evidencias_iniciales: Mapped[str] = mapped_column(Text, default="", nullable=False)
    causa_raiz: Mapped[str] = mapped_column(Text, default="", nullable=False)
    verificacion_no_regresion: Mapped[str] = mapped_column(Text, default="", nullable=False)

    proyecto: Mapped[Proyecto] = relationship(back_populates="incidencias")


class CriterioAceptacion(PkMixin, CriterioMixin, OrdenMixin, Base):
    __tablename__ = "criterios_aceptacion"

    incidencia_id: Mapped[int] = _inc_fk()


class Repositorio(PkMixin, RepositorioMixin, OrdenMixin, Base):
    __tablename__ = "repositorios"

    incidencia_id: Mapped[int] = _inc_fk()


class Tarea(PkMixin, TareaMixin, OrdenMixin, Base):
    __tablename__ = "tareas"

    incidencia_id: Mapped[int] = _inc_fk()
    criterio_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class TareaDesarrollada(PkMixin, TareaDesarrolloMixin, OrdenMixin, Base):
    __tablename__ = "tareas_desarrolladas"

    incidencia_id: Mapped[int] = _inc_fk()
    tarea_id: Mapped[int] = mapped_column(
        ForeignKey("tareas.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )


class ActividadDesarrollo(PkMixin, ActividadDesarrolloMixin, OrdenMixin, Base):
    __tablename__ = "actividades_desarrollo"

    tarea_desarrollo_id: Mapped[int] = mapped_column(
        ForeignKey("tareas_desarrolladas.id", ondelete="CASCADE"), nullable=False, index=True
    )


class CambioDesarrollo(PkMixin, CambioMixin, OrdenMixin, Base):
    __tablename__ = "cambios_desarrollo"

    tarea_desarrollo_id: Mapped[int] = mapped_column(
        ForeignKey("tareas_desarrolladas.id", ondelete="CASCADE"), nullable=False, index=True
    )


class RecursoTarea(PkMixin, RecursoMixin, OrdenMixin, Base):
    __tablename__ = "recursos_tarea"

    tarea_id: Mapped[int] = mapped_column(
        ForeignKey("tareas.id", ondelete="CASCADE"), nullable=False, index=True
    )


class ActividadTarea(PkMixin, ActividadMixin, OrdenMixin, Base):
    __tablename__ = "actividades_tarea"

    tarea_id: Mapped[int] = mapped_column(
        ForeignKey("tareas.id", ondelete="CASCADE"), nullable=False, index=True
    )


class Cambio(PkMixin, CambioMixin, OrdenMixin, Base):
    __tablename__ = "cambios"

    tarea_id: Mapped[int] = mapped_column(
        ForeignKey("tareas.id", ondelete="CASCADE"), nullable=False, index=True
    )


class CasoPrueba(PkMixin, CasoPruebaMixin, OrdenMixin, Base):
    __tablename__ = "casos_prueba"

    incidencia_id: Mapped[int] = _inc_fk()
    datos_usados: Mapped[str] = mapped_column(Text, default="", nullable=False)
    pasos_dados: Mapped[str] = mapped_column(Text, default="", nullable=False)


class EjecucionPrueba(PkMixin, EjecucionMixin, OrdenMixin, Base):
    __tablename__ = "ejecuciones_prueba"

    caso_id: Mapped[int] = mapped_column(
        ForeignKey("casos_prueba.id", ondelete="CASCADE"), nullable=False, index=True
    )


class DefinitionOfDone(PkMixin, DodMixin, OrdenMixin, Base):
    __tablename__ = "definition_of_done"

    incidencia_id: Mapped[int] = _inc_fk()


class Despliegue(PkMixin, DespliegueMixin, OrdenMixin, Base):
    __tablename__ = "despliegues"

    incidencia_id: Mapped[int] = _inc_fk()


class BaseDatosAfectada(PkMixin, BaseDatosAfectadaMixin, OrdenMixin, Base):
    __tablename__ = "bases_datos_afectadas"

    incidencia_id: Mapped[int] = _inc_fk()


class Reunion(PkMixin, ReunionMixin, OrdenMixin, Base):
    __tablename__ = "reuniones"

    incidencia_id: Mapped[int] = _inc_fk()


class AccionReunion(PkMixin, AccionReunionMixin, OrdenMixin, Base):
    __tablename__ = "acciones_reunion"

    reunion_id: Mapped[int] = mapped_column(
        ForeignKey("reuniones.id", ondelete="CASCADE"), nullable=False, index=True
    )


class Planificacion(PkMixin, PlanificacionMixin, OrdenMixin, Base):
    __tablename__ = "planificacion"

    incidencia_id: Mapped[int] = _inc_fk()


class Trazabilidad(PkMixin, TrazabilidadMixin, OrdenMixin, Base):
    __tablename__ = "trazabilidad"

    incidencia_id: Mapped[int] = _inc_fk()


class Seguimiento(PkMixin, SeguimientoMixin, OrdenMixin, Base):
    __tablename__ = "seguimientos"

    incidencia_id: Mapped[int] = _inc_fk()


class TareaSeguimiento(PkMixin, OrdenMixin, Base):
    __tablename__ = "tareas_seguimiento"

    seguimiento_id: Mapped[int] = mapped_column(
        ForeignKey("seguimientos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tarea_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    tarea_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    nombre: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    completada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ActividadSeguimiento(PkMixin, ActividadMixin, OrdenMixin, Base):
    __tablename__ = "actividades_seguimiento"

    tarea_seguimiento_id: Mapped[int] = mapped_column(
        ForeignKey("tareas_seguimiento.id", ondelete="CASCADE"), nullable=False, index=True
    )

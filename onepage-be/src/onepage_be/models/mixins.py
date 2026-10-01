"""Mixins de columnas comunes a las dos bases de datos."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PkMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class OrdenMixin:
    orden: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=_utcnow, onupdate=_utcnow, nullable=False
    )


class CabeceraMixin:
    """Campos de la tabla de cabecera comun a evolutivos e incidencias."""

    codigo: Mapped[str] = mapped_column(String(64), default="", nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    estado: Mapped[str] = mapped_column(String(64), default="Borrador", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    prioridad: Mapped[str] = mapped_column(String(32), default="Media", nullable=False)
    version: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    fecha_objetivo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    commits: Mapped[str] = mapped_column(Text, default="", nullable=False)
    despliegues: Mapped[str] = mapped_column(Text, default="", nullable=False)
    incidencias: Mapped[str] = mapped_column(Text, default="", nullable=False)


class BloquesComunesMixin:
    """Bloques narrativos presentes en ambas plantillas."""

    resumen: Mapped[str] = mapped_column(Text, default="", nullable=False)
    investigacion_previa: Mapped[str] = mapped_column(Text, default="", nullable=False)
    fuera_alcance: Mapped[str] = mapped_column(Text, default="", nullable=False)
    supuestos_restricciones: Mapped[str] = mapped_column(Text, default="", nullable=False)
    dependencias: Mapped[str] = mapped_column(Text, default="", nullable=False)
    riesgos_mitigacion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    decisiones_pendientes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    descripcion_solucion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    datos_pruebas: Mapped[str] = mapped_column(Text, default="", nullable=False)
    modulos_afectados: Mapped[str] = mapped_column(Text, default="", nullable=False)
    migracion_datos: Mapped[str] = mapped_column(Text, default="", nullable=False)


class CriterioMixin:
    codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    criterio: Mapped[str] = mapped_column(Text, default="", nullable=False)


class RepositorioMixin:
    nombre: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    subaccount: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    space: Mapped[str] = mapped_column(String(128), default="", nullable=False)


class TareaMixin:
    codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    dependencias: Mapped[str] = mapped_column(Text, default="", nullable=False)
    diseno: Mapped[str] = mapped_column(Text, default="", nullable=False)
    problemas: Mapped[str] = mapped_column(Text, default="", nullable=False)
    estado: Mapped[str] = mapped_column(String(32), default="Pendiente", nullable=False)


class TareaDesarrolloMixin:
    estado: Mapped[str] = mapped_column(String(32), default="Pendiente", nullable=False)


class ActividadDesarrolloMixin:
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    completada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_realizacion: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class RecursoMixin:
    tipo: Mapped[str] = mapped_column(String(32), default="servicio", nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    detalle: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ActividadMixin:
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    completada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class CambioMixin:
    nombre: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    repositorio: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    rama: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    commit: Mapped[str] = mapped_column(String(128), default="", nullable=False)


class CasoPlanMixin:
    codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    criterio_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    precondiciones: Mapped[str] = mapped_column(Text, default="", nullable=False)
    pasos: Mapped[str] = mapped_column(Text, default="", nullable=False)
    resultado_esperado: Mapped[str] = mapped_column(Text, default="", nullable=False)


class CasoPruebaMixin:
    datos: Mapped[str] = mapped_column(Text, default="", nullable=False)
    estado: Mapped[str] = mapped_column(String(32), default="NO EJECUTADA", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    incidencias: Mapped[str] = mapped_column(Text, default="", nullable=False)
    es_regresion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class EjecucionMixin:
    fecha: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    version: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    entorno: Mapped[str] = mapped_column(String(32), default="DEV", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    resultado: Mapped[str] = mapped_column(String(32), default="NO EJECUTADA", nullable=False)
    incidencia: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    evidencias: Mapped[str] = mapped_column(Text, default="", nullable=False)


class DodMixin:
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    completado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class DespliegueMixin:
    version: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    entorno: Mapped[str] = mapped_column(String(32), default="DEV", nullable=False)
    fecha_hora: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    commits: Mapped[str] = mapped_column(Text, default="", nullable=False)
    url_pipeline: Mapped[str] = mapped_column(String(512), default="", nullable=False)
    validacion_post: Mapped[str] = mapped_column(Text, default="", nullable=False)
    resultado: Mapped[str] = mapped_column(Text, default="", nullable=False)
    plan_reversion: Mapped[str] = mapped_column(Text, default="", nullable=False)


class BaseDatosAfectadaMixin:
    repositorio: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    nombre: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    tabla: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    campos: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ReunionMixin:
    fecha: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    participantes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    objetivo: Mapped[str] = mapped_column(Text, default="", nullable=False)
    decisiones: Mapped[str] = mapped_column(Text, default="", nullable=False)
    notas: Mapped[str] = mapped_column(Text, default="", nullable=False)


class AccionReunionMixin:
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    fecha_objetivo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class PlanificacionMixin:
    criterio_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    tarea_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    estado: Mapped[str] = mapped_column(String(32), default="Pendiente", nullable=False)
    estimado: Mapped[float] = mapped_column(default=0.0, nullable=False)
    real: Mapped[float] = mapped_column(default=0.0, nullable=False)
    inicio: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    fin: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    bloqueos: Mapped[str] = mapped_column(Text, default="", nullable=False)


class TrazabilidadMixin:
    criterio_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    tarea_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    prueba_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    cambios: Mapped[str] = mapped_column(Text, default="", nullable=False)
    estado_cobertura: Mapped[str] = mapped_column(String(32), default="Pendiente", nullable=False)


class SeguimientoMixin:
    fecha: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    tiempo: Mapped[float] = mapped_column(default=0.0, nullable=False)
    notas: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ProyectoMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default="", nullable=False)
    estado: Mapped[str] = mapped_column(String(32), default="Activo", nullable=False)
    responsable: Mapped[str] = mapped_column(String(128), default="", nullable=False)

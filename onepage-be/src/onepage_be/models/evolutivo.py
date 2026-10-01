"""Modelo de datos de la base de datos de evolutivos."""

from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import EvolutivosBase as Base
from .mixins import (
    AccionReunionMixin,
    ActividadMixin,
    ActividadDesarrolloMixin,
    BaseDatosAfectadaMixin,
    BloquesComunesMixin,
    CabeceraMixin,
    CambioMixin,
    CasoPlanMixin,
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

_EVO_FK = "evolutivos.id"


def _evo_fk() -> Mapped[int]:
    return mapped_column(ForeignKey(_EVO_FK, ondelete="CASCADE"), nullable=False, index=True)


class Proyecto(ProyectoMixin, TimestampMixin, Base):
    __tablename__ = "proyectos"

    evolutivos: Mapped[list["Evolutivo"]] = relationship(
        back_populates="proyecto", cascade="all, delete-orphan"
    )


class Evolutivo(PkMixin, CabeceraMixin, BloquesComunesMixin, OrdenMixin, TimestampMixin, Base):
    __tablename__ = "evolutivos"

    proyecto_id: Mapped[str] = mapped_column(
        ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    referencia_normativa: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    descripcion_requerimiento: Mapped[str] = mapped_column(Text, default="", nullable=False)
    objetivo: Mapped[str] = mapped_column(Text, default="", nullable=False)
    alcance: Mapped[str] = mapped_column(Text, default="", nullable=False)
    tareas_planificadas: Mapped[str] = mapped_column(Text, default="", nullable=False)

    proyecto: Mapped[Proyecto] = relationship(back_populates="evolutivos")


class GrupoRequisito(PkMixin, OrdenMixin, Base):
    __tablename__ = "grupos_requisito"

    evolutivo_id: Mapped[int] = _evo_fk()
    nombre: Mapped[str] = mapped_column(String(255), default="", nullable=False)


class Requisito(PkMixin, OrdenMixin, Base):
    __tablename__ = "requisitos"

    evolutivo_id: Mapped[int] = _evo_fk()
    grupo_id: Mapped[int] = mapped_column(
        ForeignKey("grupos_requisito.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    detalle: Mapped[str] = mapped_column(Text, default="", nullable=False)


class CriterioAceptacion(PkMixin, CriterioMixin, OrdenMixin, Base):
    __tablename__ = "criterios_aceptacion"

    evolutivo_id: Mapped[int] = _evo_fk()
    requisito_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class Repositorio(PkMixin, RepositorioMixin, OrdenMixin, Base):
    __tablename__ = "repositorios"

    evolutivo_id: Mapped[int] = _evo_fk()


class Tarea(PkMixin, TareaMixin, OrdenMixin, Base):
    __tablename__ = "tareas"

    evolutivo_id: Mapped[int] = _evo_fk()
    requisito_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class TareaDesarrollada(PkMixin, TareaDesarrolloMixin, OrdenMixin, Base):
    __tablename__ = "tareas_desarrolladas"

    evolutivo_id: Mapped[int] = _evo_fk()
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


class CasoPlan(PkMixin, CasoPlanMixin, OrdenMixin, Base):
    __tablename__ = "casos_plan"

    evolutivo_id: Mapped[int] = _evo_fk()


class CasoPrueba(PkMixin, CasoPruebaMixin, OrdenMixin, Base):
    __tablename__ = "casos_prueba"

    evolutivo_id: Mapped[int] = _evo_fk()
    caso_plan_id: Mapped[int] = mapped_column(
        ForeignKey("casos_plan.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    requisito_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class EjecucionPrueba(PkMixin, EjecucionMixin, OrdenMixin, Base):
    __tablename__ = "ejecuciones_prueba"

    caso_id: Mapped[int] = mapped_column(
        ForeignKey("casos_prueba.id", ondelete="CASCADE"), nullable=False, index=True
    )


class DefinitionOfDone(PkMixin, DodMixin, OrdenMixin, Base):
    __tablename__ = "definition_of_done"

    evolutivo_id: Mapped[int] = _evo_fk()


class Despliegue(PkMixin, DespliegueMixin, OrdenMixin, Base):
    __tablename__ = "despliegues"

    evolutivo_id: Mapped[int] = _evo_fk()


class BaseDatosAfectada(PkMixin, BaseDatosAfectadaMixin, OrdenMixin, Base):
    __tablename__ = "bases_datos_afectadas"

    evolutivo_id: Mapped[int] = _evo_fk()


class Reunion(PkMixin, ReunionMixin, OrdenMixin, Base):
    __tablename__ = "reuniones"

    evolutivo_id: Mapped[int] = _evo_fk()


class AccionReunion(PkMixin, AccionReunionMixin, OrdenMixin, Base):
    __tablename__ = "acciones_reunion"

    reunion_id: Mapped[int] = mapped_column(
        ForeignKey("reuniones.id", ondelete="CASCADE"), nullable=False, index=True
    )


class Planificacion(PkMixin, PlanificacionMixin, OrdenMixin, Base):
    __tablename__ = "planificacion"

    evolutivo_id: Mapped[int] = _evo_fk()
    requisito_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class Trazabilidad(PkMixin, TrazabilidadMixin, OrdenMixin, Base):
    __tablename__ = "trazabilidad"

    evolutivo_id: Mapped[int] = _evo_fk()
    requisito_codigo: Mapped[str] = mapped_column(String(32), default="", nullable=False)


class Seguimiento(PkMixin, SeguimientoMixin, OrdenMixin, Base):
    __tablename__ = "seguimientos"

    evolutivo_id: Mapped[int] = _evo_fk()


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

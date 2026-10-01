"""Router de evolutivos."""

from __future__ import annotations

from ..database import get_evolutivos_db
from ..models import evolutivo as m
from .documents import build_document_router
from .factory import Child

CHILDREN: tuple[Child, ...] = (
    Child("grupos-requisito", m.GrupoRequisito, "evolutivo_id", "EvoGrupoRequisito"),
    Child("requisitos", m.Requisito, "evolutivo_id", "EvoRequisito"),
    Child("criterios", m.CriterioAceptacion, "evolutivo_id", "EvoCriterio"),
    Child("repositorios", m.Repositorio, "evolutivo_id", "EvoRepositorio"),
    Child("tareas", m.Tarea, "evolutivo_id", "EvoTarea"),
    Child("tareas-desarrollo", m.TareaDesarrollada, "evolutivo_id", "EvoTareaDesarrollo"),
    Child(
        "actividades-desarrollo",
        m.ActividadDesarrollo,
        "tarea_desarrollo_id",
        "EvoActividadDesarrollo",
        parent_path="tareas-desarrollo",
    ),
    Child("casos-plan", m.CasoPlan, "evolutivo_id", "EvoCasoPlan"),
    Child("casos-prueba", m.CasoPrueba, "evolutivo_id", "EvoCasoPrueba"),
    Child("definition-of-done", m.DefinitionOfDone, "evolutivo_id", "EvoDod"),
    Child("registros-despliegue", m.Despliegue, "evolutivo_id", "EvoDespliegue"),
    Child("bases-datos", m.BaseDatosAfectada, "evolutivo_id", "EvoBaseDatos"),
    Child("reuniones", m.Reunion, "evolutivo_id", "EvoReunion"),
    Child("planificacion", m.Planificacion, "evolutivo_id", "EvoPlanificacion"),
    Child("trazabilidad", m.Trazabilidad, "evolutivo_id", "EvoTrazabilidad"),
    Child("seguimientos", m.Seguimiento, "evolutivo_id", "EvoSeguimiento"),
    Child("recursos", m.RecursoTarea, "tarea_id", "EvoRecursoTarea", parent_path="tareas"),
    Child("actividades", m.ActividadTarea, "tarea_id", "EvoActividadTarea", parent_path="tareas"),
    Child("cambios", m.Cambio, "tarea_id", "EvoCambio", parent_path="tareas"),
    Child(
        "cambios-desarrollo",
        m.CambioDesarrollo,
        "tarea_desarrollo_id",
        "EvoCambioDesarrollo",
        parent_path="tareas-desarrollo",
    ),
    Child(
        "ejecuciones",
        m.EjecucionPrueba,
        "caso_id",
        "EvoEjecucionPrueba",
        parent_path="casos-prueba",
    ),
    Child("acciones", m.AccionReunion, "reunion_id", "EvoAccionReunion", parent_path="reuniones"),
    Child(
        "tareas-seguimiento",
        m.TareaSeguimiento,
        "seguimiento_id",
        "EvoTareaSeguimiento",
        parent_path="seguimientos",
    ),
    Child(
        "actividades-seguimiento",
        m.ActividadSeguimiento,
        "tarea_seguimiento_id",
        "EvoActividadSeguimiento",
        parent_path="tareas-seguimiento",
    ),
)

router = build_document_router(
    prefix="/api/evolutivos",
    tag="evolutivos",
    name="Evolutivo",
    doc_model=m.Evolutivo,
    children=CHILDREN,
    get_db=get_evolutivos_db,
)

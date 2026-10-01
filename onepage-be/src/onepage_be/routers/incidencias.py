"""Router de incidencias."""

from __future__ import annotations

from ..database import get_incidencias_db
from ..models import incidencia as m
from .documents import build_document_router
from .factory import Child

CHILDREN: tuple[Child, ...] = (
    Child("criterios", m.CriterioAceptacion, "incidencia_id", "IncCriterio"),
    Child("repositorios", m.Repositorio, "incidencia_id", "IncRepositorio"),
    Child("tareas", m.Tarea, "incidencia_id", "IncTarea"),
    Child("tareas-desarrollo", m.TareaDesarrollada, "incidencia_id", "IncTareaDesarrollo"),
    Child(
        "actividades-desarrollo",
        m.ActividadDesarrollo,
        "tarea_desarrollo_id",
        "IncActividadDesarrollo",
        parent_path="tareas-desarrollo",
    ),
    Child("casos-plan", m.CasoPlan, "incidencia_id", "IncCasoPlan"),
    Child("casos-prueba", m.CasoPrueba, "incidencia_id", "IncCasoPrueba"),
    Child("definition-of-done", m.DefinitionOfDone, "incidencia_id", "IncDod"),
    Child("registros-despliegue", m.Despliegue, "incidencia_id", "IncDespliegue"),
    Child("bases-datos", m.BaseDatosAfectada, "incidencia_id", "IncBaseDatos"),
    Child("reuniones", m.Reunion, "incidencia_id", "IncReunion"),
    Child("planificacion", m.Planificacion, "incidencia_id", "IncPlanificacion"),
    Child("trazabilidad", m.Trazabilidad, "incidencia_id", "IncTrazabilidad"),
    Child("seguimientos", m.Seguimiento, "incidencia_id", "IncSeguimiento"),
    Child("recursos", m.RecursoTarea, "tarea_id", "IncRecursoTarea", parent_path="tareas"),
    Child("actividades", m.ActividadTarea, "tarea_id", "IncActividadTarea", parent_path="tareas"),
    Child("cambios", m.Cambio, "tarea_id", "IncCambio", parent_path="tareas"),
    Child(
        "cambios-desarrollo",
        m.CambioDesarrollo,
        "tarea_desarrollo_id",
        "IncCambioDesarrollo",
        parent_path="tareas-desarrollo",
    ),
    Child(
        "ejecuciones",
        m.EjecucionPrueba,
        "caso_id",
        "IncEjecucionPrueba",
        parent_path="casos-prueba",
    ),
    Child("acciones", m.AccionReunion, "reunion_id", "IncAccionReunion", parent_path="reuniones"),
    Child(
        "tareas-seguimiento",
        m.TareaSeguimiento,
        "seguimiento_id",
        "IncTareaSeguimiento",
        parent_path="seguimientos",
    ),
    Child(
        "actividades-seguimiento",
        m.ActividadSeguimiento,
        "tarea_seguimiento_id",
        "IncActividadSeguimiento",
        parent_path="tareas-seguimiento",
    ),
)

router = build_document_router(
    prefix="/api/incidencias",
    tag="incidencias",
    name="Incidencia",
    doc_model=m.Incidencia,
    children=CHILDREN,
    get_db=get_incidencias_db,
)

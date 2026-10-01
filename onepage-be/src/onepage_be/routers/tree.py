"""Arbol de navegacion: proyectos con sus evolutivos e incidencias."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_evolutivos_db, get_incidencias_db
from ..models import evolutivo as me
from ..models import incidencia as mi

router = APIRouter(prefix="/api", tags=["navegacion"])


@router.get("/arbol")
def arbol(
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> list[dict[str, Any]]:
    proyectos = sorted(crud.list_all(db_e, me.Proyecto), key=lambda p: p.nombre.lower())
    evolutivos = crud.list_all(db_e, me.Evolutivo)
    incidencias = crud.list_all(db_i, mi.Incidencia)

    nodos: list[dict[str, Any]] = []
    for proyecto in proyectos:
        nodos.append(
            {
                "id": proyecto.id,
                "tipo": "proyecto",
                "nombre": proyecto.nombre,
                "estado": proyecto.estado,
                "evolutivos": [
                    {
                        "id": e.id,
                        "tipo": "evolutivo",
                        "codigo": e.codigo,
                        "titulo": e.titulo or "(sin titulo)",
                        "estado": e.estado,
                        "prioridad": e.prioridad,
                    }
                    for e in evolutivos
                    if e.proyecto_id == proyecto.id
                ],
                "incidencias": [
                    {
                        "id": i.id,
                        "tipo": "incidencia",
                        "codigo": i.codigo,
                        "titulo": i.titulo or "(sin titulo)",
                        "estado": i.estado,
                        "severidad": i.severidad,
                    }
                    for i in incidencias
                    if i.proyecto_id == proyecto.id
                ],
            }
        )
    return nodos


def _partes(db: Session, m: Any, doc_model: type, doc_field: str, tipo: str) -> list[dict[str, Any]]:
    docs = {d.id: d for d in crud.list_all(db, doc_model)}
    tareas = crud.list_all(db, m.TareaSeguimiento)
    actividades = crud.list_all(db, m.ActividadSeguimiento)
    partes: list[dict[str, Any]] = []
    for s in crud.list_all(db, m.Seguimiento):
        doc = docs.get(getattr(s, doc_field))
        if doc is None:
            continue
        partes.append(
            {
                "id": s.id,
                "fecha": s.fecha,
                "tiempo": s.tiempo,
                "notas": s.notas,
                "documento": {
                    "tipo": tipo,
                    "id": doc.id,
                    "codigo": doc.codigo,
                    "titulo": doc.titulo or "(sin titulo)",
                    "proyecto_id": doc.proyecto_id,
                },
                "tareas": [
                    {
                        "id": t.id,
                        "nombre": t.nombre or t.tarea_codigo or "Tarea",
                        "descripcion": t.descripcion,
                        "completada": t.completada,
                        "actividades": [
                            {"id": a.id, "descripcion": a.descripcion, "completada": a.completada}
                            for a in actividades
                            if a.tarea_seguimiento_id == t.id
                        ],
                    }
                    for t in tareas
                    if t.seguimiento_id == s.id
                ],
            }
        )
    return partes


@router.get("/diario")
def diario(
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> list[dict[str, Any]]:
    """Partes de seguimiento de evolutivos e incidencias, para mostrarlos como diario."""
    proyectos = {p.id: p.nombre for p in crud.list_all(db_e, me.Proyecto)}
    partes = _partes(db_e, me, me.Evolutivo, "evolutivo_id", "evolutivos") + _partes(
        db_i, mi, mi.Incidencia, "incidencia_id", "incidencias"
    )
    for parte in partes:
        parte["documento"]["proyecto"] = proyectos.get(parte["documento"]["proyecto_id"], "")
    return partes

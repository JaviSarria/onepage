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

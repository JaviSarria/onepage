"""Router de proyectos: se replican en ambas bases de datos con el mismo id."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_evolutivos_db, get_incidencias_db
from ..models import evolutivo as me
from ..models import incidencia as mi

router = APIRouter(prefix="/api/proyectos", tags=["proyectos"])


class ProyectoIn(BaseModel):
    nombre: str
    descripcion: str = ""
    estado: str = "Activo"
    responsable: str = ""


class ProyectoPatch(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    estado: str | None = None
    responsable: str | None = None


class ProyectoOut(ProyectoIn):
    id: str

    model_config = {"from_attributes": True}


@router.get("", response_model=list[ProyectoOut])
def listar(db: Session = Depends(get_evolutivos_db)) -> list[me.Proyecto]:
    return sorted(crud.list_all(db, me.Proyecto), key=lambda p: p.nombre.lower())


@router.get("/{proyecto_id}", response_model=ProyectoOut)
def obtener(proyecto_id: str, db: Session = Depends(get_evolutivos_db)) -> me.Proyecto:
    return crud.get_or_404(db, me.Proyecto, proyecto_id)


@router.post("", response_model=ProyectoOut, status_code=201)
def crear(
    payload: ProyectoIn,
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> me.Proyecto:
    data = payload.model_dump() | {"id": str(uuid.uuid4())}
    crud.create(db_i, mi.Proyecto, dict(data))
    return crud.create(db_e, me.Proyecto, dict(data))


@router.put("/{proyecto_id}", response_model=ProyectoOut)
def actualizar(
    proyecto_id: str,
    payload: ProyectoPatch,
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> me.Proyecto:
    cambios = payload.model_dump(exclude_unset=True)
    espejo = db_i.get(mi.Proyecto, proyecto_id)
    if espejo is not None:
        crud.update(db_i, espejo, cambios)
    obj = crud.get_or_404(db_e, me.Proyecto, proyecto_id)
    return crud.update(db_e, obj, cambios)


@router.delete("/{proyecto_id}")
def borrar(
    proyecto_id: str,
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> dict[str, bool]:
    obj_e = db_e.get(me.Proyecto, proyecto_id)
    obj_i = db_i.get(mi.Proyecto, proyecto_id)
    if obj_e is None and obj_i is None:
        raise HTTPException(status_code=404, detail=f"Proyecto {proyecto_id} no encontrado")
    if obj_i is not None:
        crud.delete(db_i, obj_i)
    if obj_e is not None:
        crud.delete(db_e, obj_e)
    return {"ok": True}

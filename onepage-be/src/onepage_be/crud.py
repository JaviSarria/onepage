"""Operaciones CRUD genericas sobre los modelos ORM."""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session


def list_by(db: Session, model: type, field: str, value: Any) -> list[Any]:
    stmt = select(model).where(getattr(model, field) == value)
    if hasattr(model, "orden"):
        stmt = stmt.order_by(model.orden, model.id)
    return list(db.scalars(stmt))


def list_all(db: Session, model: type) -> list[Any]:
    stmt = select(model)
    if hasattr(model, "orden"):
        stmt = stmt.order_by(model.orden, model.id)
    return list(db.scalars(stmt))


def get_or_404(db: Session, model: type, pk: Any) -> Any:
    obj = db.get(model, pk)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} {pk} no encontrado")
    return obj


def create(db: Session, model: type, data: dict[str, Any]) -> Any:
    obj = model(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, obj: Any, data: dict[str, Any]) -> Any:
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, obj: Any) -> None:
    db.delete(obj)
    db.commit()

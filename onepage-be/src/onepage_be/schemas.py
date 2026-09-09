"""Generacion automatica de esquemas Pydantic a partir de los modelos SQLAlchemy."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, create_model
from sqlalchemy import Boolean, DateTime, Float, Integer

_MODEL_CONFIG = ConfigDict(from_attributes=True)


def _python_type(column: Any) -> type:
    tipo = column.type
    if isinstance(tipo, Boolean):
        return bool
    if isinstance(tipo, Integer):
        return int
    if isinstance(tipo, Float):
        return float
    if isinstance(tipo, DateTime):
        return datetime
    return str


def _default_for(column: Any) -> Any:
    if column.default is not None and getattr(column.default, "is_scalar", False):
        return column.default.arg
    if column.nullable:
        return None
    return ...


def build_schemas(
    model: type,
    *,
    name: str,
    exclude_create: tuple[str, ...] = (),
) -> tuple[type[BaseModel], type[BaseModel], type[BaseModel]]:
    """Devuelve las clases (Read, Create, Update) del modelo indicado."""
    read_fields: dict[str, Any] = {}
    create_fields: dict[str, Any] = {}
    update_fields: dict[str, Any] = {}

    for column in model.__table__.columns:
        key = column.key
        tipo = _python_type(column)
        optional = tipo | None if column.nullable else tipo
        read_fields[key] = (optional, None if column.nullable else ...)

        if key in exclude_create or key in {"created_at", "updated_at"}:
            continue
        if key == "id" and isinstance(column.type, Integer):
            continue
        create_fields[key] = (optional, _default_for(column))
        update_fields[key] = (tipo | None, None)

    read = create_model(f"{name}Read", __config__=_MODEL_CONFIG, **read_fields)
    create = create_model(f"{name}Create", __config__=_MODEL_CONFIG, **create_fields)
    update = create_model(f"{name}Update", __config__=_MODEL_CONFIG, **update_fields)
    return read, create, update

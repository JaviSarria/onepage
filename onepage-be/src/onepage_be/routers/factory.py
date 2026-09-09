"""Fabrica de routers CRUD genericos para documentos y sus secciones."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud
from ..schemas import build_schemas


@dataclass(frozen=True)
class Child:
    """Descriptor de una seccion hija de un documento."""

    path: str
    model: type
    parent_field: str
    name: str
    parent_path: str | None = None


def register_children(
    router: APIRouter,
    children: tuple[Child, ...],
    get_db: Callable[..., Session],
) -> None:
    for child in children:
        read, create_s, update_s = build_schemas(
            child.model, name=child.name, exclude_create=(child.parent_field,)
        )
        model = child.model
        field = child.parent_field
        base = f"/{child.parent_path}" if child.parent_path else ""

        def make_list(model=model, field=field, read=read):
            def _list(parent_id, db=Depends(get_db)):
                return crud.list_by(db, model, field, parent_id)

            _list.__annotations__ = {"parent_id": int, "db": Session, "return": list[read]}
            return _list

        def make_create(model=model, field=field, read=read, create_s=create_s):
            def _create(parent_id, payload, db=Depends(get_db)):
                data = payload.model_dump()
                data[field] = parent_id
                return crud.create(db, model, data)

            _create.__annotations__ = {
                "parent_id": int,
                "payload": create_s,
                "db": Session,
                "return": read,
            }
            return _create

        def make_get(model=model, read=read):
            def _get(item_id, db=Depends(get_db)):
                return crud.get_or_404(db, model, item_id)

            _get.__annotations__ = {"item_id": int, "db": Session, "return": read}
            return _get

        def make_update(model=model, read=read, update_s=update_s):
            def _update(item_id, payload, db=Depends(get_db)):
                obj = crud.get_or_404(db, model, item_id)
                return crud.update(db, obj, payload.model_dump(exclude_unset=True))

            _update.__annotations__ = {
                "item_id": int,
                "payload": update_s,
                "db": Session,
                "return": read,
            }
            return _update

        def make_delete(model=model):
            def _delete(item_id, db=Depends(get_db)):
                crud.delete(db, crud.get_or_404(db, model, item_id))
                return {"ok": True}

            _delete.__annotations__ = {"item_id": int, "db": Session, "return": dict}
            return _delete

        collection = f"{base}/{{parent_id}}/{child.path}"
        item = f"/{child.path}/item/{{item_id}}"
        tag = child.path

        router.get(collection, response_model=list[read], tags=[tag])(make_list())
        router.post(collection, response_model=read, status_code=201, tags=[tag])(make_create())
        router.get(item, response_model=read, tags=[tag])(make_get())
        router.put(item, response_model=read, tags=[tag])(make_update())
        router.delete(item, tags=[tag])(make_delete())


def serialize(obj: Any) -> dict[str, Any]:
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}

"""Construccion del router de un tipo de documento (evolutivo o incidencia)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud
from ..schemas import build_schemas
from .factory import Child, register_children, serialize


def build_document_router(
    *,
    prefix: str,
    tag: str,
    name: str,
    doc_model: type,
    children: tuple[Child, ...],
    get_db: Callable[..., Session],
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=[tag])
    read, create_s, update_s = build_schemas(doc_model, name=name)

    def _list(proyecto_id=None, db=Depends(get_db)):
        if proyecto_id:
            return crud.list_by(db, doc_model, "proyecto_id", proyecto_id)
        return crud.list_all(db, doc_model)

    _list.__annotations__ = {"proyecto_id": str | None, "db": Session, "return": list[read]}

    def _create(payload, db=Depends(get_db)):
        return crud.create(db, doc_model, payload.model_dump())

    _create.__annotations__ = {"payload": create_s, "db": Session, "return": read}

    def _get(doc_id, db=Depends(get_db)):
        return crud.get_or_404(db, doc_model, doc_id)

    _get.__annotations__ = {"doc_id": int, "db": Session, "return": read}

    def _update(doc_id, payload, db=Depends(get_db)):
        obj = crud.get_or_404(db, doc_model, doc_id)
        return crud.update(db, obj, payload.model_dump(exclude_unset=True))

    _update.__annotations__ = {
        "doc_id": int,
        "payload": update_s,
        "db": Session,
        "return": read,
    }

    def _delete(doc_id, db=Depends(get_db)):
        crud.delete(db, crud.get_or_404(db, doc_model, doc_id))
        return {"ok": True}

    _delete.__annotations__ = {"doc_id": int, "db": Session, "return": dict}

    def _full(doc_id, db=Depends(get_db)) -> dict[str, Any]:
        doc = crud.get_or_404(db, doc_model, doc_id)
        data = serialize(doc)
        cache: dict[str, list[dict[str, Any]]] = {}
        for child in children:
            if child.parent_path is None:
                items = [serialize(i) for i in crud.list_by(db, child.model, child.parent_field, doc_id)]
                data[child.path] = items
                cache[child.path] = items
        for child in children:
            if child.parent_path is None:
                continue
            for parent in cache.get(child.parent_path, []):
                items = [
                    serialize(i)
                    for i in crud.list_by(db, child.model, child.parent_field, parent["id"])
                ]
                parent[child.path] = items
                cache.setdefault(child.path, []).extend(items)
        return data

    _full.__annotations__ = {"doc_id": int, "db": Session, "return": dict}

    router.get("", response_model=list[read])(_list)
    router.post("", response_model=read, status_code=201)(_create)
    router.get("/{doc_id}", response_model=read)(_get)
    router.put("/{doc_id}", response_model=read)(_update)
    router.delete("/{doc_id}")(_delete)
    router.get("/{doc_id}/full")(_full)

    register_children(router, children, get_db)
    return router

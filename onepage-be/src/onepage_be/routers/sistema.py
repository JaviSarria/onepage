"""Gestion de bases de datos: listado, exportacion e importacion."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..config import DATA_DIR

router = APIRouter(prefix="/api/sistema", tags=["sistema"])


def _es_nombre_base(nombre: str) -> bool:
    return nombre.endswith(".sqlite3") and Path(nombre).name == nombre and nombre not in {"", ".", ".."}


@router.get("/bases")
def listar_bases() -> list[dict[str, str]]:
    bases = sorted((p.name for p in DATA_DIR.glob("*.sqlite3") if p.is_file()))
    return [{"nombre": nombre} for nombre in bases]


@router.get("/bases/{nombre}/descargar")
def descargar_base(nombre: str) -> FileResponse:
    if not _es_nombre_base(nombre):
        raise HTTPException(status_code=400, detail="Nombre de base de datos no valido")
    ruta = DATA_DIR / nombre
    if not ruta.is_file():
        raise HTTPException(status_code=404, detail=f"Base de datos no encontrada: {nombre}")
    return FileResponse(ruta, media_type="application/octet-stream", filename=nombre)


@router.post("/bases/{nombre}/importar")
async def importar_base(nombre: str, archivo: UploadFile = File(...)) -> dict[str, object]:
    if not _es_nombre_base(nombre):
        raise HTTPException(status_code=400, detail="Nombre de base de datos no valido")
    destino = DATA_DIR / nombre
    contenido = await archivo.read()
    destino.write_bytes(contenido)
    return {"ok": True, "nombre": nombre, "bytes": len(contenido)}

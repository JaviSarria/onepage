"""Gestion de bases de datos: listado, exportacion e importacion."""

from __future__ import annotations

import io
import zipfile
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

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


@router.get("/exportar")
def exportar() -> StreamingResponse:
    """Exporta todas las bases de datos y el contenido de data/assets en un unico zip."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        for ruta in sorted(DATA_DIR.glob("*.sqlite3")):
            if ruta.is_file():
                z.write(ruta, ruta.name)
        carpeta_assets = DATA_DIR / "assets"
        if carpeta_assets.is_dir():
            for ruta in sorted(carpeta_assets.rglob("*")):
                if ruta.is_file():
                    z.write(ruta, ruta.relative_to(DATA_DIR).as_posix())
    buffer.seek(0)
    nombre_zip = f"export-{datetime.now().strftime('%Y%m%d%H%M')}.zip"
    return StreamingResponse(
        content=iter([buffer.getvalue()]),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{nombre_zip}"'},
    )


def _reescribir(ruta: Path, contenido: bytes) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(contenido)


def _restaurar(rutinas: list[tuple[Path, bytes | None]]) -> None:
    for ruta, anterior in rutinas:
        try:
            if anterior is None:
                if ruta.is_file():
                    ruta.unlink()
            else:
                _reescribir(ruta, anterior)
        except Exception:
            pass


@router.post("/bases/{nombre}/importar")
async def importar_base(nombre: str, archivo: UploadFile = File(...)) -> dict[str, object]:
    if not _es_nombre_base(nombre):
        raise HTTPException(status_code=400, detail="Nombre de base de datos no valido")
    destino = DATA_DIR / nombre
    anterior: bytes | None = None
    if destino.is_file():
        anterior = destino.read_bytes()
    contenido = await archivo.read()
    try:
        _reescribir(destino, contenido)
    except Exception as e:
        if anterior is not None:
            _reescribir(destino, anterior)
        raise HTTPException(status_code=502, detail=f"No se pudo importar la base: {e}") from e
    return {"ok": True, "nombre": nombre, "bytes": len(contenido)}


@router.post("/assets")
async def importar_assets(archivo: UploadFile = File(...)) -> dict[str, object]:
    """Importa ficheros de assets a data/assets."""
    destino = DATA_DIR / "assets" / Path(archivo.filename or "asset").name
    anterior: bytes | None = None
    if destino.is_file():
        anterior = destino.read_bytes()
    contenido = await archivo.read()
    try:
        _reescribir(destino, contenido)
    except Exception as e:
        if anterior is not None:
            _reescribir(destino, anterior)
        raise HTTPException(status_code=502, detail=f"No se pudo importar el asset: {e}") from e
    return {"ok": True, "destino": destino.name, "bytes": len(contenido)}


@router.post("/importar")
async def importar_todo(archivo: UploadFile = File(...)) -> dict[str, object]:
    """Importa un backup completo: evolutivos.sqlite3, incidencias.sqlite3 y assets/."""
    contenido = await archivo.read()
    escrituras: list[tuple[Path, bytes]] = []
    anteriores: list[tuple[Path, bytes | None]] = []
    try:
        with zipfile.ZipFile(io.BytesIO(contenido), "r") as z:
            nombres = set(z.namelist())
            faltantes = [n for n in ("evolutivos.sqlite3", "incidencias.sqlite3") if n not in nombres]
            if faltantes:
                raise HTTPException(status_code=400, detail=f"Faltan ficheros en el zip: {', '.join(faltantes)}")
            for nombre in ("evolutivos.sqlite3", "incidencias.sqlite3"):
                destino = DATA_DIR / nombre
                datos = z.read(nombre)
                escrituras.append((destino, datos))
                anteriores.append((destino, destino.read_bytes() if destino.is_file() else None))
            for info in z.infolist():
                if info.is_dir() or not info.filename.startswith("assets/"):
                    continue
                if ".." in info.filename.split("/"):
                    continue
                destino = DATA_DIR / info.filename
                datos = z.read(info.filename)
                escrituras.append((destino, datos))
                anteriores.append((destino, destino.read_bytes() if destino.is_file() else None))
        for destino, datos in escrituras:
            _reescribir(destino, datos)
    except HTTPException:
        raise
    except Exception as e:
        _restaurar(anteriores)
        raise HTTPException(status_code=502, detail=f"No se pudo importar el backup completo: {e}") from e
    return {"ok": True, "bases": ["evolutivos.sqlite3", "incidencias.sqlite3"], "bytes": sum(len(d) for _, d in escrituras)}

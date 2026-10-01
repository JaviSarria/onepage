"""Imagenes adjuntas a los campos de texto (Descripcion, Notas) de los documentos."""

from __future__ import annotations

import re
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .. import crud
from ..config import DATA_DIR
from ..database import get_evolutivos_db, get_incidencias_db
from ..models import evolutivo as me
from ..models import incidencia as mi

ASSETS_DIR = DATA_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

MAX_BYTES = 20 * 1024 * 1024
# SVG excluido a proposito: puede contener scripts.
EXTENSIONES = {"png", "jpg", "jpeg", "gif", "webp", "bmp"}
CODIGOS_SECCION = {
    "requerimiento": "RQ",
    "problema": "PB",
    "analisis": "AN",
    "desarrollo": "DS",
    "pruebas": "PR",
    "dod": "DD",
    "despliegue": "DP",
    "reuniones": "RE",
    "seguimiento": "SG",
}
NOMBRE_VALIDO = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z]+$")

router = APIRouter(prefix="/api/assets", tags=["assets"])


def _codigo_documento(tipo: str, doc_id: int, db_e: Session, db_i: Session) -> str:
    if tipo == "evolutivos":
        doc, prefijo = crud.get_or_404(db_e, me.Evolutivo, doc_id), "EV"
    elif tipo == "incidencias":
        doc, prefijo = crud.get_or_404(db_i, mi.Incidencia, doc_id), "INC"
    else:
        raise HTTPException(400, "Tipo de documento no valido")
    codigo = re.sub(r"[^A-Za-z0-9-]", "", doc.codigo or "")
    return codigo or f"{prefijo}{doc_id:02d}"


@router.post("", status_code=201)
async def subir(
    request: Request,
    tipo: str,
    doc_id: int,
    seccion: str,
    ext: str,
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> dict[str, str]:
    ext = ext.lower().lstrip(".")
    if ext not in EXTENSIONES:
        raise HTTPException(400, "Formato de imagen no soportado")
    if seccion not in CODIGOS_SECCION:
        raise HTTPException(400, "Seccion no valida")
    contenido = await request.body()
    if not contenido:
        raise HTTPException(400, "Fichero vacio")
    if len(contenido) > MAX_BYTES:
        raise HTTPException(413, "La imagen supera el tamano maximo (20 MB)")

    # Formato: <CODIGO>-<SECCION>-<YYYYMMDD>-<N>.<EXT>, p. ej. INC01-AN-20260910-2.PNG
    base = "-".join(
        [
            _codigo_documento(tipo, doc_id, db_e, db_i),
            CODIGOS_SECCION[seccion],
            date.today().strftime("%Y%m%d"),
        ]
    )
    contador = 1
    while True:
        nombre = f"{base}-{contador}.{ext.upper()}"
        if not any(ASSETS_DIR.glob(f"{base}-{contador}.*")):
            try:
                with open(ASSETS_DIR / nombre, "xb") as fichero:
                    fichero.write(contenido)
                break
            except FileExistsError:
                pass
        contador += 1
    return {"nombre": nombre, "url": f"/api/assets/{nombre}"}


@router.get("/{nombre}")
def descargar(nombre: str) -> FileResponse:
    if not NOMBRE_VALIDO.match(nombre) or nombre.rsplit(".", 1)[1].lower() not in EXTENSIONES:
        raise HTTPException(404, "No encontrado")
    ruta = ASSETS_DIR / nombre
    if not ruta.is_file():
        raise HTTPException(404, "No encontrado")
    return FileResponse(ruta, headers={"X-Content-Type-Options": "nosniff"})

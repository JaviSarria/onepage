"""Aplicacion FastAPI de OnePage."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import CORS_ORIGINS
from .database import init_databases
from .logging import configure_logging
from .routers import assets, evolutivos, incidencias, proyectos, search, sistema, tree

logger = logging.getLogger("onepage")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    configure_logging()
    logger.info("Servicio OnePage iniciado")
    init_databases()
    yield
    logger.info("Servicio OnePage detenido")


app = FastAPI(
    title="OnePage API",
    version="0.1.0",
    description="Gestion de proyectos, evolutivos e incidencias",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(proyectos.router)
app.include_router(tree.router)
app.include_router(evolutivos.router)
app.include_router(incidencias.router)
app.include_router(assets.router)
app.include_router(search.router)
app.include_router(sistema.router)


@app.get("/api/salud", tags=["sistema"])
def salud() -> dict[str, str]:
    return {"estado": "ok"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Loguea los errores HTTP y devuelve la respuesta con el detalle."""
    logger.warning("HTTPException %s %s %s %s", request.method, request.url.path, exc.status_code, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Loguea el error no controlado y devuelve una respuesta 500."""
    logger.exception("Error no controlado en %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})

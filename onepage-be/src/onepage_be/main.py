"""Aplicacion FastAPI de OnePage."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS
from .database import init_databases
from .routers import assets, evolutivos, incidencias, proyectos, search, tree


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_databases()
    yield


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


@app.get("/api/salud", tags=["sistema"])
def salud() -> dict[str, str]:
    return {"estado": "ok"}

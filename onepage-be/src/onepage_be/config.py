"""Configuracion basica del backend."""

from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.environ.get("ONEPAGE_DATA_DIR", BASE_DIR / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

EVOLUTIVOS_DB_PATH = DATA_DIR / "evolutivos.sqlite3"
INCIDENCIAS_DB_PATH = DATA_DIR / "incidencias.sqlite3"

EVOLUTIVOS_DB_URL = f"sqlite:///{EVOLUTIVOS_DB_PATH.as_posix()}"
INCIDENCIAS_DB_URL = f"sqlite:///{INCIDENCIAS_DB_PATH.as_posix()}"

CORS_ORIGINS = os.environ.get(
    "ONEPAGE_CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

API_HOST = os.environ.get("ONEPAGE_BE_HOST", "127.0.0.1")
API_PORT = int(os.environ.get("ONEPAGE_BE_PORT", "8000"))

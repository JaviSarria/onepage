"""Punto de entrada del backend de OnePage."""

from __future__ import annotations


def main() -> None:
    import uvicorn

    from .config import API_HOST, API_PORT

    uvicorn.run("onepage_be.main:app", host=API_HOST, port=API_PORT, reload=False)

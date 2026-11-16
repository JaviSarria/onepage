"""Configuracion del logging del backend de OnePage."""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

from .config import DATA_DIR

LOG_FILE = DATA_DIR / "onepage.log"
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(log_file: Path | None = None) -> None:
    """Configura el logging del servicio con archivo rotado y consola estandar."""
    destino = log_file or LOG_FILE
    destino.parent.mkdir(parents=True, exist_ok=True)
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()
    file_handler = logging.handlers.RotatingFileHandler(
        destino, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(stream_handler)

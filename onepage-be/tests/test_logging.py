"""Pruebas unitarias para el logging del backend de OnePage."""

import logging
import shutil
import tempfile
import unittest
from logging.handlers import RotatingFileHandler
from pathlib import Path

from onepage_be.logging import LOG_FILE, configure_logging


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.root_logger = logging.getLogger()
        self.previous_handlers = list(self.root_logger.handlers)
        self.previous_level = self.root_logger.level
        self.tmp_dir = None

    def tearDown(self):
        for handler in list(self.root_logger.handlers):
            self.root_logger.removeHandler(handler)
            handler.close()
        for handler in self.previous_handlers:
            self.root_logger.addHandler(handler)
        self.root_logger.setLevel(self.previous_level)
        if self.tmp_dir is not None:
            shutil.rmtree(self.tmp_dir, ignore_errors=True)
            self.tmp_dir = None

    def test_configure_logging_writes_to_file(self):
        self.tmp_dir = tempfile.mkdtemp()
        file_path = Path(self.tmp_dir) / "onepage.log"
        configure_logging(file_path)
        handlers = list(logging.getLogger().handlers)
        self.assertTrue(any(isinstance(handler, RotatingFileHandler) for handler in handlers))
        logging.getLogger("onepage").error("Error de prueba en OnePage")
        self.assertTrue(file_path.exists())
        self.assertIn("Error de prueba en OnePage", file_path.read_text(encoding="utf-8"))

    def test_default_log_file(self):
        self.assertEqual(LOG_FILE.name, "onepage.log")


if __name__ == "__main__":
    unittest.main()

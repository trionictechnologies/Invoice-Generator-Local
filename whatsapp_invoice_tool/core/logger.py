"""
Centralized logging helper for the WhatsApp invoice tool.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from .config import project_path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.json"
DEFAULT_LOG_FILE = project_path("logs/app.log", writable=True)


def _load_logging_config(config_path: Optional[Path] = None) -> dict:
  """Load logging configuration from config.json if available."""
  cfg_path = config_path or DEFAULT_CONFIG_PATH
  if cfg_path.exists():
    try:
      with cfg_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("logging", {})
    except (json.JSONDecodeError, OSError):
      pass
  return {}


def get_logger(name: str = "whatsapp_invoice_tool", config_path: Optional[Path] = None) -> logging.Logger:
  """
  Return a module-level logger configured to log to both file and stdout.
  Ensures handlers are added once per logger.
  """
  logger = logging.getLogger(name)
  if logger.handlers:
    return logger

  logging_cfg = _load_logging_config(config_path)
  log_level_name = logging_cfg.get("level", "INFO").upper()
  log_level = getattr(logging, log_level_name, logging.INFO)
  log_file = logging_cfg.get("file", str(DEFAULT_LOG_FILE))
  log_path = Path(log_file)
  if not log_path.is_absolute():
    log_path = project_path(log_path, writable=True)
  log_path.parent.mkdir(parents=True, exist_ok=True)

  formatter = logging.Formatter(
      fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
  )

  file_handler = logging.FileHandler(log_path, encoding="utf-8")
  file_handler.setFormatter(formatter)

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)

  logger.setLevel(log_level)
  logger.addHandler(file_handler)
  logger.addHandler(stream_handler)
  logger.propagate = False

  logger.debug("Logger initialized with level %s at %s", log_level_name, log_path)
  return logger

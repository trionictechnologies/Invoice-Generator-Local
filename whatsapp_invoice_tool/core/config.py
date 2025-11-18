"""
Configuration loader utility for the WhatsApp invoice tool.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Union
import sys


def _resource_root() -> Path:
  base = getattr(sys, "_MEIPASS", None)
  if base:
    return Path(base)
  return Path(__file__).resolve().parents[1]


RESOURCE_ROOT = _resource_root()


def _writable_root() -> Path:
  if getattr(sys, "_MEIPASS", None):
    return Path(sys.executable).parent
  return RESOURCE_ROOT


WRITABLE_ROOT = _writable_root()
DEFAULT_CONFIG_PATH = RESOURCE_ROOT / "config.json"


PathLike = Union[str, Path]


@lru_cache(maxsize=1)
def load_config(config_path: PathLike = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
  """Load config.json and cache the result."""
  path = Path(config_path)
  if not path.is_absolute():
    path = RESOURCE_ROOT / path
  if not path.exists():
    raise FileNotFoundError(f"Config file not found at {path}")
  with path.open("r", encoding="utf-8") as file:
    return json.load(file)


def project_path(relative_path: PathLike, *, writable: bool = False) -> Path:
  """
  Return an absolute path either under the resource root (read-only assets)
  or the writable root (for generated artifacts).
  """
  path = Path(relative_path)
  if path.is_absolute():
    return path
  base = WRITABLE_ROOT if writable else RESOURCE_ROOT
  return base / path

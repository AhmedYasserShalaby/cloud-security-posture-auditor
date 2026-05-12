from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from cloud_audit.paths import ROOT


def project_path(path: str | Path) -> Path:
    return ROOT / path


def load_settings() -> dict[str, Any]:
    with project_path("config/settings.yaml").open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

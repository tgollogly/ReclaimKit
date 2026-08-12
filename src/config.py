from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = Path("config.yaml")


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path or DEFAULT_CONFIG_PATH)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found at {config_path}. Copy config.example.yaml to config.yaml first."
        )
    with config_path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def subject_name(config: dict[str, Any]) -> str:
    return config["subject"]["full_name"]

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from src.security import is_safe_http_url

DEFAULT_CONFIG_PATH = Path("config.yaml")

REQUIRED_KEYS = {
    "subject": ["full_name", "email"],
    "case": ["facebook"],
    "evidence": ["screenshots_dir", "output_dir"],
}


class ConfigError(ValueError):
    """Invalid or incomplete configuration."""


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path or DEFAULT_CONFIG_PATH)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found at {config_path}. Copy config.example.yaml to config.yaml first."
        )
    if not config_path.is_file():
        raise ConfigError(f"Config path is not a file: {config_path}")

    with config_path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    if not isinstance(raw, dict):
        raise ConfigError("Config root must be a YAML mapping")

    config = _apply_env_secrets(raw)
    validate_config(config)
    return config


def _apply_env_secrets(config: dict[str, Any]) -> dict[str, Any]:
    """Allow secrets via environment variables (safer than committing to config)."""
    auto = config.setdefault("automation", {})
    smtp = auto.setdefault("smtp", {})
    img = auto.setdefault("image_search", {})

    if os.environ.get("RECLAIMKIT_SMTP_PASSWORD"):
        smtp["password"] = os.environ["RECLAIMKIT_SMTP_PASSWORD"]
    if os.environ.get("RECLAIMKIT_SLACK_WEBHOOK"):
        auto["slack_webhook_url"] = os.environ["RECLAIMKIT_SLACK_WEBHOOK"]
    if os.environ.get("RECLAIMKIT_SERPAPI_KEY"):
        img["serpapi_key"] = os.environ["RECLAIMKIT_SERPAPI_KEY"]
    if os.environ.get("RECLAIMKIT_TINEYE_KEY"):
        img["tineye_api_key"] = os.environ["RECLAIMKIT_TINEYE_KEY"]

    return config


def validate_config(config: dict[str, Any]) -> None:
    subject = config.get("subject")
    if not isinstance(subject, dict):
        raise ConfigError("Missing subject section in config.yaml")

    for key in REQUIRED_KEYS["subject"]:
        if not subject.get(key):
            raise ConfigError(f"config.yaml subject.{key} is required")

    case = config.get("case")
    if not isinstance(case, dict):
        raise ConfigError("Missing case section in config.yaml")

    fb = case.get("facebook")
    if not isinstance(fb, dict):
        raise ConfigError("Missing case.facebook section in config.yaml")

    for key in ("group_name", "post_caption", "post_url"):
        if not fb.get(key):
            raise ConfigError(f"config.yaml case.facebook.{key} is required")

    post_url = fb["post_url"]
    if not is_safe_http_url(post_url):
        raise ConfigError("case.facebook.post_url must be http(s) URL")

    evidence = config.get("evidence")
    if not isinstance(evidence, dict):
        raise ConfigError("Missing evidence section in config.yaml")

    for key in REQUIRED_KEYS["evidence"]:
        if not evidence.get(key):
            raise ConfigError(f"config.yaml evidence.{key} is required")

    monitor = config.get("monitor", {})
    queries = monitor.get("search_queries", [])
    if queries is not None and not isinstance(queries, list):
        raise ConfigError("monitor.search_queries must be a list")


def subject_name(config: dict[str, Any]) -> str:
    return config["subject"]["full_name"]

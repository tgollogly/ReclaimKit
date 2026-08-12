"""Legacy entry point — delegates to campaign escalation system."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.campaign import generate_next_package, init_campaign, load_state


def write_takedown_letters(config: dict[str, Any], output_dir: Path | None = None) -> Path:
    """Generate round-1 campaign package (Meta + Google). Prefer: campaign init."""
    state = init_campaign(config, output_dir)
    package_dir, generated = generate_next_package(config, state)
    if not generated:
        # Force initial rounds
        from src.campaign import generate_round_package

        out = output_dir or Path(config["evidence"]["output_dir"])
        from datetime import datetime, timezone

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        package_dir = out / f"campaign-package-{timestamp}"
        package_dir.mkdir(parents=True, exist_ok=True)
        generate_round_package(config, state, "meta", 1, package_dir)
        generate_round_package(config, state, "google", 1, package_dir)
    return package_dir

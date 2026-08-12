"""System health check and self-test."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

from src.config import load_config, validate_config
from src.escalation_letters import META_ROUNDS, GOOGLE_ROUNDS, ICO_ROUNDS
from src.letter_context import case_ref


def run_doctor(config_path: str = "config.yaml") -> dict[str, Any]:
    report: dict[str, Any] = {"checks": [], "ok": True}

    def check(name: str, passed: bool, detail: str = "") -> None:
        report["checks"].append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            report["ok"] = False

    check("python_version", sys.version_info >= (3, 10), sys.version.split()[0])

    for mod in ("yaml", "PIL", "requests"):
        try:
            importlib.import_module(mod)
            check(f"import_{mod}", True)
        except ImportError as exc:
            check(f"import_{mod}", False, str(exc))

    try:
        import duckduckgo_search  # noqa: F401
        check("import_duckduckgo_search", True)
    except ImportError:
        check("import_duckduckgo_search", False, "pip install duckduckgo-search")

    config: dict[str, Any] | None = None
    try:
        config = load_config(config_path)
        check("config_load", True)
    except FileNotFoundError as exc:
        check("config_load", False, str(exc))
    except Exception as exc:  # noqa: BLE001
        check("config_load", False, str(exc))

    if config:
        try:
            validate_config(config)
            check("config_validate", True)
        except Exception as exc:  # noqa: BLE001
            check("config_validate", False, str(exc))

        evidence = Path(config["evidence"]["screenshots_dir"])
        images = [
            p for p in evidence.glob("*")
            if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]
        check("evidence_screenshots", len(images) > 0, f"{len(images)} image(s) in {evidence}")

        out = Path(config["evidence"]["output_dir"])
        check("output_writable", _dir_writable(out), str(out.resolve()))

        slack = config.get("automation", {}).get("slack_webhook_url", "")
        placeholder = "YOUR/WEBHOOK"
        slack_ok = bool(slack) and placeholder not in slack
        check(
            "slack_configured",
            True,
            "configured" if slack_ok else "optional — set for VPS alerts",
        )

        try:
            letter = META_ROUNDS[1][1](config, {})
            check(
                "letter_meta_r1",
                "Article 17" in letter and config["case"]["facebook"]["post_url"] in letter,
            )
            check("letter_case_ref", case_ref(config, "META-R1") in letter)
        except Exception as exc:  # noqa: BLE001
            check("letter_meta_r1", False, str(exc))

        check("letter_rounds_meta", len(META_ROUNDS) == 6, f"{len(META_ROUNDS)} rounds")
        check("letter_rounds_google", len(GOOGLE_ROUNDS) == 3)
        check("letter_rounds_ico", len(ICO_ROUNDS) == 1)

        state_path = out / "campaign" / "state.json"
        check("campaign_state", state_path.exists(), "Run: python3 main.py campaign init")

    return report


def _dir_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test = path / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink()
        return True
    except OSError:
        return False


def format_doctor_report(report: dict[str, Any]) -> str:
    lines = ["RECLAIMKIT DOCTOR", "=" * 40]
    for item in report["checks"]:
        icon = "✓" if item["passed"] else "✗"
        line = f"  {icon} {item['name']}"
        if item.get("detail") and not item["passed"]:
            line += f" — {item['detail']}"
        lines.append(line)
    lines.append("")
    lines.append("ALL OK" if report["ok"] else "ISSUES FOUND — fix items marked ✗")
    return "\n".join(lines)

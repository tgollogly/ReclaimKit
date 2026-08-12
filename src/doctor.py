"""System health check and self-test."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any

from src.config import load_config, validate_config
from src.escalation_letters import META_ROUNDS, GOOGLE_ROUNDS, ICO_ROUNDS, TRACKS
from src.letter_context import case_ref

PLACEHOLDER_EMAIL_MARKERS = ("example.com", "your.email", "your.real.email")


def run_doctor(config_path: str = "config.yaml") -> dict[str, Any]:
    report: dict[str, Any] = {"checks": [], "warnings": [], "ok": True}

    def check(name: str, passed: bool, detail: str = "") -> None:
        report["checks"].append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            report["ok"] = False

    def warn(name: str, detail: str) -> None:
        report["warnings"].append({"name": name, "detail": detail})

    check("python_version", sys.version_info >= (3, 10), sys.version.split()[0])

    for mod in ("yaml", "PIL", "requests"):
        try:
            importlib.import_module(mod)
            check(f"import_{mod}", True)
        except ImportError as exc:
            check(f"import_{mod}", False, str(exc))

    search_ok = False
    for mod_name in ("ddgs", "duckduckgo_search"):
        try:
            importlib.import_module(mod_name)
            check("import_ddgs", True, mod_name)
            search_ok = True
            break
        except ImportError:
            continue
    if not search_ok:
        check("import_ddgs", False, "pip install ddgs")

    config: dict[str, Any] | None = None
    try:
        config = load_config(config_path)
        check("config_load", True, config_path)
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

        fb = config.get("case", {}).get("facebook", {})
        origin = (fb.get("post_origin") or "uncertain").lower()
        if origin not in {"uncertain", "third_party", "self"}:
            warn("post_origin", f"Invalid post_origin {origin!r} — use uncertain, third_party, or self")
        elif origin == "uncertain":
            check("post_origin_uncertain", True, "safe wording — no false claims about who posted")

        email = config.get("subject", {}).get("email", "")
        if any(m in email.lower() for m in PLACEHOLDER_EMAIL_MARKERS):
            warn("subject_email", f"Replace placeholder email: {email}")

        if fb.get("reported_to_meta") and not fb.get("meta_reports"):
            warn(
                "meta_reports",
                "Add case.facebook.meta_reports (see config.example.yaml) so letters cite CS rejection",
            )

        evidence = Path(config["evidence"]["screenshots_dir"])
        images = [
            p for p in evidence.glob("*")
            if p.is_file() and not p.is_symlink() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]
        if len(images) == 0:
            warn("evidence_screenshots", f"Add PNG/JPG screenshots to {evidence}")
        else:
            check("evidence_screenshots", True, f"{len(images)} image(s)")

        out = Path(config["evidence"]["output_dir"])
        check("output_writable", _dir_writable(out), str(out.resolve()))

        slack = config.get("automation", {}).get("slack_webhook_url", "")
        placeholder = "YOUR/WEBHOOK"
        if slack and placeholder not in slack:
            check("slack_configured", True, "configured")
        else:
            warn("slack_configured", "Optional — set automation.slack_webhook_url for VPS alerts")

        try:
            letter = META_ROUNDS[1][1](config, {})
            check(
                "letter_meta_r1",
                "Article 17" in letter and config["case"]["facebook"]["post_url"] in letter,
            )
            check("letter_case_ref", case_ref(config, "META-R1") in letter)
            check("letter_cs_distinction", "Community Standards" in letter)
        except Exception as exc:  # noqa: BLE001
            check("letter_meta_r1", False, str(exc))

        for track, rounds in TRACKS.items():
            for round_num, (_, fn, _, _) in rounds.items():
                try:
                    text = fn(config, {})
                    if len(text) < 200:
                        raise ValueError("letter too short")
                except Exception as exc:  # noqa: BLE001
                    check(f"letter_{track}_r{round_num}", False, str(exc))
                    break
            else:
                check(f"letter_rounds_{track}", True, f"{len(rounds)} rounds")
                continue
            check(f"letter_rounds_{track}", False, "generation failed")

        state_path = out / "campaign" / "state.json"
        if state_path.exists():
            check("campaign_state", True, str(state_path))
        else:
            warn("campaign_state", "Run: python3 main.py campaign init")

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
        elif item.get("detail") and item["passed"] and item["name"] in {"config_load", "evidence_screenshots", "slack_configured", "campaign_state"}:
            line += f" — {item['detail']}"
        lines.append(line)

    for item in report.get("warnings", []):
        lines.append(f"  ! {item['name']} — {item['detail']}")

    lines.append("")
    if report["ok"]:
        if report.get("warnings"):
            lines.append("CORE CHECKS OK — address warnings above before sending letters")
        else:
            lines.append("ALL OK")
    else:
        lines.append("ISSUES FOUND — fix items marked ✗")
    return "\n".join(lines)

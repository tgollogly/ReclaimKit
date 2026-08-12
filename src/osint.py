from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


# Pseudonym patterns common in AWDTSG-style anonymous groups.
PSEUDONYM_PATTERNS = [
    (r"^[A-Z][a-z]+[A-Z][a-z]+\d+$", "reddit_style_pseudonym"),
    (r"^Anonymous participant \d+$", "facebook_anonymous_participant"),
    (r"^Anonymous participant$", "facebook_anonymous_poster"),
]


def analyse_osint(config: dict[str, Any]) -> dict[str, Any]:
    """
    Document publicly visible identifiers from config and screenshots metadata.

    This does NOT attempt to deanonymise Facebook users. Identifying anonymous
    commenters typically requires a court order / police investigation with Meta.
    """
    commenters = config["case"].get("alleged_commenters", [])
    fb = config["case"]["facebook"]

    profiles: list[dict[str, Any]] = []
    for commenter in commenters:
        name = commenter["display_name"]
        profile: dict[str, Any] = {
            "display_name": name,
            "comment_excerpt": commenter["comment"][:120],
            "posted_approx": commenter.get("posted_approx", "unknown"),
            "classification": classify_username(name),
            "deanonymisation_feasibility": assess_deanonymisation(name),
            "notes": [],
        }

        if profile["classification"] == "reddit_style_pseudonym":
            profile["notes"].append(
                "Auto-generated-style handle common in anonymous posting modes. "
                "Real identity is held by Meta; not discoverable via public OSINT alone."
            )
        elif profile["classification"] == "facebook_anonymous_participant":
            profile["notes"].append(
                "Facebook anonymous posting — identity known only to Meta platform."
            )
        elif " " in name and not name.lower().startswith("anonymous"):
            profile["notes"].append(
                "Appears to be a real display name (not auto-generated). "
                "May be traceable via legal disclosure order to Meta."
            )
            profile["deanonymisation_feasibility"] = "possible_via_legal_process"

        profiles.append(profile)

    location_mentions = extract_location_mentions(commenters)
    name_mentions = extract_name_mentions(commenters, config["subject"]["full_name"])

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "subject": config["subject"]["full_name"],
        "facebook_group": fb["group_name"],
        "important_limitation": (
            "This report documents handles and patterns only. Attempting to identify "
            "anonymous posters without legal authority may breach privacy law in your jurisdiction. "
            "Consult a local solicitor or regulator about lawful disclosure requests to Meta."
        ),
        "commenter_profiles": profiles,
        "location_mentions_in_thread": location_mentions,
        "name_mentions_in_thread": name_mentions,
        "legal_disclosure_pathways": [
            {
                "route": "Civil litigation",
                "description": (
                    "Consult a local solicitor about pre-action letters and disclosure orders "
                    "to identify anonymous posters where your jurisdiction allows."
                ),
                "reference": "Applicable local defamation or privacy law",
            },
            {
                "route": "Regulator complaint against platform",
                "description": (
                    "If the platform fails to erase personal data within the statutory period "
                    "under your jurisdiction's privacy law."
                ),
                "reference": "Configure jurisdiction.regulator_url in config.yaml",
            },
        ],
        "public_osint_actions_taken": [
            "Username pattern classification (no external scraping of Facebook)",
            "Location/name mention extraction from known comments",
            "No attempt to contact or harass identified handles",
        ],
        "recommended_next_steps": _recommended_steps(config),
    }
    return report


def _recommended_steps(config: dict[str, Any]) -> list[str]:
    j = config.get("jurisdiction", {})
    regulator = j.get("regulator_name", "your data protection authority")
    return [
        "Preserve screenshots (run: python3 main.py evidence)",
        "Submit platform privacy erasure letter (run: python3 main.py campaign init)",
        "Do NOT engage with commenters publicly",
        f"If the platform refuses after {j.get('response_days', 30)} days, complain to {regulator}",
        "After removal confirmed, consider closing the account (run: python3 main.py close)",
        "Monitor search engines monthly (python3 main.py monitor)",
    ]


def classify_username(name: str) -> str:
    for pattern, label in PSEUDONYM_PATTERNS:
        if re.match(pattern, name):
            return label
    if name.lower().startswith("anonymous"):
        return "facebook_anonymous"
    return "possible_real_display_name"


def assess_deanonymisation(name: str) -> str:
    classification = classify_username(name)
    if classification in {"reddit_style_pseudonym", "facebook_anonymous_participant", "facebook_anonymous_poster", "facebook_anonymous"}:
        return "requires_meta_legal_disclosure"
    return "unknown_public_osint_limited"


def extract_location_mentions(commenters: list[dict[str, Any]]) -> list[str]:
    """Extract capitalised place-like tokens from comments (heuristic)."""
    found: set[str] = set()
    for commenter in commenters:
        text = commenter.get("comment", "")
        for match in re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b", text):
            if match.lower() not in {"i", "the", "anyone", "please"}:
                found.add(match)
    return sorted(found)


def extract_name_mentions(commenters: list[dict[str, Any]], full_name: str) -> list[str]:
    found: set[str] = set()
    parts = full_name.lower().split()
    for commenter in commenters:
        text = commenter.get("comment", "").lower()
        for part in parts:
            if len(part) > 2 and part in text:
                found.add(part)
    return sorted(found)


def write_osint_report(config: dict[str, Any], output_dir: Path | None = None) -> Path:
    report = analyse_osint(config)
    out = output_dir or Path(config["evidence"]["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = out / f"osint-report-{timestamp}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    summary_path = out / f"osint-report-{timestamp}.txt"
    summary_path.write_text(_format_osint_summary(report), encoding="utf-8")
    return report_path


def _format_osint_summary(report: dict[str, Any]) -> str:
    lines = [
        "OSINT & IDENTIFIER REPORT (LEGAL DOCUMENTATION ONLY)",
        "=" * 60,
        report["important_limitation"],
        "",
        f"Subject: {report['subject']}",
        f"Group: {report['facebook_group']}",
        "",
        "COMMENTERS:",
    ]
    for profile in report["commenter_profiles"]:
        lines.append(f"\n  Handle: {profile['display_name']}")
        lines.append(f"  Type: {profile['classification']}")
        lines.append(f"  ID feasibility: {profile['deanonymisation_feasibility']}")
        for note in profile["notes"]:
            lines.append(f"  Note: {note}")

    lines.extend(["", "LOCATIONS MENTIONED:", ", ".join(report["location_mentions_in_thread"]) or "None"])
    lines.extend(["", "LEGAL PATHWAYS TO IDENTIFY POSTERS:"])
    for pathway in report["legal_disclosure_pathways"]:
        lines.append(f"  - {pathway['route']}: {pathway['description']}")

    return "\n".join(lines) + "\n"

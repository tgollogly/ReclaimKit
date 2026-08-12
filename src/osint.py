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
            "anonymous posters without legal authority may itself breach UK privacy law. "
            "Your solicitor or PSNI can request account data from Meta via court order "
            "or mutual legal assistance."
        ),
        "commenter_profiles": profiles,
        "location_mentions_in_thread": location_mentions,
        "name_mentions_in_thread": name_mentions,
        "legal_disclosure_pathways": [
            {
                "route": "Civil litigation (NI High Court)",
                "description": (
                    "Solicitor can issue a pre-action letter to Meta and apply for "
                    "Norwich Pharmacal or disclosure order to identify posters."
                ),
                "reference": "Defamation Act (Northern Ireland) 2022",
            },
            {
                "route": "Criminal complaint (PSNI)",
                "description": (
                    "False allegations of drugging and sexual offences may fall under "
                    "malicious communications or harassment. PSNI can investigate and "
                    "request data from Meta with appropriate authority."
                ),
                "reference": "Protection from Harassment (NI) Order 1997; Communications Act 2003",
            },
            {
                "route": "ICO complaint against Meta",
                "description": (
                    "If Meta fails to erase personal data within one month of GDPR request."
                ),
                "reference": "UK GDPR Article 17; https://ico.org.uk/make-a-complaint/",
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
    prefs = config.get("preferences", {})
    steps = [
        "Preserve screenshots (run: python3 main.py evidence)",
        "Submit Meta GDPR letter and escalation (run: python3 main.py letters)",
        "Do NOT engage with commenters publicly",
    ]
    if prefs.get("no_police", True):
        steps.extend([
            "If Meta refuses after 30 days, complain to ICO (no police needed)",
            "After removal confirmed, close Facebook (run: python3 main.py close)",
            "Monitor Google monthly after account closure (python3 main.py monitor)",
        ])
    else:
        steps.extend([
            "If criminal allegations persist, consider PSNI report on 101 with evidence pack",
            "Consult NI defamation solicitor for Norwich Pharmacal order if needed",
        ])
    return steps


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
    ni_places = [
        "Omagh", "Enniskillen", "Belfast", "Derry", "Newry", "Armagh",
        "Lisburn", "Bangor", "Coleraine", "Antrim", "Down", "Tyrone",
        "Fermanagh", "Londonderry", "Northern Ireland", "NI",
    ]
    found: set[str] = set()
    for commenter in commenters:
        text = commenter.get("comment", "")
        for place in ni_places:
            if place.lower() in text.lower():
                found.add(place)
    return sorted(found)


def extract_name_mentions(commenters: list[dict[str, Any]], full_name: str) -> list[str]:
    found: set[str] = set()
    parts = full_name.lower().split()
    for commenter in commenters:
        text = commenter.get("comment", "").lower()
        for part in parts:
            if len(part) > 2 and part in text:
                found.add(part)
        if "marty ban" in text:
            found.add("Marty Ban (possible misidentification or alias in thread)")
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

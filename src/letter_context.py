"""Shared context and formatting for legal correspondence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def today_long() -> str:
    return datetime.now(timezone.utc).strftime("%d %B %Y")


def case_ref(config: dict[str, Any], suffix: str = "") -> str:
    name = config["subject"]["full_name"].replace(" ", "-").upper()
    base = f"TG-ER-{name[:12]}"
    return f"{base}-{suffix}" if suffix else base


def format_address(subject: dict[str, Any]) -> str:
    parts = [
        subject.get("address_line1", ""),
        subject.get("city", ""),
        subject.get("county", ""),
        subject.get("postcode", ""),
        subject.get("country", "United Kingdom"),
    ]
    return "\n".join(p for p in parts if p)


def comment_block(config: dict[str, Any], *, numbered: bool = True) -> str:
    commenters = config["case"].get("alleged_commenters", [])
    if not commenters:
        return "  (No comments listed in config.yaml — add alleged_commenters.)"
    lines: list[str] = []
    for idx, c in enumerate(commenters, 1):
        prefix = f"{idx}. " if numbered else "• "
        lines.append(
            f'{prefix}Display name: "{c["display_name"]}" '
            f'({c.get("posted_approx", "date unknown")})\n'
            f'   Comment: "{c["comment"]}"'
        )
    return "\n".join(lines)


def post_details(config: dict[str, Any]) -> dict[str, str]:
    fb = config["case"]["facebook"]
    return {
        "group": fb["group_name"],
        "date": fb["post_date"],
        "caption": fb["post_caption"],
        "url": fb["post_url"] or "[INSERT POST URL]",
    }


def subject_line(config: dict[str, Any]) -> dict[str, str]:
    s = config["subject"]
    return {
        "name": s["full_name"],
        "email": s["email"],
        "phone": s.get("phone", "Not provided"),
        "address": format_address(s),
    }


def false_allegations_summary() -> str:
    return (
        "The thread contains specific false imputations of serious criminal and sexual "
        "misconduct, including claims that I drug drinks and engage in inappropriate "
        "conduct toward family members. I deny each allegation absolutely. No factual "
        "basis for these statements has ever existed."
    )

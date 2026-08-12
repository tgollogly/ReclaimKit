"""Shared context and formatting for legal correspondence."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote_plus


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


def section(title: str) -> str:
    line = "=" * 78
    return f"\n{line}\n{title.upper()}\n{line}\n"


def comment_block(config: dict[str, Any], *, numbered: bool = True) -> str:
    commenters = config["case"].get("alleged_commenters", [])
    if not commenters:
        return "  (No comments listed in config.yaml — add alleged_commenters.)"
    lines: list[str] = []
    for idx, c in enumerate(commenters, 1):
        prefix = f"{idx}. " if numbered else "- "
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


def publication_context_block(config: dict[str, Any]) -> dict[str, str]:
    """
    Wording for who posted — avoids false claims when origin is uncertain.

    post_origin in config.case.facebook:
      - uncertain (default): safe if you may or may not have posted
      - third_party: someone else posted your photo/name
      - self: you posted and want everything removed including comments
    """
    fb = config["case"].get("facebook", {})
    origin = (fb.get("post_origin") or "uncertain").strip().lower()

    if origin == "third_party":
        return {
            "intro": (
                "My photograph and name appear in a Facebook group post I did not create. "
                "I did not authorise publication of my personal data in this context."
            ),
            "personal_data": (
                "(a) My photograph (selfie), published without my knowledge or consent;\n"
                "(b) My personal name in connection with that image and defamatory commentary;\n"
                "(c) All comments that identify, describe, or publish false statements about me;\n"
                "(d) Metadata linking my identity to this content."
            ),
            "consent_ground": (
                "(b) Article 17(1)(c) — Withdrawal of consent. I never consented to this processing "
                "and withdraw any implied consent. No lawful basis under Article 6(1) applies."
            ),
            "unlawful_ground": (
                "(d) Article 17(1)(e) — Unlawful processing. Publication of my image without consent, "
                "combined with false criminal and sexual allegations, is unlawful processing."
            ),
        }

    if origin == "self":
        return {
            "intro": (
                "My personal data appears in a Facebook group post. I request erasure of all "
                "personal data at the URL below regardless of who created the post caption. "
                "I do not consent to continued processing of my likeness, name, or associated "
                "third-party comments on this thread."
            ),
            "personal_data": (
                "(a) My photograph (selfie) at the URL below;\n"
                "(b) My personal name in connection with that image and all commentary;\n"
                "(c) All third-party comments that identify, describe, or publish false statements about me;\n"
                "(d) Metadata linking my identity to this content."
            ),
            "consent_ground": (
                "(b) Article 17(1)(c) — Withdrawal of consent. I withdraw consent for continued "
                "processing of my personal data at this URL and request immediate erasure."
            ),
            "unlawful_ground": (
                "(d) Article 17(1)(e) — Unlawful processing. Continued hosting of false criminal "
                "and sexual allegations alongside my image causes unlawful harm."
            ),
        }

    # uncertain — default; truthful when you do not know who posted
    return {
        "intro": (
            "My photograph and full name appear in a Facebook group post at the URL below. "
            "I request erasure of ALL my personal data at this location. I do not consent to "
            "continued processing of my likeness, name, or the associated comments about me. "
            "This request is made without prejudice as to who created the post; my right as "
            "data subject to erasure applies regardless."
        ),
        "personal_data": (
            "(a) My photograph (selfie) displayed at the URL below;\n"
            "(b) My personal name — in connection with that image and all commentary on the thread;\n"
            "(c) All comments that identify, describe, or publish false statements about me;\n"
            "(d) Metadata linking my identity to this content (including group indexing and copies)."
        ),
        "consent_ground": (
            "(b) Article 17(1)(c) — Withdrawal of consent. I do not consent to continued processing "
            "of my personal data at this URL and withdraw any consent that may previously have applied."
        ),
        "unlawful_ground": (
            "(d) Article 17(1)(e) — Unlawful processing. Hosting my image and name alongside false "
            "criminal and sexual allegations causes unlawful processing and serious harm."
        ),
    }


def publication_summary_for_google(config: dict[str, Any]) -> str:
    origin = (config["case"].get("facebook", {}).get("post_origin") or "uncertain").lower()
    if origin == "third_party":
        return (
            f'publishes my photograph and name without consent alongside comments containing '
            f'false defamatory imputations.'
        )
    if origin == "self":
        return (
            f'contains my photograph and name alongside third-party comments with false '
            f'defamatory imputations. I request delisting while source erasure is pursued.'
        )
    return (
        f'contains my photograph and name alongside comments with false defamatory '
        f'imputations. I request erasure and delisting of my personal data regardless of '
        f'who created the post.'
    )


def false_allegations_summary() -> str:
    return (
        "The thread contains specific false imputations of serious criminal and sexual "
        "misconduct, including claims that I drug drinks and engage in inappropriate "
        "conduct toward family members. I deny each allegation absolutely. No factual "
        "basis for these statements has ever existed. No court, police force, or "
        "regulator has ever found any basis for these claims."
    )


def harm_and_distress_block(config: dict[str, Any]) -> str:
    fb = config["case"].get("facebook", {})
    group = fb.get("group_name", "the named Facebook group")
    custom = config["case"].get("harm_statement", "").strip()
    if custom:
        return custom

    return (
        "This content has caused me serious and ongoing distress, reputational harm, "
        "and anxiety. I am a private individual in Northern Ireland, not a public figure. "
        "The post publishes my likeness and full name alongside solicited abusive commentary "
        f'in the group "{group}". This is targeted reputational harm — functionally bullying '
        "and harassment — regardless of whether Meta's Community Standards team classified "
        "an in-app report differently. Under UK GDPR I am entitled to erasure of my personal "
        "data irrespective of Community Standards outcomes."
    )


def meta_reports_block(config: dict[str, Any]) -> str:
    fb = config["case"].get("facebook", {})
    reports = fb.get("meta_reports")
    if isinstance(reports, list) and reports:
        lines = [
            "I have already used Meta's in-app reporting tools. Those decisions do NOT "
            "discharge Meta's UK GDPR obligations and are recorded below for completeness:",
            "",
        ]
        for idx, report in enumerate(reports, 1):
            if not isinstance(report, dict):
                continue
            lines.append(
                f"{idx}. {report.get('type', 'Report')} "
                f"({report.get('date', 'date not recorded')})\n"
                f"   Outcome: {report.get('outcome', 'pending')}"
            )
            if report.get("notes"):
                lines.append(f"   Notes: {report['notes']}")
        lines.append("")
        lines.append(
            "A Community Standards rejection (e.g. \"does not violate our policies\") is "
            "a moderation outcome — not a lawful Article 17(3) exemption. This formal request "
            "must be processed by Meta's data protection function under UK GDPR."
        )
        return "\n".join(lines)

    if fb.get("reported_to_meta"):
        return (
            "I reported this content through Meta's in-app reporting tools. Meta responded "
            "that the content \"does not go against Community Standards\" and declined removal "
            "(support message, August 2026 — screenshot attached). That moderation outcome "
            "does NOT satisfy Article 17 UK GDPR and does NOT constitute a valid refusal under "
            "Article 12(4). I also reported the group for hate speech; group-level moderation "
            "is separate from my personal erasure rights."
        )

    return (
        "I am submitting this Article 17 request without reliance on in-app reporting alone."
    )


def group_pattern_block(config: dict[str, Any]) -> str:
    fb = config["case"].get("facebook", {})
    pattern = fb.get("group_pattern", "").strip()
    if pattern:
        return pattern

    group = fb.get("group_name", "")
    if "AreWeDatingTheSameGuy" in group or "AWDTSG" in group.upper():
        return (
            f'The group "{group}" follows a known pattern of publishing men\'s photographs '
            "and names soliciting unverified \"red flag\" allegations. The same format has "
            "harmed multiple private individuals. That systemic pattern reinforces that this "
            "processing lacks legitimate purpose and causes disproportionate harm, but my "
            "request concerns erasure of MY personal data only."
        )
    return ""


def search_queries_block(config: dict[str, Any]) -> str:
    queries = config.get("monitor", {}).get("search_queries", [])
    if not queries:
        return "  (Add monitor.search_queries in config.yaml and run: python3 main.py monitor)"
    lines = []
    for q in queries:
        encoded = quote_plus(q)
        lines.append(f"  - Google search: https://www.google.com/search?q={encoded}")
    lines.append("  - Add any result URLs from output/search-monitor-*.txt after running monitor")
    return "\n".join(lines)

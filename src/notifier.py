"""Slack notifications via incoming webhook."""

from __future__ import annotations

from typing import Any

import requests


def slack_notify(webhook_url: str, text: str, *, blocks: list[dict[str, Any]] | None = None) -> bool:
    if not webhook_url:
        return False
    payload: dict[str, Any] = {"text": text}
    if blocks:
        payload["blocks"] = blocks
    try:
        resp = requests.post(webhook_url, json=payload, timeout=15)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def format_hit_message(subject: str, hits: list[dict[str, Any]]) -> str:
    lines = [f"*Removal monitor — {subject}*", f"Found {len(hits)} new potentially harmful URL(s):"]
    for hit in hits[:10]:
        lines.append(f"• <{hit.get('url', '')}|{hit.get('domain', 'link')}> — {hit.get('title', '')[:60]}")
    if len(hits) > 10:
        lines.append(f"_…and {len(hits) - 10} more_")
    return "\n".join(lines)


def format_escalation_message(track: str, round_num: int, package_path: str, auto_sent: bool) -> str:
    sent = " (email sent automatically)" if auto_sent else " (review package before sending)"
    return (
        f"*Campaign escalated — {track.upper()} round {round_num}*{sent}\n"
        f"Package: `{package_path}`"
    )


def format_daily_summary(summary: dict[str, Any]) -> str:
    status = summary.get("campaign_status", "unknown")
    removed = summary.get("removed", False)
    new_urls = summary.get("new_url_count", 0)
    image_hits = summary.get("image_hit_count", 0)
    escalated = summary.get("escalations", [])
    emoji = "✅" if removed else "🔍"
    lines = [
        f"{emoji} *Daily removal scan — {summary.get('subject', 'Unknown')}*",
        f"Campaign: {status}" + (" — *CONTENT REMOVED*" if removed else ""),
        f"New search hits: {new_urls} | Image matches: {image_hits}",
    ]
    if escalated:
        lines.append("Escalations today: " + ", ".join(escalated))
    if summary.get("errors"):
        lines.append("Errors: " + "; ".join(summary["errors"][:3]))
    return "\n".join(lines)

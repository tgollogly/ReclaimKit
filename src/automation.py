"""Daily automated monitor, escalation, optional email, Slack alerts."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.campaign import (
    generate_next_package,
    generate_round_package,
    init_campaign,
    load_state,
    record_no_response,
    record_sent,
    save_state,
)
from src.email_sender import send_letter_email
from src.escalation_letters import META_ROUNDS, TRACKS
from src.image_search import run_image_search
from src.monitor import monitor_search_results
from src.notifier import (
    format_daily_summary,
    format_escalation_message,
    format_hit_message,
    slack_notify,
)

SEEN_URLS_FILENAME = "seen_urls.json"


def _seen_urls_path(output_dir: Path) -> Path:
    return output_dir / "campaign" / SEEN_URLS_FILENAME


def _load_seen_urls(output_dir: Path) -> set[str]:
    path = _seen_urls_path(output_dir)
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("urls", []))


def _save_seen_urls(output_dir: Path, urls: set[str]) -> None:
    path = _seen_urls_path(output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"urls": sorted(urls), "updated_at": datetime.now(timezone.utc).isoformat()}, indent=2),
        encoding="utf-8",
    )


def _days_since_sent(state: dict[str, Any], track: str) -> int | None:
    events = [e for e in state["tracks"][track]["events"] if e["type"] == "sent"]
    if not events:
        return None
    last = events[-1]
    try:
        ts = datetime.fromisoformat(last["timestamp"].replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - ts).days
    except (KeyError, ValueError):
        return None


def _check_campaign_escalation(config: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    """Auto-escalate Meta track if enough days passed since last send."""
    auto_cfg = config.get("automation", {})
    if not auto_cfg.get("auto_escalate", False):
        return []

    if state.get("removed"):
        return []

    meta_days = auto_cfg.get("meta_escalation_days", 7)
    days = _days_since_sent(state, "meta")
    if days is None:
        return []

    current = state["tracks"]["meta"]["round"]
    maximum = state["tracks"]["meta"]["max_round"]
    if days < meta_days or current >= maximum:
        return []

    record_no_response(state, "meta", days)
    next_round = current + 1
    out = Path(config["evidence"]["output_dir"])
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    package_dir = out / f"auto-escalation-{timestamp}"
    package_dir.mkdir(parents=True, exist_ok=True)
    generate_round_package(config, state, "meta", next_round, package_dir)

    result = {
        "track": "meta",
        "round": next_round,
        "package_dir": str(package_dir),
        "email_sent": False,
    }

    if auto_cfg.get("auto_send_emails", False):
        filename, _, send_to, _ = META_ROUNDS[next_round]
        letter_path = package_dir / f"round-{next_round:02d}-meta" / filename
        body = letter_path.read_text(encoding="utf-8")
        subject_line = body.split("\n")[2].replace("Subject: ", "") if "Subject:" in body else f"GDPR R{next_round}"
        to_addr = "privacy@facebook.com"
        email_result = send_letter_email(
            config,
            to_address=to_addr,
            subject=subject_line,
            body=body,
            letter_path=letter_path,
        )
        result["email_sent"] = email_result.get("sent", False)
        result["email_detail"] = email_result
        if email_result.get("sent"):
            record_sent(state, "meta", next_round)

    return [result]


def run_daily_automation(config: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    """Full daily job: search monitor, image search, escalation, Slack."""
    auto_cfg = config.get("automation", {})
    webhook = auto_cfg.get("slack_webhook_url", "")
    out_dir = Path(config["evidence"]["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "subject": config["subject"]["full_name"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "new_url_count": 0,
        "image_hit_count": 0,
        "escalations": [],
        "errors": [],
        "removed": False,
        "campaign_status": "unknown",
    }

    # Campaign state
    try:
        state = load_state(out_dir / "campaign" / "state.json")
    except FileNotFoundError:
        state = init_campaign(config, out_dir)
        if auto_cfg.get("auto_start_campaign", True) and not dry_run:
            generate_next_package(config, state)

    summary["removed"] = state.get("removed", False)
    summary["campaign_status"] = state.get("status", "active")

    if summary["removed"]:
        if webhook and not dry_run:
            slack_notify(webhook, f"✅ Campaign complete — content removed for {summary['subject']}")
        return summary

    # Text search monitor
    new_hits: list[dict[str, Any]] = []
    try:
        monitor_report = monitor_search_results(config)
        report_path = out_dir / f"auto-search-{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
        report_path.write_text(json.dumps(monitor_report, indent=2), encoding="utf-8")

        seen = _load_seen_urls(out_dir)
        for item in monitor_report.get("results", []):
            url = item.get("url", "")
            if not url or url in seen:
                continue
            if item.get("potentially_harmful") or _is_facebook_or_awdtsg(url):
                new_hits.append(item)
                seen.add(url)
        if not dry_run:
            _save_seen_urls(out_dir, seen)
        summary["new_url_count"] = len(new_hits)

        if new_hits and webhook and not dry_run:
            slack_notify(webhook, format_hit_message(summary["subject"], new_hits))
    except Exception as exc:  # noqa: BLE001
        summary["errors"].append(f"search monitor: {exc}")

    # Reverse image search
    try:
        image_report = run_image_search(config)
        img_path = out_dir / f"auto-image-{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
        img_path.write_text(json.dumps(image_report, indent=2), encoding="utf-8")

        img_hits = [r for r in image_report.get("results", []) if r.get("url") and "error" not in r]
        seen = _load_seen_urls(out_dir)
        fresh_img: list[dict[str, Any]] = []
        for hit in img_hits:
            url = hit["url"]
            if url not in seen:
                fresh_img.append(hit)
                if not dry_run:
                    seen.add(url)
        if not dry_run:
            _save_seen_urls(out_dir, seen)
        summary["image_hit_count"] = len(fresh_img)

        if fresh_img and webhook and not dry_run:
            slack_notify(
                webhook,
                format_hit_message(summary["subject"] + " (image match)", fresh_img),
            )
    except Exception as exc:  # noqa: BLE001
        summary["errors"].append(f"image search: {exc}")

    # Auto-escalation
    if not dry_run:
        try:
            escalations = _check_campaign_escalation(config, state)
            save_state(state, out_dir / "campaign" / "state.json")
            for esc in escalations:
                summary["escalations"].append(f"{esc['track']} r{esc['round']}")
                if webhook:
                    slack_notify(
                        webhook,
                        format_escalation_message(
                            esc["track"],
                            esc["round"],
                            esc["package_dir"],
                            esc.get("email_sent", False),
                        ),
                    )
        except Exception as exc:  # noqa: BLE001
            summary["errors"].append(f"escalation: {exc}")

    # Daily summary to Slack
    if webhook and not dry_run:
        slack_notify(webhook, format_daily_summary(summary))

    log_path = out_dir / "automation-log.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(summary) + "\n")

    return summary


def _is_facebook_or_awdtsg(url: str) -> bool:
    lower = url.lower()
    return any(x in lower for x in ("facebook.com", "awdtsg", "arewedatingthesameguy"))

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None  # type: ignore[misc, assignment]


HARMFUL_KEYWORDS = [
    "facebook",
    "arewedatingthesameguy",
    "red flags",
    "gollogly",
]


def monitor_search_results(config: dict[str, Any]) -> dict[str, Any]:
    """Search public web for indexed mentions (does not access Facebook directly)."""
    if DDGS is None:
        raise ImportError("Install dependencies: pip install -r requirements.txt")

    monitor_cfg = config.get("monitor", {})
    queries = monitor_cfg.get("search_queries", ['"Thomas Gollogly"'])
    region = monitor_cfg.get("region", "uk-en")

    all_results: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    with DDGS() as ddgs:
        for query in queries:
            try:
                results = list(ddgs.text(query, region=region, max_results=15))
            except Exception as exc:  # noqa: BLE001
                all_results.append(
                    {"query": query, "error": str(exc), "results": []}
                )
                continue

            query_hits: list[dict[str, Any]] = []
            for item in results:
                url = item.get("href") or item.get("link") or ""
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                hit = {
                    "url": url,
                    "title": item.get("title", ""),
                    "snippet": item.get("body", item.get("snippet", "")),
                    "domain": urlparse(url).netloc,
                    "potentially_harmful": _is_potentially_harmful(item, config),
                }
                query_hits.append(hit)
                all_results.append({"query": query, **hit})

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "subject": config["subject"]["full_name"],
        "queries_run": queries,
        "region": region,
        "total_unique_urls": len(seen_urls),
        "results": all_results,
        "action_items": _monitor_action_items(all_results),
    }
    return report


def _is_potentially_harmful(item: dict[str, Any], config: dict[str, Any]) -> bool:
    text = " ".join(
        [
            item.get("title", ""),
            item.get("body", item.get("snippet", "")),
            item.get("href", item.get("link", "")),
        ]
    ).lower()
    name_parts = config["subject"]["full_name"].lower().split()
    has_name = all(part in text for part in name_parts if len(part) > 2)
    has_harmful = any(kw in text for kw in HARMFUL_KEYWORDS)
    return has_name and (has_harmful or "facebook" in text)


def _monitor_action_items(results: list[dict[str, Any]]) -> list[str]:
    harmful = [r for r in results if r.get("potentially_harmful")]
    items = []
    if not harmful:
        items.append(
            "No obviously harmful indexed results found in this scan. Re-run weekly."
        )
    else:
        items.append(
            f"Found {len(harmful)} potentially harmful indexed URL(s). "
            "Add each URL to Google defamation/personal info removal requests."
        )
        for hit in harmful:
            items.append(f"  → Review and request removal: {hit.get('url', 'N/A')}")
    items.append(
        "Monitor does not access Facebook directly. Private group posts may not appear in search."
    )
    return items


def write_monitor_report(config: dict[str, Any], output_dir: Path | None = None) -> Path:
    report = monitor_search_results(config)
    out = output_dir or Path(config["evidence"]["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out / f"search-monitor-{timestamp}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    summary = out / f"search-monitor-{timestamp}.txt"
    lines = [
        "SEARCH MONITOR REPORT",
        "=" * 60,
        f"Scanned at: {report['generated_at_utc']}",
        f"Unique URLs found: {report['total_unique_urls']}",
        "",
        "ACTION ITEMS:",
    ]
    lines.extend(report["action_items"])
    lines.extend(["", "ALL RESULTS:"])
    for item in report["results"]:
        if "error" in item:
            lines.append(f"  Query '{item['query']}': ERROR — {item['error']}")
        elif "url" in item:
            flag = " ⚠ HARMFUL?" if item.get("potentially_harmful") else ""
            lines.append(f"  [{item['query']}] {item['url']}{flag}")
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path

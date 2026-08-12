"""Reverse image search via optional paid APIs (SerpAPI Google Lens, TinEye)."""

from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from typing import Any

import requests

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}


def find_reference_image(config: dict[str, Any]) -> Path | None:
    cfg = config.get("automation", {}).get("image_search", {})
    explicit = cfg.get("reference_image")
    if explicit:
        path = Path(explicit)
        if path.exists():
            return path
    evidence_dir = Path(config["evidence"]["screenshots_dir"])
    if not evidence_dir.exists():
        return None
    for path in sorted(evidence_dir.iterdir()):
        if path.suffix.lower() in IMAGE_EXTENSIONS and path.is_file():
            return path
    return None


def run_image_search(config: dict[str, Any]) -> dict[str, Any]:
    cfg = config.get("automation", {}).get("image_search", {})
    ref = find_reference_image(config)
    report: dict[str, Any] = {
        "reference_image": str(ref) if ref else None,
        "provider": cfg.get("provider", "none"),
        "results": [],
        "errors": [],
    }
    if not ref:
        report["errors"].append("No reference image in evidence/screenshots/")
        return report

    provider = (cfg.get("provider") or "none").lower()
    if provider == "serpapi":
        report["results"] = _serpapi_google_lens(ref, cfg.get("serpapi_key", ""))
    elif provider == "tineye":
        report["results"] = _tineye_search(ref, cfg.get("tineye_api_key", ""))
    elif provider == "none":
        report["errors"].append(
            "Image search disabled. Set automation.image_search.provider to serpapi or tineye "
            "and add API key — see deploy/README.md"
        )
    else:
        report["errors"].append(f"Unknown provider: {provider}")

    report["result_count"] = len(report["results"])
    return report


def _serpapi_google_lens(image_path: Path, api_key: str) -> list[dict[str, Any]]:
    if not api_key:
        return []
    with image_path.open("rb") as handle:
        b64 = base64.b64encode(handle.read()).decode("ascii")
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_lens",
        "api_key": api_key,
        "url": f"data:image/jpeg;base64,{b64}",
    }
    # SerpAPI Google Lens may require public URL — try file upload alternative
    try:
        resp = requests.get(url, params={"engine": "google_lens", "api_key": api_key}, timeout=30)
        if resp.status_code != 200:
            # Fallback: upload to serpapi with image file
            with image_path.open("rb") as img:
                resp = requests.post(
                    "https://serpapi.com/search.json",
                    data={"engine": "google_lens", "api_key": api_key},
                    files={"image": img},
                    timeout=60,
                )
        data = resp.json()
        if "error" in data:
            return [{"error": data["error"], "url": ""}]
        results: list[dict[str, Any]] = []
        for item in data.get("visual_matches", [])[:20]:
            results.append({
                "url": item.get("link", ""),
                "title": item.get("title", ""),
                "source": item.get("source", ""),
                "provider": "serpapi_google_lens",
            })
        for item in data.get("exact_matches", [])[:10]:
            results.append({
                "url": item.get("link", ""),
                "title": "exact match",
                "source": item.get("source", ""),
                "provider": "serpapi_google_lens",
            })
        return results
    except requests.RequestException as exc:
        return [{"error": str(exc), "url": ""}]


def _tineye_search(image_path: Path, api_key: str) -> list[dict[str, Any]]:
    if not api_key:
        return []
    url = "https://api.tineye.com/rest/search/"
    try:
        with image_path.open("rb") as handle:
            resp = requests.post(
                url,
                headers={"X-API-Key": api_key},
                files={"image": handle},
                timeout=60,
            )
        data = resp.json()
        if data.get("status") != "ok":
            return [{"error": data.get("status", "tineye error"), "url": ""}]
        results: list[dict[str, Any]] = []
        for match in data.get("results", {}).get("matches", [])[:25]:
            for backlink in match.get("backlinks", [])[:3]:
                results.append({
                    "url": backlink.get("url", ""),
                    "title": backlink.get("url", ""),
                    "source": "tineye",
                    "provider": "tineye",
                    "score": match.get("score"),
                })
        return results
    except requests.RequestException as exc:
        return [{"error": str(exc), "url": ""}]


def image_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

"""Reverse image search via optional paid APIs (SerpAPI Google Lens, TinEye)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import requests

from src.security import resolve_under

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
MAX_IMAGE_BYTES = 20 * 1024 * 1024
REQUEST_TIMEOUT = 60


def find_reference_image(config: dict[str, Any]) -> Path | None:
    cfg = config.get("automation", {}).get("image_search", {})
    evidence_dir = Path(config["evidence"]["screenshots_dir"]).resolve()

    explicit = cfg.get("reference_image")
    if explicit:
        try:
            if Path(explicit).is_absolute():
                path = Path(explicit).resolve()
                if not str(path).startswith(str(evidence_dir)):
                    return None
            else:
                path = resolve_under(evidence_dir, explicit)
            if path.is_file() and not path.is_symlink():
                return _validate_image(path)
        except (ValueError, OSError):
            return None

    if not evidence_dir.exists():
        return None
    for path in sorted(evidence_dir.iterdir()):
        if path.is_file() and not path.is_symlink() and path.suffix.lower() in IMAGE_EXTENSIONS:
            try:
                return _validate_image(path)
            except ValueError:
                continue
    return None


def _validate_image(path: Path) -> Path:
    size = path.stat().st_size
    if size <= 0 or size > MAX_IMAGE_BYTES:
        raise ValueError(f"Image size out of range: {path.name}")
    return path


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
            "Image search disabled. Set automation.image_search.provider to serpapi or tineye"
        )
    else:
        report["errors"].append(f"Unknown provider: {provider}")

    report["result_count"] = len([r for r in report["results"] if r.get("url")])
    return report


def _serpapi_google_lens(image_path: Path, api_key: str) -> list[dict[str, Any]]:
    if not api_key:
        return [{"error": "Missing serpapi_key", "url": ""}]
    try:
        with image_path.open("rb") as img:
            resp = requests.post(
                "https://serpapi.com/search.json",
                data={"engine": "google_lens", "api_key": api_key},
                files={"image": (image_path.name, img, "application/octet-stream")},
                timeout=REQUEST_TIMEOUT,
            )
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            return [{"error": data["error"], "url": ""}]
        results: list[dict[str, Any]] = []
        for item in data.get("visual_matches", [])[:20]:
            link = item.get("link", "")
            if link:
                results.append({
                    "url": link,
                    "title": item.get("title", ""),
                    "source": item.get("source", ""),
                    "provider": "serpapi_google_lens",
                })
        return results
    except (requests.RequestException, ValueError) as exc:
        return [{"error": str(exc), "url": ""}]


def _tineye_search(image_path: Path, api_key: str) -> list[dict[str, Any]]:
    if not api_key:
        return [{"error": "Missing tineye_api_key", "url": ""}]
    try:
        with image_path.open("rb") as handle:
            resp = requests.post(
                "https://api.tineye.com/rest/search/",
                headers={"X-API-Key": api_key},
                files={"image": handle},
                timeout=REQUEST_TIMEOUT,
            )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "ok":
            return [{"error": data.get("status", "tineye error"), "url": ""}]
        results: list[dict[str, Any]] = []
        for match in data.get("results", {}).get("matches", [])[:25]:
            for backlink in match.get("backlinks", [])[:3]:
                url = backlink.get("url", "")
                if url:
                    results.append({
                        "url": url,
                        "title": url,
                        "source": "tineye",
                        "provider": "tineye",
                        "score": match.get("score"),
                    })
        return results
    except (requests.RequestException, ValueError) as exc:
        return [{"error": str(exc), "url": ""}]


def image_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()

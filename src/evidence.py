from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _image_metadata(path: Path) -> dict[str, Any]:
    meta: dict[str, Any] = {"filename": path.name, "size_bytes": path.stat().st_size}
    try:
        with Image.open(path) as img:
            meta["width"] = img.width
            meta["height"] = img.height
            meta["format"] = img.format
            exif = img.getexif()
            if exif:
                meta["exif_tag_count"] = len(exif)
    except Exception as exc:  # noqa: BLE001 - preserve evidence even if corrupt
        meta["image_read_error"] = str(exc)
    return meta


def build_evidence_pack(config: dict[str, Any]) -> Path:
    """Copy screenshots into a timestamped evidence pack with integrity hashes."""
    evidence_cfg = config["evidence"]
    source_dir = Path(evidence_cfg["screenshots_dir"])
    output_root = Path(evidence_cfg["output_dir"])
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pack_dir = output_root / f"evidence-pack-{timestamp}"
    files_dir = pack_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    if not source_dir.exists():
        source_dir.mkdir(parents=True, exist_ok=True)
        readme = source_dir / "README.txt"
        readme.write_text(
            "Place your screenshots of the Facebook post and comments here.\n"
            "Supported formats: PNG, JPG, JPEG, WEBP, GIF, BMP\n",
            encoding="utf-8",
        )
        raise FileNotFoundError(
            f"No screenshots found. Created {source_dir}. Add your screenshots and re-run."
        )

    entries: list[dict[str, Any]] = []
    copied = 0
    for path in sorted(source_dir.iterdir()):
        if not path.is_file() or path.is_symlink():
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        dest = files_dir / path.name
        shutil.copy2(path, dest)
        file_hash = _sha256_file(dest)
        entry = {
            "original_path": str(path.resolve()),
            "stored_as": dest.name,
            "sha256": file_hash,
            **_image_metadata(dest),
        }
        entries.append(entry)
        copied += 1

    if copied == 0:
        raise FileNotFoundError(
            f"No image files in {source_dir}. Add screenshots of the post and comments."
        )

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "subject": config["subject"]["full_name"],
        "facebook_group": config["case"]["facebook"]["group_name"],
        "post_date": config["case"]["facebook"]["post_date"],
        "file_count": copied,
        "files": entries,
        "integrity_note": (
            "SHA-256 hashes prove files were not altered after capture. "
            "Preserve originals on your device; share this pack with solicitors or police."
        ),
    }

    manifest_path = pack_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    summary_path = pack_dir / "EVIDENCE_SUMMARY.txt"
    summary_path.write_text(_evidence_summary(manifest, config), encoding="utf-8")

    return pack_dir


def _evidence_summary(manifest: dict[str, Any], config: dict[str, Any]) -> str:
    fb = config["case"]["facebook"]
    lines = [
        "EVIDENCE PACK SUMMARY",
        "=" * 60,
        f"Subject: {manifest['subject']}",
        f"Generated (UTC): {manifest['generated_at_utc']}",
        f"Facebook group: {fb['group_name']}",
        f"Post date: {fb['post_date']}",
        f"Post caption: {fb['post_caption']}",
        "",
        "FILES (SHA-256 for court/solicitor use):",
    ]
    for item in manifest["files"]:
        lines.append(f"  - {item['stored_as']}: {item['sha256']}")
    lines.extend(
        [
            "",
            "NEXT STEPS:",
            "  1. Do not edit these files after hashing.",
            "  2. Provide this folder to your solicitor or PSNI if reporting.",
            "  3. Keep originals on the device where you took the screenshots.",
        ]
    )
    return "\n".join(lines) + "\n"

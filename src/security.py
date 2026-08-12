"""Security helpers: path validation, input sanitization, safe defaults."""

from __future__ import annotations

import re
from pathlib import Path

MAX_REFUSAL_REASON_LEN = 4000
MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024  # 10 MB per file
MAX_TOTAL_ATTACHMENTS_BYTES = 25 * 1024 * 1024
SAFE_FILENAME = re.compile(r"^[a-zA-Z0-9._\- ]+$")
META_RECIPIENT = "privacy@facebook.com"


def resolve_under(base: Path, user_path: str | Path) -> Path:
    """Resolve user_path and ensure it stays under base (prevents path traversal)."""
    base_resolved = base.resolve()
    target = (base_resolved / user_path).resolve()
    if not str(target).startswith(str(base_resolved)):
        raise ValueError(f"Path escapes allowed directory: {user_path}")
    return target


def safe_output_path(config_output: str | Path, *parts: str) -> Path:
    """Build paths under configured output directory only."""
    root = Path(config_output).resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = root
    for part in parts:
        if part in ("", ".", "..") or ".." in part:
            raise ValueError(f"Invalid path segment: {part!r}")
        target = target / part
    target = target.resolve()
    if not str(target).startswith(str(root)):
        raise ValueError("Output path escapes configured output_dir")
    return target


def sanitize_filename(name: str) -> str:
    """Use basename only; reject path separators and suspicious names."""
    if any(sep in name for sep in ("/", "\\", "\x00")):
        raise ValueError(f"Invalid filename: {name!r}")
    base = Path(name).name
    if not base or base in (".", "..") or base.startswith("."):
        raise ValueError(f"Invalid filename: {name!r}")
    if not SAFE_FILENAME.match(base):
        raise ValueError(f"Filename contains unsafe characters: {base!r}")
    return base


def validate_email_address(addr: str) -> str:
    addr = addr.strip()
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", addr):
        raise ValueError(f"Invalid email address: {addr!r}")
    if len(addr) > 254:
        raise ValueError("Email address too long")
    return addr


def clamp_text(text: str, max_len: int) -> str:
    return text[:max_len] if len(text) > max_len else text


def is_safe_http_url(url: str) -> bool:
    lower = url.lower()
    return lower.startswith("https://") or lower.startswith("http://")


def allowed_recipient(to_address: str) -> str:
    """Only permit known GDPR recipients for automated email."""
    addr = validate_email_address(to_address)
    allowed = {META_RECIPIENT, "dpo@facebook.com"}
    if addr.lower() not in allowed:
        raise ValueError(
            f"Automated email restricted to Meta DPO addresses, not {addr!r}"
        )
    return addr

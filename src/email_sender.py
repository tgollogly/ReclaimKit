"""Send GDPR / escalation letters via SMTP (optional automation)."""

from __future__ import annotations

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from src.security import (
    MAX_ATTACHMENT_BYTES,
    MAX_TOTAL_ATTACHMENTS_BYTES,
    allowed_recipient,
    resolve_under,
    sanitize_filename,
)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}


def send_letter_email(
    config: dict[str, Any],
    *,
    to_address: str,
    subject: str,
    body: str,
    letter_path: Path | None = None,
    attach_screenshots: bool = True,
) -> dict[str, Any]:
    smtp_cfg = config.get("automation", {}).get("smtp", {})
    if not smtp_cfg.get("enabled"):
        return {"sent": False, "reason": "SMTP disabled in config"}

    try:
        to_address = allowed_recipient(to_address)
    except ValueError as exc:
        return {"sent": False, "reason": str(exc)}

    host = smtp_cfg.get("host", "")
    port = int(smtp_cfg.get("port", 587))
    user = smtp_cfg.get("username", "")
    password = smtp_cfg.get("password", "")
    from_addr = smtp_cfg.get("from_email") or config["subject"]["email"]
    use_tls = smtp_cfg.get("use_tls", True)

    if not all([host, user, password, from_addr]):
        return {"sent": False, "reason": "Incomplete SMTP config"}

    if len(subject) > 998:
        subject = subject[:998]

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    total_bytes = 0
    if attach_screenshots:
        evidence_dir = Path(config["evidence"]["screenshots_dir"]).resolve()
        if evidence_dir.exists():
            for path in sorted(evidence_dir.iterdir()):
                if not path.is_file() or path.is_symlink():
                    continue
                if path.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                try:
                    safe_name = sanitize_filename(path.name)
                except ValueError:
                    continue
                size = path.stat().st_size
                if size > MAX_ATTACHMENT_BYTES:
                    continue
                if total_bytes + size > MAX_TOTAL_ATTACHMENTS_BYTES:
                    break
                with path.open("rb") as handle:
                    data = handle.read()
                part = MIMEApplication(data, Name=safe_name)
                part["Content-Disposition"] = f'attachment; filename="{safe_name}"'
                msg.attach(part)
                total_bytes += size

    if letter_path and letter_path.exists():
        try:
            letter_resolved = letter_path.resolve()
            output_root = Path(config["evidence"]["output_dir"]).resolve()
            if str(letter_resolved).startswith(str(output_root)):
                msg.attach(MIMEText(f"\n\nLetter file: {letter_path.name}", "plain"))
        except OSError:
            pass

    try:
        with smtplib.SMTP(host, port, timeout=30) as server:
            if use_tls:
                server.starttls()
            server.login(user, password)
            server.sendmail(from_addr, [to_address], msg.as_string())
        return {"sent": True, "to": to_address, "subject": subject}
    except smtplib.SMTPException as exc:
        return {"sent": False, "reason": str(exc)}

"""Send GDPR / escalation letters via SMTP (optional automation)."""

from __future__ import annotations

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

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

    host = smtp_cfg.get("host", "")
    port = int(smtp_cfg.get("port", 587))
    user = smtp_cfg.get("username", "")
    password = smtp_cfg.get("password", "")
    from_addr = smtp_cfg.get("from_email") or config["subject"]["email"]
    use_tls = smtp_cfg.get("use_tls", True)

    if not all([host, user, password, from_addr]):
        return {"sent": False, "reason": "Incomplete SMTP config"}

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    if letter_path and letter_path.exists():
        msg.attach(MIMEText(f"\n\n---\nAttached letter file: {letter_path.name}", "plain"))

    if attach_screenshots:
        evidence_dir = Path(config["evidence"]["screenshots_dir"])
        if evidence_dir.exists():
            for path in sorted(evidence_dir.iterdir()):
                if path.suffix.lower() in IMAGE_EXTENSIONS and path.is_file():
                    with path.open("rb") as handle:
                        part = MIMEApplication(handle.read(), Name=path.name)
                    part["Content-Disposition"] = f'attachment; filename="{path.name}"'
                    msg.attach(part)

    try:
        with smtplib.SMTP(host, port, timeout=30) as server:
            if use_tls:
                server.starttls()
            server.login(user, password)
            server.sendmail(from_addr, [to_address], msg.as_string())
        return {"sent": True, "to": to_address, "subject": subject}
    except smtplib.SMTPException as exc:
        return {"sent": False, "reason": str(exc)}

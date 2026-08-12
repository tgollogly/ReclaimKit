# VPS deployment

Run daily monitoring, Slack alerts, and optional auto-escalation on any Linux VPS or Docker host.

## What automation CAN do

| Feature | Automated? |
|---------|------------|
| Daily text search for your name | Yes |
| Daily reverse image search (SerpAPI/TinEye) | Yes (needs API key) |
| Slack notification on new hits | Yes |
| Auto-generate next escalation letter every 7 days | Yes |
| Auto-email Meta (`privacy@facebook.com`) | Optional (`auto_send_emails: true`) |
| Track campaign state | Yes |

## What automation CANNOT do

| Feature | Why |
|---------|-----|
| **Force-delete Facebook posts** | Only Meta can remove — no API for individuals |
| **Auto-submit Google forms** | Google has no public API; forms need manual/browser submit |
| **Scrape private Facebook groups** | Illegal / against ToS / requires login |
| **Guarantee removal** | Platforms decide; automation persists requests |

This is the same limitation Removify has — they also submit forms and emails, not magic deletes.

---

## Quick start (Docker on VPS)

```bash
git clone https://github.com/tgollogly/stop-assholes.git
cd stop-assholes
pip install -r requirements.txt
python3 main.py init
# Edit config.yaml — email, address, Slack webhook, optional API keys
# Add screenshots to evidence/screenshots/

python3 main.py campaign init
python3 main.py campaign sent --track meta --round 1

cd deploy
docker compose up -d --build
```

Logs: `output/cron.log` and `output/automation-log.jsonl`

---

## Quick start (cron, no Docker)

```bash
# On your VPS
crontab -e
# Add:
0 8 * * * cd /path/to/stop-assholes && /usr/bin/python3 main.py daemon once >> output/cron.log 2>&1
```

---

## Slack setup

1. https://api.slack.com/messaging/webhooks
2. Create incoming webhook for your channel
3. Paste URL into `config.yaml`:

```yaml
automation:
  slack_webhook_url: "https://hooks.slack.com/services/..."
```

Test: `python3 main.py daemon once --dry-run` then without `--dry-run`

---

## Reverse image search (daily photo scan)

Free search engines don't offer reliable reverse-image APIs. Use one of:

### SerpAPI (Google Lens) — recommended
- Sign up: https://serpapi.com/
- ```yaml
  automation:
    image_search:
      provider: serpapi
      serpapi_key: "your-key"
  ```

### TinEye
- https://tineye.com/api
- ```yaml
    image_search:
      provider: tineye
      tineye_api_key: "your-key"
  ```

Place your selfie in `evidence/screenshots/` (or set `reference_image`).

---

## Auto-email Meta (optional)

**Default is OFF.** When enabled, sends escalation letters to `privacy@facebook.com` via SMTP.

Gmail example:
```yaml
automation:
  auto_send_emails: true
  smtp:
    enabled: true
    host: smtp.gmail.com
    port: 587
    username: you@gmail.com
    password: "16-char-app-password"
    from_email: you@gmail.com
```

Use a Gmail [App Password](https://support.google.com/accounts/answer/185833), not your main password.

---

## Manual commands

```bash
python3 main.py daemon once          # run daily job now
python3 main.py daemon once --dry-run  # test without writes/emails
python3 main.py campaign status
```

---

## Security

- Never commit `config.yaml` (contains Slack webhook + SMTP passwords)
- Mount `config.yaml` read-only in Docker
- VPS should only be accessible to you (SSH keys, firewall)

# Auto-email setup (free Gmail)

Send Meta GDPR letters automatically from your VPS — **free** using a Gmail account and an **App Password**.

> **What auto-email does:** Sends escalation letters **to** `privacy@facebook.com` on schedule.  
> **What it does NOT do:** Read Meta's replies from your inbox. When Meta emails you back, check Gmail yourself and run the matching CLI command (see [When Meta replies](#when-meta-replies-you-still-act)).

---

## What gets automated

| Automated | Manual |
|-----------|--------|
| Daily monitor + Slack alerts | Reading Meta's reply emails |
| Generate next letter after 7 days silence | Pasting Google form submissions |
| **Optional:** SMTP send to Meta | Recording `campaign refused` if Meta says no |
| Attach screenshots from `evidence/screenshots/` | Sending passport/ID if Meta asks |

Enable in `config.yaml`:

```yaml
automation:
  enabled: true
  auto_escalate: true
  meta_escalation_days: 7
  auto_send_emails: true      # turn ON after SMTP tested
  smtp:
    enabled: true
    host: smtp.gmail.com
    port: 587
    use_tls: true
    username: your.name@gmail.com
    from_email: your.name@gmail.com
    password: ""               # use .env — see below
```

---

## Step 1 — Use a dedicated Gmail address

1. Create **your.name.reclaim@gmail.com** (or use existing Gmail)
2. Use the **same address** in `config.yaml` → `subject.email` and `smtp.from_email`
3. Meta replies go to this inbox — check it weekly

**Free:** Gmail costs nothing. No paid SMTP service required.

---

## Step 2 — Create a Google App Password

Google blocks normal passwords for SMTP. You need a 16-character **App Password**.

1. Enable **2-Step Verification** on the Google account:  
   https://myaccount.google.com/security
2. Go to **App passwords**:  
   https://myaccount.google.com/apppasswords
3. Create app: name it `ReclaimKit VPS`
4. Copy the 16-character password (e.g. `abcd efgh ijkl mnop`)

---

## Step 3 — Store password securely (not in config.yaml)

```bash
cp .env.example .env
nano .env
```

```bash
RECLAIMKIT_SMTP_PASSWORD=abcdefghijklmnop    # no spaces
RECLAIMKIT_SLACK_WEBHOOK=https://hooks.slack.com/...
```

Load before running:

```bash
export $(grep -v '^#' .env | xargs)
```

On Docker VPS, uncomment in `deploy/docker-compose.yml`:

```yaml
env_file:
  - ../.env
```

`src/config.py` injects `RECLAIMKIT_SMTP_PASSWORD` into `automation.smtp.password` automatically.

---

## Step 4 — Send Round 1 manually first

Auto-email only sends **escalation rounds** after Round 1 is recorded. Always:

```bash
python3 main.py campaign init
# Email Round 1 yourself OR test SMTP once manually
python3 main.py campaign sent --track meta --round 1
```

---

## Step 5 — Test SMTP before enabling automation

Create a one-line test (from repo root):

```bash
export $(grep -v '^#' .env | xargs)
python3 -c "
from src.config import load_config
from src.email_sender import send_letter_email
cfg = load_config('config.yaml')
cfg['automation']['smtp']['enabled'] = True
r = send_letter_email(
    cfg,
    to_address='privacy@facebook.com',
    subject='TEST - ignore - ReclaimKit SMTP check',
    body='SMTP test only. Please ignore.',
    attach_screenshots=False,
)
print(r)
"
```

Expected: `{'sent': True, ...}`

If it fails:
- Check App Password (no spaces in `.env`)
- Check 2-Step Verification enabled
- Try port 587 + `use_tls: true`

---

## Step 6 — Enable auto-send on VPS

```bash
# config.yaml
automation:
  auto_send_emails: true
  smtp:
    enabled: true

cd deploy && docker compose up -d --build
```

Daily cron runs `python3 main.py daemon once` which:
1. Monitors Google for your name
2. After 7 days since last send → generates next Meta letter
3. If `auto_send_emails: true` → emails `privacy@facebook.com`
4. Records send in `output/campaign/state.json`
5. Slack notification

Logs: `output/cron.log`, `output/automation-log.jsonl`

---

## When Meta replies (you still act)

ReclaimKit **cannot read your Gmail inbox** (by design — safer, simpler).

When Meta emails you:

| Meta says | You run |
|-----------|---------|
| "Content removed" | `python3 main.py campaign success` |
| "Does not violate..." / refusal | `python3 main.py campaign refused --track meta --reason "paste their reply"` |
| "We need ID" | Reply manually with passport — do not automate |
| "Received your request" | Wait — no action yet |
| No reply after 7 days | Daemon auto-escalates OR `python3 main.py campaign no-response --track meta` |

**Tip:** Create a Gmail filter: from `facebook.com` OR `meta.com` → label `ReclaimKit` → star.

---

## Alternative free SMTP providers

| Provider | SMTP host | Notes |
|----------|-----------|-------|
| **Gmail** | smtp.gmail.com:587 | Recommended — App Password |
| **Outlook.com** | smtp-mail.outlook.com:587 | App password if 2FA on |
| **Proton Mail** | Paid bridge required | Not free for SMTP |

---

## Security checklist

- [ ] App Password only — never your main Google password
- [ ] `.env` in `.gitignore` (already is)
- [ ] VPS SSH keys only
- [ ] `auto_send_emails: false` until SMTP test passes
- [ ] Same email in `subject.email` and `smtp.from_email`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `SMTP disabled` | Set `automation.smtp.enabled: true` |
| `Incomplete SMTP config` | Fill username, from_email, RECLAIMKIT_SMTP_PASSWORD |
| `535 Authentication failed` | Regenerate App Password |
| Email sent but no Meta reply | Normal — wait up to 1 month GDPR deadline |
| Auto-send didn't fire | Check `campaign sent` recorded; need 7+ days since last send |

Run: `python3 main.py doctor` and `./scripts/audit.sh`

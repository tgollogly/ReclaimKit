# Stop Assholes — Online Harassment Response Toolkit (UK/NI)

Removal-focused toolkit: **get the post taken down → delist from Google → close Facebook**. No police required.

## What this does

| Command | Purpose |
|---------|---------|
| `python3 main.py init` | Create `config.yaml` and evidence folders |
| `python3 main.py letters` | Generate Meta GDPR + Google removal letter drafts |
| `python3 main.py evidence` | Hash and package screenshots (for ICO/Meta if needed) |
| `python3 main.py monitor` | Scan public search for indexed harmful URLs |
| `python3 main.py guide` | Removal-only action guide |
| `python3 main.py close` | Checklist to close Facebook after removal |
| `python3 main.py all` | Run the full workflow |

## Quick start

```bash
pip install -r requirements.txt
python3 main.py init
# Edit config.yaml — email, address, Facebook post URL
# Copy screenshots into evidence/screenshots/
python3 main.py all
python3 main.py close   # read before deleting Facebook
```

## Your plan (no police)

1. **Submit Meta GDPR request today** — email `privacy@facebook.com` with generated letter
2. **Escalate if ignored** — https://www.facebook.com/help/contact/571927962827151
3. **Google delisting** — if anything shows in search (`python3 main.py monitor`)
4. **Wait up to 1 month** for Meta's GDPR response
5. **If Meta refuses** → ICO complaint (free, no police): https://ico.org.uk/make-a-complaint/
6. **Confirm post is gone** → close Facebook (`python3 main.py close`)

**Important:** Deleting Facebook does **not** remove the group post. Submit the GDPR request **before** you close your account, and keep your screenshots locally.

## What this cannot do

No software can instantly wipe content from the internet. Meta has up to **1 month** to respond to GDPR requests. Google only hides URLs from search — it does not delete Facebook posts.

## If Meta refuses (still no police)

Use the **ICO** (Information Commissioner's Office) — 0303 123 1113 — with your evidence pack and proof you emailed Meta. That is the civil data-protection route, not a criminal one.

---

*Information and templates only — not legal advice.*

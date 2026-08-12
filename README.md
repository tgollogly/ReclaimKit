# Stop Assholes — Multi-Round Removal Campaign (UK/NI)

Automated **escalation campaign** to remove harmful Facebook content and Google search results. Generates professionally worded legal letters across **multiple rounds** — each refusal or silence triggers the next, stronger letter until removal or ICO enforcement.

**No solicitor. No police.**

## How it works

```bash
pip install -r requirements.txt
python3 main.py init          # create config.yaml
# Edit config.yaml — your real email, address, phone
# Add screenshots to evidence/screenshots/

python3 main.py campaign init # round 1: Meta GDPR + Google
# → Send letters from output/campaign-package-*/

python3 main.py campaign sent --track meta --round 1

# 7 days, no removal?
python3 main.py campaign no-response --track meta

# Meta explicitly refused?
python3 main.py campaign refused --track meta --reason "They said..."

# Check progress anytime
python3 main.py campaign status

# Content gone?
python3 main.py campaign success
python3 main.py close
```

## Escalation rounds (automatic)

### Meta track (6 rounds)

| Round | Letter | When |
|-------|--------|------|
| 1 | UK GDPR Article 17 — formal erasure request | Day 0 — **start here** |
| 2 | Article 12(3) deadline reminder | 7 days, no response |
| 3 | Trust & Safety + Community Standards | 14 days |
| 4 | Formal rebuttal of refusal | Meta refuses |
| 5 | Final notice before ICO | 28 days |
| 6 | Post-ICO continued non-compliance | After ICO complaint |

### Google track (3 rounds)

| Round | Letter | When |
|-------|--------|------|
| 1 | Defamation delisting (UK) | Day 0 (parallel with Meta R1) |
| 2 | Personal info / doxxing form | Day 7 |
| 3 | Resubmission with Meta/ICO history | Day 30 |

### ICO track (1 round)

| Round | Letter | When |
|-------|--------|------|
| 1 | Full ICO complaint against Meta | After Meta round 4+ or 30 days |

Each letter includes a **case reference** (e.g. `TG-ER-THOMAS-GOLLO-META-R1`) — quote it in every email.

## Commands

| Command | Purpose |
|---------|---------|
| `campaign init` | Start campaign, generate round 1 |
| `campaign sent --track meta --round N` | Record that you sent round N |
| `campaign refused --track meta --reason "..."` | Record refusal → auto-generates next round |
| `campaign no-response --track meta` | No reply in 7 days → next round |
| `campaign next` | Generate next escalation package |
| `campaign status` | Dashboard |
| `campaign success` | Mark removed |
| `evidence` | SHA-256 evidence pack for ICO |
| `monitor` | Find Google URLs to delist |
| `close` | Facebook closure checklist |
| `daemon once` | Daily VPS job (monitor + Slack + escalate) |

## VPS automation (24/7 on a server)

Deploy on any Linux VPS — daily scans + Slack pings. Full guide: **`deploy/README.md`**

```bash
# In config.yaml: slack_webhook_url + optional SerpAPI key for daily photo search
python3 main.py daemon once

# Docker — runs daily at 08:00 UTC
cd deploy && docker compose up -d --build
```

| Automated | Not possible |
|-----------|--------------|
| Daily name search | Force-delete Facebook |
| Daily reverse image search (API key) | Auto-submit Google web forms |
| Slack alerts on new URLs | Scrape private Facebook groups |
| Next Meta letter every 7 days | Guaranteed removal |
| Optional email to Meta (off by default) | |

## Your post (pre-configured)

**URL:** https://www.facebook.com/groups/1054539240086174/posts/1252856073587822/

## What success looks like

1. Meta deletes post + comments (source removal)
2. Google delists any indexed URLs (search removal)
3. You close Facebook (`python3 main.py close`)
4. Monthly `monitor` for 3 months to catch re-indexing

## Honest limits

Software cannot force instant deletion. This tool matches what Removify and similar firms do — **formal requests, resubmissions, escalating legal pressure** — except you run it yourself for free. Persistence across rounds is what wins.

---

*Templates only — not legal advice.*

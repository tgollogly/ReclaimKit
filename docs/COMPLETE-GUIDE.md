# ReclaimKit — Complete User Guide

**Everything you need to know and do to remove harmful Facebook content, delist from Google, and close your account.**

| Field | Details |
|-------|---------|
| **For** | Anyone removing harmful social content |
| **Toolkit** | [ReclaimKit](https://github.com/tgollogly/ReclaimKit) |
| **Version** | August 2026 |
| **Legal basis** | Configurable — set `jurisdiction` in config.yaml for your country's privacy law |

> **Note:** For the latest test/deploy steps, see [README.md](../README.md). This guide provides extended detail.

> **Disclaimer:** ReclaimKit generates templates and tracks your campaign. It is **not legal advice** and is not affiliated with Meta, Google, or any paid removal service. Platform decisions are theirs; this guide helps you use official channels reputation firms use.

---

## Table of contents

1. [Will this work?](#1-will-this-work)
2. [Your situation at a glance](#2-your-situation-at-a-glance)
3. [What you need before you start](#3-what-you-need-before-you-start)
4. [Facebook login — what matters](#4-facebook-login--what-matters)
5. [Install ReclaimKit](#5-install-reclaimkit)
6. [Configure your case](#6-configure-your-case)
7. [Day 1 — start the campaign](#7-day-1--start-the-campaign)
8. [How to send Round 1 to Meta](#8-how-to-send-round-1-to-meta)
9. [Campaign tracks and timeline](#9-campaign-tracks-and-timeline)
10. [Google delisting (parallel track)](#10-google-delisting-parallel-track)
11. [Regulator complaint (if Meta refuses)](#11-regulator-complaint-if-meta-refuses)
12. [Closing Facebook after removal](#12-closing-facebook-after-removal)
13. [Daily monitoring and VPS automation](#13-daily-monitoring-and-vps-automation)
14. [All CLI commands reference](#14-all-cli-commands-reference)
15. [Windows 11 setup (Docker + WSL)](#15-windows-11-setup-docker--wsl)
16. [Costs and comparison to paid services](#16-costs-and-comparison-to-paid-services)
17. [FAQ](#17-faq)
18. [Troubleshooting](#18-troubleshooting)
19. [Support contacts (no police required)](#19-support-contacts-no-police-required)
20. [Checklist — print and tick off](#20-checklist--print-and-tick-off)
21. [Community Standards vs GDPR](#21-community-standards-vs-gdpr)
22. [Meta rejected your report — what now](#22-meta-rejected-your-report--what-now)
23. [Docker — does it auto-save?](#23-docker--does-it-auto-save)
24. [Unsure who posted? (safe wording)](#24-unsure-who-posted-safe-wording)
25. [Job hunting — will this hurt you?](#25-job-hunting--will-this-hurt-you)
26. [How long until content is erased?](#26-how-long-until-content-is-erased)
27. [Cheap VPS for automation + free AI](#27-cheap-vps-for-automation--free-ai)

---

## 1. Will this work?

**Yes — this is a proven, legitimate process.** Paid reputation firms (Removify, Erase.com, etc.) charge **£400–£2,000 per item** to submit the **same** GDPR emails, Meta escalation forms, and Google delisting requests that ReclaimKit generates for you.

### What ReclaimKit does

| Capability | Details |
|------------|---------|
| **6-round Meta escalation** | Privacy initial, then reminder, Trust & Safety, rebuttal, regulator notice, post-regulator |
| **3-round Google delisting** | Defamation, then personal info, then resubmit with case history |
| **1 regulator complaint letter** | Free authority pressure if Meta refuses after the response deadline |
| **Evidence pack** | Hashed screenshots + case summary for attachments |
| **Search monitoring** | Scans public web for indexed mentions of your name |
| **Image search** | Optional daily reverse-image scan (SerpAPI/TinEye) |
| **Slack alerts** | Notifies you when new harmful URLs appear |
| **VPS automation** | Daily monitor + optional auto-email to Meta (~£5/month) |

### What no software can do

| Limitation | Why |
|------------|-----|
| **Instant deletion** | Only Meta can remove Facebook posts — there is no public delete API |
| **Auto-submit Google forms** | Google has no API; you paste letter text into their web forms (~2 min each) |
| **Scrape private groups** | Illegal / against ToS; ReclaimKit uses your saved URL and screenshots |
| **Guarantee removal** | Platforms decide; persistence and proper legal framing improve success |
| **Deanonymize commenters** | Meta will not reveal identities without legal disclosure |

**Realistic expectation:** Platforms must respond within the deadline set by your jurisdiction (often **30 days**). Many cases resolve in Round 1–3. If the platform refuses, regulator complaints are free and often effective. Google delisting hides content from search even if a copy exists elsewhere.

---

## 2. Example case (fill in your own details in config.yaml)

| Field | Example placeholder |
|-------|---------------------|
| **Your name** | Set in `config.yaml` → `subject.full_name` |
| **Location** | Set in `config.yaml` → `subject.country` |
| **Harmful content** | Facebook group post with your photo + false allegations |
| **Group** | Set in `config.yaml` → `case.facebook.group_name` |
| **Post URL** | Set in `config.yaml` → `case.facebook.post_url` |
| **Already reported in-app?** | Set `reported_to_meta: true` if applicable |

### Alleged commenters

Add handles to `config.yaml` → `case.alleged_commenters`. ReclaimKit **cannot** identify real people behind anonymous names — only the platform can, via legal process.

Example:

```yaml
alleged_commenters:
  - display_name: "ExampleUser1"
    comment: "Example harmful comment"
    posted_approx: "date unknown"
```

---

## 3. What you need before you start

### Required (you almost certainly have these)

| Item | Used for |
|------|----------|
| **Your real email address** | Sending GDPR requests; Meta replies here |
| **Postal address** | Identity verification in letters (name + address) |
| **Full legal name** | As it appears on the harmful content |
| **Screenshots** | Post, comments, your photo — saved locally |
| **Post URL** | Set in `config.yaml` after `init` |
| **A computer** | Windows 11, Mac, or Linux |

### Helpful but optional

| Item | Used for |
|------|----------|
| **Phone number** | Included in letters; Meta may contact you |
| **Passport / ID** | **Not sent upfront.** Meta may ask later to verify identity |
| **Slack webhook** | Daily alerts when new URLs appear |
| **VPS (~£5/month)** | Hands-off daily monitoring |
| **SerpAPI or TinEye key** | Daily reverse-image search |

### Not required

| Item | Notes |
|------|-------|
| **Facebook password long-term** | GDPR runs on email; see [Section 4](#4-facebook-login--what-matters) |
| **Solicitor** | Only if platform + regulator both fail |
| **Police report** | Your chosen path avoids this |
| **Payment to Removify** | Same process, self-service |

---

## 4. Facebook login — what matters

You are **currently logged into Facebook**. That is useful now. You plan to **close the account after removal** — that is the correct order.

### Works without Facebook login

- Email **privacy@facebook.com** with GDPR letters
- Meta escalation form: `https://www.facebook.com/help/contact/571927962827151`
- Regulator complaint (URL from `jurisdiction.regulator_url` in config)
- Google delisting forms
- All ReclaimKit commands (`campaign`, `monitor`, `daemon`, etc.)

### Easier with Facebook login (do these **now**)

- Confirm the post is still live
- Take fresh screenshots if needed
- Download your Facebook data (Settings > Download your information)
- Save any in-app report reference numbers

### After you delete Facebook

- Meta can still process your GDPR request via **email**
- You **cannot** easily check if the post is gone — ask someone still in the group, or wait for Meta's reply
- **Deleting your account does NOT remove the post** — Meta must delete it separately

### Recommended order

```
1. Submit GDPR + escalation (while logged in)
2. Save screenshots and Meta reply emails locally
3. Wait up to 1 month for Meta
4. Confirm removal (check yourself or ask someone in the group)
5. Google delisting if anything still appears in search
6. THEN delete/deactivate Facebook
7. Keep monitoring 3–6 months via ReclaimKit (no Facebook needed)
```

---

## 5. Install ReclaimKit

### Option A — Local (quickest to start)

```bash
git clone https://github.com/tgollogly/ReclaimKit.git
cd reclaimkit
pip install -r requirements.txt
python3 main.py init
```

This creates `config.yaml` from the template and `evidence/screenshots/` folder.

### Option B — VPS with Docker (set-and-forget monitoring)

See [Section 13](#13-daily-monitoring-and-vps-automation) and `deploy/README.md`.

### Verify installation

```bash
python3 main.py doctor          # health check
python3 -m pytest tests/ -v     # run test suite (20 tests)
```

---

## 6. Configure your case

Edit **`config.yaml`** (never commit this file — it contains personal details).

If you created `config.yaml` before the latest update, copy new fields from
**`config.example.yaml`** — especially `case.facebook.meta_reports` and `preferences`.

### Subject block — fill with your real details

```yaml
subject:
  full_name: "Your Full Name"
  email: "your.email@example.com"
  phone: "+1 555 0100"
  address_line1: "Your street address"
  city: "Your city"
  region: ""              # state/province — optional
  postcode: "12345"
  country: "Your country"
```

### Case block — copy from config.example.yaml and edit

```yaml
case:
  facebook:
    group_name: "Example Community Group"
    post_date: "2025-06-05"
    post_caption: "Example caption text"
    post_url: "https://www.facebook.com/groups/EXAMPLE/posts/EXAMPLE/"
    post_origin: uncertain   # uncertain | third_party | self — see section 24
    reported_to_meta: true
    meta_reports:
      - type: "In-app content report (photo/post)"
        date: "2026-01-01"
        outcome: "Rejected — does not violate Community Standards"
        notes: "Attach Meta support screenshot"
      - type: "Group report"
        date: "2026-01-01"
        outcome: "Submitted"
```

Letters automatically cite these reports and explain why a Community Standards
rejection does **not** answer a GDPR request.

### Optional harm statement

```yaml
case:
  harm_statement: >
    Optional custom paragraph describing impact on you. If omitted, letters use
    a strong default harm/distress paragraph.
```

### Preferences

```yaml
preferences:
  no_police: true
  closing_facebook_after_removal: true
```

### Evidence folders

```yaml
evidence:
  screenshots_dir: "./evidence/screenshots"
  output_dir: "./output"
```

### Add screenshots

Copy your Facebook screenshots into **`evidence/screenshots/`**:

- Full post view (photo + caption visible)
- Each harmful comment (scroll and capture)
- Meta report confirmation screen
- **Meta "We didn't remove the photo" support message (important for Round 1)**

Supported formats: PNG, JPG, JPEG, WEBP.

### Secrets (VPS only — use environment variables)

Copy `.env.example` to `.env`:

```bash
RECLAIMKIT_SMTP_PASSWORD=       # Gmail app password if auto-email enabled
RECLAIMKIT_SLACK_WEBHOOK=       # Slack incoming webhook URL
RECLAIMKIT_SERPAPI_KEY=         # Optional image search
RECLAIMKIT_TINEYE_KEY=          # Optional image search
```

**Never put passwords in `config.yaml` on a VPS.** Use `.env` instead.

---

## 7. Day 1 — start the campaign

Run these commands in order:

```bash
# 1. Build evidence pack (hashed screenshots + summary)
python3 main.py evidence

# 2. Start campaign and generate Round 1 letters
python3 main.py campaign init

# 3. Check everything looks correct
python3 main.py doctor
python3 main.py campaign status
```

Or run everything in one go:

```bash
python3 main.py all
```

### What gets created

```
output/
  campaign/
    state.json                         (tracks your progress)
  campaign-package-YYYYMMDD.../
    README.txt
    round-01-meta/
      meta_r1_erasure_initial.txt      (EMAIL THIS TO META)
      SUBMIT.txt                       (step-by-step instructions)
    round-01-google/
      google_r1_removal.txt
      SUBMIT.txt
  evidence-pack-YYYYMMDD.../             (attach to emails if needed)
```

Each letter includes a **case reference** like `RK-ER-YOURNAME-META-R1` (generated from your name in config). Always put this in the email subject line.

---

## 8. How to send Round 1 to Meta

This is the **most important step**. It starts the legal response clock for your jurisdiction.

### Step-by-step

1. Open `output/campaign-package-.../round-01-meta/meta_r1_erasure_initial.txt`
2. Open your email client (Gmail, Outlook, etc.)
3. **To:** `privacy@facebook.com`
4. **CC (optional):** `dpo@facebook.com`
5. **Subject:** `RK-ER-YOURNAME-META-R1 — Article 17 Erasure Request — Your Full Name`
6. **Body:** Paste the entire letter
7. **Attachments:** All screenshots from `evidence/screenshots/`
8. Send from the **same email address** listed in `config.yaml`
9. Record submission in ReclaimKit:

```bash
python3 main.py campaign sent --track meta --round 1
```

### Tips for a strong submission

- Send from your real email — Meta may reply asking for verification
- Attach clear screenshots showing your face, name, and harmful comments
- Keep a copy of the sent email in a folder (or export to PDF)
- Do **not** send your passport unless Meta explicitly asks in a reply

### If you already reported in-app

Round 1 mentions your prior report. Meta sometimes treats GDPR as a separate, stronger legal obligation — send it anyway.

---

## 9. Campaign tracks and timeline

ReclaimKit runs three parallel **tracks**. Meta is the priority.

### Meta track — 6 rounds

| Round | Letter | When to send |
|-------|--------|--------------|
| **R1** | GDPR Article 17 initial request | **Day 1 — send today** |
| **R2** | GDPR reminder (no response) | 7+ days after R1 with no removal |
| **R3** | Trust & Safety escalation | 7+ days after R2, or if refused |
| **R4** | Formal rebuttal to refusal | When Meta refuses with a reason |
| **R5** | Notice of intended regulator complaint | After `response_days` with no removal |
| **R6** | Post-regulator follow-up to Meta | After regulator accepts complaint |

**Generate next round automatically:**

```bash
# No response after 7 days
python3 main.py campaign no-response --track meta

# Meta refused — include their reason
python3 main.py campaign refused --track meta --reason "They said it doesn't violate community standards"

# Manually generate a specific round
python3 main.py campaign next --track meta --round 3
```

**Round 3+ also submit the escalation form:**

`https://www.facebook.com/help/contact/571927962827151`

(No Facebook login required for this form.)

### Recording submissions

Every time you send a letter or submit a form:

```bash
python3 main.py campaign sent --track meta --round 2
python3 main.py campaign sent --track google --round 1
python3 main.py campaign sent --track regulator --round 1 --reference REG-REF-12345
```

### Check progress anytime

```bash
python3 main.py campaign status
```

### Mark success

When the post and comments are gone:

```bash
python3 main.py campaign success --note "Post removed confirmed 2026-08-XX"
python3 main.py close    # prints Facebook closure checklist
```

---

## 10. Google delisting (parallel track)

Google removal **hides content from search** — it does not delete the Facebook post. Run this **in parallel** with Meta, especially if your name or photo appears in Google results.

### Round 1 — Defamation

1. Open `output/campaign-package-.../round-01-google/google_r1_removal.txt`
2. Follow the URL in the letter header (Google Legal Troubleshooter)
3. Paste relevant sections into the form
4. Record: `python3 main.py campaign sent --track google --round 1`

### Additional Google tools

| Tool | URL | Use when |
|------|-----|----------|
| **Defamation troubleshooter** | https://support.google.com/legal/troubleshooter/1114905 | False allegations in search snippets |
| **Personal info removal** | https://support.google.com/websearch/contact/content_removal_form | Photo, address, phone in results |
| **Results About You** | https://myactivity.google.com/results-about-you | Ongoing alerts for new mentions |

### Monitor for new URLs

```bash
python3 main.py monitor
```

Reports save to `output/search-monitor-*.txt` and `.json`. Submit delisting for any harmful URLs found.

**Google forms are manual (~2 minutes each)** — ReclaimKit drafts the text; you paste it in.

---

## 11. Regulator complaint (if Meta refuses)

If Meta does not remove content within the deadline set in `jurisdiction.response_days`, or explicitly refuses your erasure request, escalate to your **data protection authority** — free, no police, no court.

### When to file

- Response deadline passed since Round 1 with no removal
- Meta sent a refusal citing "community standards" or similar
- After Meta Round 4 (rebuttal) failed

### How to file

1. Generate regulator letter: `python3 main.py campaign next --track regulator`
2. Go to the URL in `jurisdiction.regulator_url` in your config
3. Attach:
   - Evidence pack from `output/evidence-pack-.../`
   - All Meta correspondence (your emails + their replies)
   - Screenshots
4. Record: `python3 main.py campaign sent --track regulator --round 1 --reference YOUR-REG-REF`

### After the regulator

- The authority may contact Meta on your behalf
- Send Meta Round 5 (regulator notice) when you file
- Send Meta Round 6 after the regulator acknowledges the complaint

---

## 12. Closing Facebook after removal

**Do NOT delete Facebook until removal is confirmed or you have exhausted the privacy/regulator path.**

Run the built-in checklist:

```bash
python3 main.py close
```

### Before deleting your account

- [ ] Download your data: Settings > Download your information
- [ ] Save all Meta reply emails locally
- [ ] Save evidence pack and campaign letters from `output/`
- [ ] Remove apps connected to Facebook (Settings > Apps and websites)
- [ ] Update logins on sites where you used "Log in with Facebook"
- [ ] Confirm post is gone (check while still logged in, or ask someone in the group)

### Deactivate vs delete

| Action | Effect |
|--------|--------|
| **Deactivate** | Profile hidden; reversible for 30 days |
| **Delete permanently** | Cannot log back in; data scheduled for deletion |

Path: Settings and privacy > Settings > Accounts Centre > Personal details > Account ownership and control > Deactivation or deletion

### After Facebook is closed

- Continue `python3 main.py monitor` monthly for 3–6 months
- Re-submit Google delisting if new URLs appear
- Meta GDPR follow-up still works via email to `privacy@facebook.com`

---

## 13. Daily monitoring and VPS automation

Optional but recommended if you want hands-off daily checks (~£5/month VPS).

### What runs automatically (Docker or cron)

| Task | Frequency |
|------|-----------|
| Web search for your name | Daily |
| Reverse image search (if API key set) | Daily |
| Slack alert on new harmful URLs | When found |
| Auto-generate next Meta letter after 7 days silence | If enabled |
| Auto-email Meta | Optional (`auto_send_emails: true`) |

### Docker quick start

```bash
cd deploy
docker compose up -d --build
```

Logs: `output/cron.log` and `output/automation-log.jsonl`

### Cron (no Docker)

```bash
0 8 * * * cd /path/to/reclaimkit && python3 main.py daemon once >> output/cron.log 2>&1
```

### Test automation without sending

```bash
python3 main.py daemon once --dry-run
```

### Slack setup

1. Create incoming webhook: `https://api.slack.com/messaging/webhooks`
2. Add URL to `config.yaml` under `automation.slack_webhook_url`
3. Or set `RECLAIMKIT_SLACK_WEBHOOK` in `.env`

Full VPS details: **`deploy/README.md`**

---

## 14. All CLI commands reference

| Command | Purpose |
|---------|---------|
| `python3 main.py init` | Create `config.yaml` and evidence folders |
| `python3 main.py evidence` | Build hashed evidence pack |
| `python3 main.py letters` | Generate standalone takedown letters (non-campaign) |
| `python3 main.py campaign init` | Start campaign + Round 1 package |
| `python3 main.py campaign status` | Show progress dashboard |
| `python3 main.py campaign sent --track meta --round N` | Record submission |
| `python3 main.py campaign no-response --track meta` | 7-day silence, then next round |
| `python3 main.py campaign refused --track meta --reason "..."` | Refusal, then rebuttal letter |
| `python3 main.py campaign next --track meta --round N` | Generate specific round |
| `python3 main.py campaign success` | Mark content removed |
| `python3 main.py monitor` | Scan search for indexed URLs |
| `python3 main.py osint` | Document commenter handles |
| `python3 main.py guide` | Print removal action guide |
| `python3 main.py close` | Facebook closure checklist |
| `python3 main.py doctor` | Validate config, deps, letters |
| `python3 main.py daemon once` | Run daily automation cycle |
| `python3 main.py daemon once --dry-run` | Test without writes/emails |
| `python3 main.py all` | Evidence + campaign + osint + monitor |

Global option: `--config path/to/config.yaml` (default: `config.yaml`)

---

## 15. Windows 11 setup (Docker + WSL)

ReclaimKit is Python and runs best on **WSL2** (Windows Subsystem for Linux). Docker Desktop integrates with WSL.

### Step 1 — Install WSL2

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart if prompted. Ubuntu is the default distribution.

### Step 2 — Install Docker Desktop

1. Download from `https://www.docker.com/products/docker-desktop/`
2. Install and enable **WSL 2 backend** in Settings > General
3. Enable integration with your Ubuntu distro in Settings > Resources > WSL Integration

### Step 3 — Clone and run in WSL

Open Ubuntu (WSL terminal):

```bash
sudo apt update && sudo apt install -y python3 python3-pip git
git clone https://github.com/tgollogly/ReclaimKit.git
cd reclaimkit
pip install -r requirements.txt
python3 main.py init
# Edit config.yaml with: nano config.yaml
# Add screenshots to evidence/screenshots/
python3 main.py campaign init
python3 main.py doctor
```

### Step 4 — Optional VPS-style Docker monitoring

From WSL, inside the repo:

```bash
cd deploy
docker compose up -d --build
docker compose logs -f
```

### Accessing files from Windows

WSL files live at `\\wsl$\Ubuntu\home\<username>\reclaimkit\` in File Explorer. You can copy screenshots there directly.

### Testing on Windows (no VPS)

You do **not** need Docker for the core workflow. Local Python in WSL is enough:

```bash
python3 main.py campaign init
# Email Meta manually using the generated letter
python3 main.py campaign sent --track meta --round 1
python3 main.py monitor
```

---

## 16. Costs and comparison to paid services

| Option | Cost | Notes |
|--------|------|-------|
| **ReclaimKit (local)** | **£0** | Your time only |
| **VPS monitoring** | **~£5/month** | Hetzner, DigitalOcean, etc. |
| **SerpAPI (image search)** | **~$50/month** free tier available | Optional |
| **Removify** | **£400–£2,000 per item** | Same forms and emails |
| **Solicitor** | **Varies** | Only if platform + regulator both fail |

ReclaimKit automates what paid services do manually: letter drafting, escalation timing, monitoring, and record-keeping.

---

## 17. FAQ

### Do I need my Facebook password?

**Not for the removal process.** GDPR runs on your email and postal address. Login helps you check the post and take screenshots now, but follow-up works without it.

### Do I need to send my passport?

**Not in Round 1.** Meta may ask for ID in a reply email to verify you are the data subject. Only send if they request it.

### I already reported the post in-app. Do I still send GDPR?

**Yes.** In-app reports and GDPR Article 17 requests are different channels. GDPR creates a legal deadline Meta must meet.

### Will deleting Facebook remove the post?

**No.** The post must be removed by Meta while your request is active. Close your account **after** removal.

### Can this hurt my US travel or create a public record?

This process is **private correspondence** with Meta/Google/your regulator — not a public court case or police record. Google delisting **reduces** public visibility. Avoid posting about the case on public blogs (higher SEO risk than a private group).

### Can ReclaimKit identify who posted the comments?

**No.** Anonymous Facebook handles cannot be deanonymized without Meta legal disclosure. Focus on **content removal**, not confronting individuals.

### What if Meta says "doesn't violate community standards"?

Record the refusal and generate Round 4 (rebuttal):

```bash
python3 main.py campaign refused --track meta --reason "Pasted Meta's exact reply here"
```

Then proceed toward a regulator complaint if still not removed after the response deadline.

### How long does it take?

| Stage | Typical timeframe |
|-------|-------------------|
| Meta privacy response | Up to `jurisdiction.response_days` (often 30 days) |
| Google delisting | Days to weeks |
| Regulator complaint | Weeks to months |
| Full campaign | 1–3 months in most cases |

---

## 18. Troubleshooting

### Run the doctor (health check — not Docker)

**Doctor** = validate your setup before sending letters. **Docker** = run daily monitoring on a VPS (section 23).

```bash
python3 main.py doctor
python3 main.py --config config.example.yaml doctor   # validate template
```

Core checks must pass (marked ✓). Warnings (marked !) are items you must fix before emailing Meta — placeholder email, missing screenshots, etc.

### Common issues

| Problem | Fix |
|---------|-----|
| `config.yaml not found` | Run `python3 main.py init` |
| `No campaign found` | Run `python3 main.py campaign init` |
| `No screenshots found` | Add PNG/JPG files to `evidence/screenshots/` |
| Monitor import error | `pip install ddgs` |
| SMTP auto-email fails | Use Gmail App Password, not main password; set `RECLAIMKIT_SMTP_PASSWORD` |
| Letters missing your name | Edit `config.yaml` subject block |

### Run tests

```bash
python3 -m pytest tests/ -v
```

All 20 tests should pass.

Run the full audit script:

```bash
chmod +x scripts/audit.sh
./scripts/audit.sh
```

---

## 19. Support contacts

| Service | Contact | Use for |
|---------|---------|---------|
| **Your data protection authority** | URL in `jurisdiction.regulator_url` | Platform privacy failures |
| **Meta DPO** | privacy@facebook.com, dpo@facebook.com | Data erasure requests |

Set `jurisdiction.regulator_name` and `jurisdiction.regulator_url` in config for your country. Solicitors remain optional if the platform and regulator both fail.

---

## 20. Checklist — print and tick off

### Phase 1 — Setup (Day 1)

- [ ] Clone repo and run `pip install -r requirements.txt`
- [ ] Run `python3 main.py init`
- [ ] Fill real email, address, phone in `config.yaml`
- [ ] Copy screenshots to `evidence/screenshots/`
- [ ] Run `python3 main.py evidence`
- [ ] Run `python3 main.py campaign init`
- [ ] Run `python3 main.py doctor` (all checks green)

### Phase 2 — Meta removal (Week 1)

- [ ] Email Round 1 letter to `privacy@facebook.com`
- [ ] Subject line includes your case reference from the generated letter (e.g. `RK-ER-YOURNAME-META-R1`)
- [ ] Attach all screenshots
- [ ] Run `python3 main.py campaign sent --track meta --round 1`
- [ ] Save sent email and any Meta reply

### Phase 3 — Google (parallel)

- [ ] Run `python3 main.py monitor`
- [ ] Submit Google Round 1 if URLs found
- [ ] Enable Results About You on Google account
- [ ] Run `python3 main.py campaign sent --track google --round 1`

### Phase 4 — Follow-up (Weeks 2–4)

- [ ] If no removal in 7 days: `campaign no-response --track meta`
- [ ] If Meta refuses: `campaign refused --track meta --reason "..."`
- [ ] Round 3+: submit escalation form at `facebook.com/help/contact/571927962827151`
- [ ] If response deadline passes: regulator complaint + Meta Round 5

### Phase 5 — After removal

- [ ] Confirm post gone (while logged in or via someone in group)
- [ ] Run `python3 main.py campaign success`
- [ ] Download Facebook data
- [ ] Run `python3 main.py close` and follow checklist
- [ ] Delete/deactivate Facebook account
- [ ] Monitor monthly 3–6 months: `python3 main.py monitor`

---

## 21. Community Standards vs GDPR

These are **two different doors** into Meta. ReclaimKit is built for the legal one.

| | Community Standards (Report button) | Privacy erasure request (privacy@facebook.com) |
|---|---|---|
| **Question** | Does this break Meta's house rules? | Must you delete my personal data? |
| **Team** | Content moderation | Data protection / privacy |
| **Deadline** | None | Set by your jurisdiction (often **30 days**) |
| **Your outcome** | Rejected ("no violation") | Still pending until DPO responds |
| **Bullying/harm** | Often dismissed as "discussion" | Harm supports erasure + distress |

**Bullying is harmful.** Meta's rejection only means their moderation system did not classify it as a policy breach. Applicable privacy law still covers your photo, name, and comments about you.

## 22. Meta rejected your report — what now

If you received: *"We didn't remove the photo"* / *"doesn't go against Community Standards"*:

1. **Save a screenshot** to `evidence/screenshots/`
2. Add under `case.facebook.meta_reports` in `config.yaml` (see config.example.yaml)
3. **Send GDPR Round 1 anyway** — the letter now cites the rejection explicitly
4. Record refusal:

```bash
python3 main.py campaign refused --track meta --reason "In-app report rejected: does not violate Community Standards (12 Aug 2026)"
```

5. Attach the rejection screenshot to every Meta email

Paid removal firms see this rejection daily. Their next step is always **GDPR to privacy@facebook.com** — same as you.

## 23. Docker — does it auto-save?

> **Not the same as `doctor`:** **Docker** runs ReclaimKit on a VPS in the background.
> **`python3 main.py doctor`** is a separate health-check command (config, screenshots, letters).
> See [section 18](#18-troubleshooting) for `doctor`.

**Yes.** Docker does not lose your campaign when the container restarts.

These folders are **mounted from your PC/VPS** (not stored only inside the container):

| Host path | What is saved |
|-----------|----------------|
| `output/` | Campaign state, letters, monitor reports, automation logs |
| `output/campaign/state.json` | Round tracking (`campaign sent`, etc.) |
| `output/automation-log.jsonl` | Daily daemon history |
| `evidence/` | Screenshots and evidence packs |

From `deploy/docker-compose.yml`:

```yaml
volumes:
  - ../config.yaml:/app/config.yaml:ro
  - ../evidence:/app/evidence
  - ../output:/app/output
```

**What persists automatically when `daemon once` runs:**

- Updated `state.json` after escalation
- New monitor JSON reports
- `seen_urls.json` (URLs already alerted)
- Appended lines in `automation-log.jsonl`

**What is NOT automatic:**

- Sending Round 1 initially (you run `campaign init` once)
- Recording `campaign sent` unless you run the command (or auto-email sends)
- Google form submission (always manual)

**Safe workflow:**

```bash
python3 main.py campaign init
python3 main.py campaign sent --track meta --round 1
cd deploy && docker compose up -d --build
```

If the container is deleted and recreated, **your data remains** in `output/` and `evidence/` on the host.

---

## 24. Unsure who posted? (safe wording)

**You can still remove everything.** Applicable privacy law protects **your data** — not only cases where someone else posted.

If you do not remember whether you posted the caption yourself (e.g. after drinking, testing the group), use:

```yaml
case:
  facebook:
    post_origin: uncertain   # DEFAULT — safest
```

| Value | When to use |
|-------|-------------|
| **uncertain** | You are not sure who created the post — **use this if in any doubt** |
| **third_party** | You are certain someone else posted your photo/name |
| **self** | You posted it and want all data + comments removed |

**uncertain** letters say:
- You request erasure of your photo, name, and comments
- You do **not** consent to continued processing
- **Without claiming** someone else definitely posted
- **Without admitting** you posted — legally neutral

You are **not** required to tell Meta you might have posted drunk. Do **not** lie if they ask directly later.

The harmful **comments** are still from other people — erasing those protects you regardless of who wrote the caption.

---

## 25. Job hunting — will this hurt you?

| Risk | Level | Notes |
|------|-------|-------|
| **Private group post** | Medium | Not on Google for everyone, but group members see it |
| **Google search for your name** | Medium–High | If indexed, employers *may* find it — run `python3 main.py monitor` |
| **Niche community groups** | Low | Most recruiters do not search specific groups by name |
| **After Meta removal + Google delist** | Low | Source gone + search hidden = much safer |

**What helps job hunting:**
1. Remove source (Meta privacy request) — **do this first**
2. Google delisting + **Results About You** alerts
3. Do **not** post about the case publicly (creates new SEO)
4. LinkedIn/CV focus on skills — most employers check LinkedIn, not niche groups

**Reality:** Until removed, there is **some** risk if someone Googles you. After removal and delisting (typically 1–3 months), risk drops sharply. This is **not** a criminal record or court case — it does not appear on standard employment checks.

---

## 26. How long until content is erased?

| Stage | Typical time | What happens |
|-------|--------------|--------------|
| **Send privacy Round 1** | Day 1 (today) | Clock starts — platform has until `response_days` to respond |
| **Meta removes post** | 1–4 weeks | Many cases resolve Round 1–3 |
| **Meta refuses / silence** | Week 2–4 | Escalation rounds + regulator |
| **Regulator complaint** | Week 4–8+ | Free authority pressure |
| **Google delisting** | 1–4 weeks after submit | Hides from search (parallel track) |
| **Google cache clears** | Days–weeks after delist | Old snippets may linger briefly |
| **Full campaign** | **1–3 months** typical | Complex refusals take longer |

**Private group posts** are often **not indexed** by Google — but run monitor to check.

There is **no instant delete** — Meta has up to one month by law. ReclaimKit automates follow-up so you do not pay £400+ for someone else to send the same emails.

---

## 27. Cheap VPS for automation + free AI

Full guide: **[deploy/VPS-GUIDE.md](../deploy/VPS-GUIDE.md)**

| Provider | Cost | Recommendation |
|----------|------|----------------|
| **Hetzner CX22** | ~£4.50/mo | **Best value** — 4 GB RAM, EU servers, runs Docker + ReclaimKit |
| DigitalOcean | ~$6/mo | Easy for beginners |
| Oracle Cloud Free | £0 | Powerful if you get approved — setup harder |

One VPS can run:
- ReclaimKit daily monitor (this repo)
- **Ollama** — free local AI (Llama, Mistral)
- n8n, Uptime Kuma, VPN, other scripts

```bash
cd deploy && docker compose up -d --build
```

Data **auto-saves** to `output/` on the host — see section 23.

---

**ReclaimKit** | [MIT License](../LICENSE) | Copyright © 2026 [tgollogly](https://github.com/tgollogly)

**Legal disclaimer:** Templates and guides are for informational use only — not legal advice. Not affiliated with Meta, Google, or any reputation-management service. You are solely responsible for submissions and outcomes. See [LICENSE](../LICENSE) for full terms.

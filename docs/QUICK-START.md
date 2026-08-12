# ReclaimKit — Quick Start

**Remove harmful Facebook content + Google results — UK GDPR path.**

## 1. Install (5 minutes)

```bash
git clone https://github.com/tgollogly/stop-assholes.git
cd stop-assholes
pip install -r requirements.txt
python3 main.py init
```

## 2. Configure

Edit `config.yaml`:

- Real **email**, **address**, **phone**
- `post_origin: uncertain` if unsure who posted (safest)
- `meta_reports` — add Meta "We didn't remove" rejection

Copy screenshots → `evidence/screenshots/`

## 3. Start campaign

```bash
python3 main.py campaign init
python3 main.py doctor
```

## 4. Email Meta (most important)

Open `output/campaign-package-.../round-01-meta/meta_r1_gdpr_initial.txt`

- **To:** privacy@facebook.com
- **Subject:** include case reference (e.g. TG-ER-THOMAS-GOLLO-META-R1)
- **Attach:** all screenshots

```bash
python3 main.py campaign sent --track meta --round 1
```

## 5. Parallel tracks

- **Google:** `python3 main.py monitor` → submit delisting if URLs found
- **VPS (optional):** `cd deploy && docker compose up -d --build` (~£5/mo)
- **Auto-email (optional):** [AUTO-EMAIL-SETUP.md](AUTO-EMAIL-SETUP.md)

## 6. If Meta ignores (after 7 days)

```bash
python3 main.py campaign no-response --track meta
```

## 7. When removed

```bash
python3 main.py campaign success
python3 main.py close
```

---

| Doc | Purpose |
|-----|---------|
| [COMPLETE-GUIDE.md](COMPLETE-GUIDE.md) | Full guide (PDF available) |
| [AUTO-EMAIL-SETUP.md](AUTO-EMAIL-SETUP.md) | Free Gmail auto-send |
| [../deploy/VPS-GUIDE.md](../deploy/VPS-GUIDE.md) | Cheap VPS + Docker |
| [../deploy/README.md](../deploy/README.md) | VPS deploy details |

```bash
./scripts/audit.sh    # verify entire repo
```

**Not legal advice.** Templates use UK GDPR Article 17 — same channels paid firms use.

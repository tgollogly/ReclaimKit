<p align="center">
  <img src="assets/reclaimkit-hero.png" alt="ReclaimKit — UK/NI Reputation Reclaim Toolkit" width="100%" />
</p>

<h1 align="center">ReclaimKit</h1>

<p align="center">
  <strong>UK/NI Reputation Reclaim Toolkit</strong><br/>
  Multi-round GDPR campaigns · Daily monitoring · Docker automation
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT License" />
  <img src="https://img.shields.io/badge/region-UK%20%2F%20NI-teal?style=flat-square" alt="UK/NI" />
  <img src="https://img.shields.io/badge/cost-%240%20software-success?style=flat-square" alt="Free software" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square" alt="Python 3.10+" />
</p>

---

> Remove harmful Facebook posts and Google results using **UK GDPR Article 17** — the same emails and forms reputation firms charge **£400–£2,000** to send.

---

## How to test and deploy

ReclaimKit has **four phases**. Do them in order:

| Phase | What you do | Sends emails? | Time |
|-------|-------------|---------------|------|
| **1. Test** | Run health checks + dry-run | **No** — safe | ~5 min |
| **2. Configure** | Edit `config.yaml`, add screenshots | No | ~10 min |
| **3. Deploy** | Start Docker (daily automation) | Only if you enable auto-email | ~2 min |
| **4. Go live** | Email Meta yourself, record the send | **Yes** — you send Round 1 | ~5 min |

**Doctor** = one-off health check (`python3 main.py doctor`).  
**Docker** = background service that runs the daily job at 08:00 UTC. Different things.

---

## Pick your platform

| You are on… | Follow this section |
|-------------|---------------------|
| **Windows 11** (recommended) | [Windows — WSL + Docker](#windows-11--wsl--docker) |
| Linux or Mac | [Linux / Mac](#linux--mac) |
| Cloud VPS (~£5/mo, PC can be off) | [VPS](#vps--cloud-server) |

**Windows:** use **Ubuntu in WSL + Docker Desktop**, not PowerShell alone. PowerShell is only to install WSL (`wsl --install`) and start Docker Desktop.

---

## Windows 11 — WSL + Docker

### Prerequisites (one time, on Windows)

1. **WSL2** — PowerShell as Admin: `wsl --install` → restart  
2. **Docker Desktop** — install, enable **WSL integration** for Ubuntu  
3. Open **Ubuntu** from the Start menu (or type `wsl` in PowerShell)

Full walkthrough: [docs/WINDOWS-WSL-DOCKER.md](docs/WINDOWS-WSL-DOCKER.md) · [PDF](docs/WINDOWS-WSL-DOCKER.pdf)

---

### Phase 1 — Test (safe, no emails)

Paste in the **Ubuntu/WSL** terminal:

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/tgollogly/stop-assholes.git ~/stop-assholes
cd ~/stop-assholes
chmod +x scripts/wsl-setup-and-test.sh
./scripts/wsl-setup-and-test.sh
```

The script automatically:

1. Builds the Docker image  
2. Runs `doctor` (health check)  
3. Runs `campaign init` (generates sample Round 1 letters)  
4. Runs `daemon once --dry-run` (**safe test — nothing is emailed**)  
5. Starts the Docker container (Phase 3 deploy)

**Success = terminal shows `SETUP COMPLETE`.**

Verify manually if you want:

```bash
cd ~/stop-assholes/deploy

docker compose run --rm stop-assholes python3 main.py doctor
docker compose run --rm stop-assholes python3 main.py daemon once --dry-run
docker compose ps                    # should show container "Up"
ls ../output/campaign-package-*/round-01-meta/
```

| Check | Pass if… |
|-------|----------|
| `doctor` | Core checks pass (missing screenshots = warning only at this stage) |
| `daemon once --dry-run` | JSON output, no errors |
| `docker compose ps` | Container status **Up** |
| `output/.../meta_r1_gdpr_initial.txt` | File exists |

---

### Phase 2 — Configure (before emailing Meta)

```bash
nano ~/stop-assholes/config.yaml
```

Fill in your real **email**, **address**, and **phone**. Keep `post_origin: uncertain` if you are not sure who posted the caption.

Copy screenshots into `~/stop-assholes/evidence/screenshots/` (Meta rejection, post screenshot, etc.). From Windows Explorer:

```
\\wsl$\Ubuntu\home\YOUR_USERNAME\stop-assholes\evidence\screenshots\
```

Regenerate letters after editing config:

```bash
cd ~/stop-assholes/deploy
docker compose run --rm stop-assholes python3 main.py campaign init
docker compose run --rm stop-assholes python3 main.py doctor
```

---

### Phase 3 — Deploy (daily automation)

The setup script already started this. To manage the container:

```bash
cd ~/stop-assholes/deploy
docker compose up -d          # start (if stopped)
docker compose logs -f        # watch logs
docker compose down           # stop automation
cat ../output/cron.log        # cron history
```

**Your data persists on disk** at `~/stop-assholes/output/` and `~/stop-assholes/evidence/` — container restarts do not wipe campaign state or letters.

What runs automatically every day at **08:00 UTC**:

- Web search for your name  
- Slack alerts (if configured)  
- Generate next escalation letter after 7 days of no Meta reply  
- Optional: SMTP email to Meta ([AUTO-EMAIL-SETUP.md](docs/AUTO-EMAIL-SETUP.md))

---

### Phase 4 — Go live (email Meta)

1. Open the letter:  
   `~/stop-assholes/output/campaign-package-.../round-01-meta/meta_r1_gdpr_initial.txt`  
2. Email **privacy@facebook.com** — attach your screenshots  
3. Record that you sent it:

```bash
cd ~/stop-assholes/deploy
docker compose run --rm stop-assholes python3 main.py campaign sent --track meta --round 1
```

Check progress anytime:

```bash
docker compose run --rm stop-assholes python3 main.py campaign status
```

---

## Linux / Mac

### Phase 1 — Test

```bash
git clone https://github.com/tgollogly/stop-assholes.git
cd stop-assholes
pip install -r requirements.txt
python3 main.py init
python3 main.py doctor
python3 main.py daemon once --dry-run    # safe — no emails
python3 -m pytest tests/ -v              # 20 automated tests
```

### Phase 2 — Configure

Edit `config.yaml` (email, address, `post_origin: uncertain` if needed). Add screenshots to `evidence/screenshots/`.

```bash
python3 main.py campaign init
python3 main.py doctor
```

### Phase 3 — Deploy (Docker)

```bash
cd deploy
docker compose up -d --build
docker compose ps
docker compose logs -f
```

Or without Docker — cron on your machine:

```bash
crontab -e
# Add: 0 8 * * * cd /path/to/stop-assholes && python3 main.py daemon once >> output/cron.log 2>&1
```

### Phase 4 — Go live

1. Email Meta using the letter in `output/campaign-package-.../round-01-meta/`  
2. `python3 main.py campaign sent --track meta --round 1`

---

## VPS — cloud server

Use a VPS (~£4.50/mo on Hetzner) when you want automation running 24/7 while your PC is off.

Full guide: [deploy/VPS-GUIDE.md](deploy/VPS-GUIDE.md) · [deploy/README.md](deploy/README.md)

```bash
# SSH into your VPS (Ubuntu)
git clone https://github.com/tgollogly/stop-assholes.git
cd stop-assholes
pip install -r requirements.txt

# Phase 2 — configure
cp config.example.yaml config.yaml && nano config.yaml
mkdir -p evidence/screenshots output
# upload screenshots via scp or sftp

# Phase 1 — test
python3 main.py init
python3 main.py campaign init
python3 main.py doctor
python3 main.py daemon once --dry-run

# Phase 3 — deploy
cd deploy && docker compose up -d --build
docker compose ps

# Phase 4 — go live (email Meta from your laptop or the VPS)
python3 main.py campaign sent --track meta --round 1
```

Optional: copy `.env.example` to `.env` for Gmail auto-send — see [docs/AUTO-EMAIL-SETUP.md](docs/AUTO-EMAIL-SETUP.md).

---

## What runs automatically vs what you do

| Automated (Docker daily cron) | You do manually |
|------------------------------|-----------------|
| Web search for your name | **Email Meta Round 1** (first time) |
| Slack alerts on new URLs | Google delisting web forms (~2 min each) |
| Generate next letter after 7 days | Read Meta's reply emails |
| Optional: SMTP email to Meta | Send ID if Meta asks |

When Meta replies: run `campaign success`, `campaign refused`, or wait for 7-day auto-escalation. ReclaimKit does **not** read your inbox.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python3: command not found` on Windows | Use **WSL/Ubuntu**, not PowerShell. In PowerShell use `python` (no `3`). |
| `Docker daemon not running` | Start **Docker Desktop** on Windows; wait until it says Running. |
| `doctor` warns about screenshots | Add PNG/JPG files to `evidence/screenshots/`, then re-run `campaign init`. |
| Letters have placeholder text | Edit `config.yaml` with real details, then `campaign init` again. |
| Container not running | `cd deploy && docker compose up -d` |
| Want to re-test safely | `docker compose run --rm stop-assholes python3 main.py daemon once --dry-run` |
| Full repo check | `./scripts/audit.sh` (20 tests + doctor + PDFs) |

---

## Commands cheat sheet

Run locally as `python3 main.py <command>`, or in Docker:

```bash
cd deploy
docker compose run --rm stop-assholes python3 main.py <command>
```

| Command | Purpose |
|---------|---------|
| `doctor` | Health check — run first |
| `campaign init` | Generate Round 1 letters |
| `campaign sent --track meta --round 1` | Record that you emailed Meta |
| `campaign status` | Show progress |
| `campaign no-response --track meta` | 7 days silence → next round |
| `campaign refused --track meta --reason "..."` | Refusal → rebuttal |
| `campaign success` | Mark content removed |
| `daemon once --dry-run` | **Safe test** — no emails sent |
| `daemon once` | Run daily job now (live) |
| `monitor` | Scan Google for your name |
| `init` | Create `config.yaml` and evidence folders |
| `evidence` | Build hashed evidence pack |
| `letters` | Generate standalone takedown letters |
| `close` | Facebook closure checklist |
| `all` | Evidence + campaign + osint + monitor |

---

## Documentation

| Guide | When to read |
|-------|--------------|
| [docs/QUICK-START.md](docs/QUICK-START.md) | Minimum steps to email Meta today |
| [docs/COMPLETE-GUIDE.md](docs/COMPLETE-GUIDE.md) | Full walkthrough + FAQ |
| [docs/WINDOWS-WSL-DOCKER.md](docs/WINDOWS-WSL-DOCKER.md) | **Windows test & deploy** (detailed) |
| [docs/AUTO-EMAIL-SETUP.md](docs/AUTO-EMAIL-SETUP.md) | Free Gmail auto-send |
| [deploy/VPS-GUIDE.md](deploy/VPS-GUIDE.md) | Cheap cloud server setup |

PDFs in `docs/*.pdf` — rebuild with `./scripts/build-all-pdfs.sh`

---

## Campaign tracks

| Track | Rounds | Purpose |
|-------|--------|---------|
| **Meta** | 6 | GDPR → reminder → escalation → ICO |
| **Google** | 3 | Defamation delisting drafts |
| **ICO** | 1 | If Meta refuses after 30 days |

---

## Developer / full audit

```bash
./scripts/audit.sh      # tests + letters + doctor + PDFs
python3 -m pytest tests/ -v
```

---

## License

**MIT License** — Copyright © 2026 **Thomas Gollogly**. See [LICENSE](LICENSE).

Not legal advice. Not affiliated with Meta, Google, or Removify.

<p align="center"><sub>Built in Northern Ireland · GDPR Article 17 · Defamation Act (NI) 2022</sub></p>

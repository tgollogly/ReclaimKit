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

# ⭐ START HERE — Windows 11

**If your prompt says `PS C:\Users\User>` you are in PowerShell.**  
The commands `git clone`, `chmod`, and `sudo apt` **do not work there**. That is why you got errors.

### One-time setup (do once)

1. Install **Docker Desktop** → open it → wait until it says **Running**
2. Install **WSL + Ubuntu** — PowerShell as Admin:
   ```powershell
   wsl --install -d Ubuntu
   ```
   Restart if asked.

### Run setup

> **Important:** This GitHub repo is **private**. The download script (`irm ...`) will **404** and `git clone` will ask for a password until you do **one** of the following:
>
> **Easiest — make the repo public** (you own it):  
> https://github.com/tgollogly/ReclaimKit/settings → General → scroll to **Danger Zone** → **Change visibility** → **Public**
>
> **Or keep it private** — create a GitHub token: https://github.com/settings/tokens → **Generate new token (classic)** → check **repo** → copy the token. Use it as the password when `git clone` asks (username = `tgollogly`).

**After that**, copy **one line** into PowerShell (`PS C:\...>`):

```powershell
wsl -d Ubuntu bash -c "sudo apt update && sudo apt install -y git && rm -rf ~/stop-assholes && git clone https://github.com/tgollogly/ReclaimKit.git ~/stop-assholes && cd ~/stop-assholes && chmod +x scripts/wsl-setup-and-test.sh && ./scripts/wsl-setup-and-test.sh"
```

If `wsl -d Ubuntu` fails, use `wsl` instead:

```powershell
wsl bash -c "sudo apt update && sudo apt install -y git && rm -rf ~/stop-assholes && git clone https://github.com/tgollogly/ReclaimKit.git ~/stop-assholes && cd ~/stop-assholes && chmod +x scripts/wsl-setup-and-test.sh && ./scripts/wsl-setup-and-test.sh"
```

If `git clone` asks for credentials inside that command, run setup **manually in Ubuntu** instead (see below).

**Wait until you see `SETUP COMPLETE`.** Do not type anything else while it runs.

### Or run manually in Ubuntu (if clone asks for login)

1. Start menu → **Ubuntu** (prompt must be `useradmin@DESKTOP:~$`, not `PS C:\`)
2. Type **one command at a time**, press Enter after each:

```bash
sudo apt update
```

```bash
sudo apt install -y git
```

```bash
rm -rf ~/stop-assholes
```

```bash
git clone https://github.com/tgollogly/ReclaimKit.git ~/stop-assholes
```

When asked: username = `tgollogly`, password = **your GitHub token** (not your Windows password).

```bash
cd ~/stop-assholes
```

```bash
chmod +x scripts/wsl-setup-and-test.sh
```

```bash
./scripts/wsl-setup-and-test.sh
```

### After setup — configure and email Meta

Open **Ubuntu** from the Start menu (prompt looks like `username@DESKTOP:~$`), then:

```bash
nano ~/stop-assholes/config.yaml          # your real email, address, phone
cd ~/stop-assholes/deploy
docker compose run --rm stop-assholes python3 main.py campaign init
```

Copy screenshots into `~/stop-assholes/evidence/screenshots/`.

Email **privacy@facebook.com** using the letter in  
`~/stop-assholes/output/campaign-package-.../round-01-meta/meta_r1_gdpr_initial.txt`

Then record the send:

```bash
cd ~/stop-assholes/deploy
docker compose run --rm stop-assholes python3 main.py campaign sent --track meta --round 1
```

**Detailed Windows guide:** [docs/WINDOWS-WSL-DOCKER.md](docs/WINDOWS-WSL-DOCKER.md) · [PDF](docs/WINDOWS-WSL-DOCKER.pdf)

### Wrong terminal? Read this

| Prompt | OK to run setup? |
|--------|------------------|
| `PS C:\Users\User>` | **No** — use the PowerShell one-liner above |
| `username@DESKTOP:~$` | **Yes** — Ubuntu; use bash commands |
| `DESKTOP:/mnt/host/c/...#` | **No** — wrong Linux; open **Ubuntu** app instead |

**Do not** type `wsl` and then run `sudo apt` on the next `PS C:\` line — that is still PowerShell.

Clean up a bad PowerShell clone:

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\~\stop-assholes" -ErrorAction SilentlyContinue
```

---

### Complete walkthrough — every step (Windows)

Follow this in order. **One-time** steps only need doing once.

#### One-time: install Ubuntu + Docker

1. **PowerShell as Admin:** `wsl --install -d Ubuntu` → restart PC  
   - If it says *already exists*, Ubuntu is installed — skip this.
2. Create Ubuntu user/password when prompted (e.g. `useradmin`).
3. Install **Docker Desktop** → open it → wait until **Running**.
4. Docker Desktop → **Settings → Resources → WSL Integration** → turn **ON** for **Ubuntu** → **Apply & Restart**.
5. In PowerShell: `wsl --shutdown` → wait 10 seconds → reopen Ubuntu.

#### One-time: GitHub access (private repo)

6. Create a token: https://github.com/settings/tokens → **Generate new token (classic)** → tick **repo** → copy `ghp_...`  
   - Or make repo public: https://github.com/tgollogly/ReclaimKit/settings → **Change visibility → Public**

#### One-time: clone and run setup

7. Open Ubuntu (`wsl -d Ubuntu` or Start menu → **Ubuntu**). Prompt must be `useradmin@DESKTOP:~$`.
8. Run **one command at a time**:
   ```bash
   sudo apt update
   sudo apt install -y git
   rm -rf ~/stop-assholes
   git clone https://github.com/tgollogly/ReclaimKit.git ~/stop-assholes
   ```
   - If asked: username `tgollogly`, password = **GitHub token** (not Windows password).
9. Continue setup:
   ```bash
   cd ~/stop-assholes
   chmod +x scripts/wsl-setup-and-test.sh
   docker info          # must show Server Version — if not, fix WSL Integration (step 4)
   ./scripts/wsl-setup-and-test.sh
   ```
   Pass = **`SETUP COMPLETE`**.

#### Configure (edit once, saved forever)

10. Edit config:
    ```bash
    nano ~/stop-assholes/config.yaml
    ```
    Change email, phone, address to your real details. Keep `post_origin: uncertain` if unsure who posted.

    **Save in nano:** `Ctrl+X` → `Y` → `Enter`

11. Regenerate letters and add screenshots:
    ```bash
    cd ~/stop-assholes/deploy
    docker compose run --rm stop-assholes python3 main.py campaign init
    ```
    Copy PNG/JPG screenshots to `~/stop-assholes/evidence/screenshots/`  
    (Windows path: `\\wsl$\Ubuntu\home\useradmin\stop-assholes\evidence\screenshots\`)

#### Go live — email Meta

12. Open letter: `~/stop-assholes/output/campaign-package-.../round-01-meta/meta_r1_gdpr_initial.txt`  
    Email **privacy@facebook.com** with screenshots attached, then:
    ```bash
    cd ~/stop-assholes/deploy
    docker compose run --rm stop-assholes python3 main.py campaign sent --track meta --round 1
    ```

---

### After closing the terminal — does it autosave?

**Yes. You do NOT rerun setup every time.**

Docker saves everything to your Ubuntu home folder on disk. Closing the terminal does not delete anything.

| Saved automatically | Location | Rerun setup? |
|---------------------|----------|--------------|
| Your config | `~/stop-assholes/config.yaml` | **No** |
| Generated letters | `~/stop-assholes/output/` | **No** |
| Campaign progress | `~/stop-assholes/output/campaign/state.json` | **No** |
| Screenshots | `~/stop-assholes/evidence/screenshots/` | **No** |
| Daily automation logs | `~/stop-assholes/output/cron.log` | **No** |
| Docker container (daily cron) | Runs in background | Restarts with Docker Desktop |

**After closing the terminal**, open Ubuntu again and run only:

```bash
wsl -d Ubuntu
cd ~/stop-assholes/deploy
docker compose ps                    # check container is Up
docker compose run --rm stop-assholes python3 main.py campaign status
```

You only rerun `./scripts/wsl-setup-and-test.sh` if you delete the repo or move to a new PC.

**Docker Desktop must be Running** for daily automation. Your files stay on disk even if Docker is closed — you just can't run docker commands until you start it again.

#### Verify autosave is working

Autosave is **built in** — `deploy/docker-compose.yml` bind-mounts your folders to disk:

```yaml
volumes:
  - ../config.yaml:/app/config.yaml:ro
  - ../evidence:/app/evidence      # screenshots — saved on laptop
  - ../output:/app/output          # letters, state, logs — saved on laptop
```

Run this anytime in Ubuntu:

```bash
cd ~/stop-assholes
chmod +x scripts/check-autosave.sh
./scripts/check-autosave.sh
```

Or check manually:

```bash
ls ~/stop-assholes/config.yaml
ls ~/stop-assholes/output/campaign/state.json
cd ~/stop-assholes/deploy && docker compose ps
```

If `state.json` exists and the container is **Up**, autosave is working.

---

## Laptop vs cloud VPS — which do you need?

| | **Your laptop (Windows + WSL)** | **Cloud VPS (~£5/mo)** |
|---|--------------------------------|------------------------|
| **Best for** | Getting started, editing config, emailing Meta | 24/7 automation while PC is off |
| **You already have this** | ✓ if setup completed | Optional extra |
| **Daily cron (08:00 UTC)** | Yes, when Docker Desktop is running | Yes, always on |
| **Autosave** | Yes — `~/stop-assholes/` on your PC | Yes — `/root/stop-assholes/` on server |
| **Cost** | £0 | ~£4.50/mo (Hetzner) |
| **Needs PC on?** | Docker Desktop must be running | No |

**Recommended path for Thomas:**

1. **Run on laptop first** (you are here) — configure, email Meta Round 1, verify it works  
2. **Add VPS later** (optional) — only if you want monitoring when your laptop is off  

You can use **both** — laptop for editing letters, VPS for always-on monitoring. Copy `config.yaml`, `evidence/`, and `output/` to the VPS to sync progress.

---

### Run on your laptop (daily use)

**Open Ubuntu** → run these whenever you need ReclaimKit:

```bash
cd ~/stop-assholes/deploy
docker compose ps                                              # container Up?
docker compose run --rm stop-assholes python3 main.py campaign status
docker compose run --rm stop-assholes python3 main.py campaign init   # after config edits
docker compose run --rm stop-assholes python3 main.py campaign sent --track meta --round 1
```

**Edit config:** `nano ~/stop-assholes/config.yaml` → save `Ctrl+X`, `Y`, `Enter`  
**Screenshots:** `\\wsl$\Ubuntu\home\useradmin\stop-assholes\evidence\screenshots\`  
**Letters:** `\\wsl$\Ubuntu\home\useradmin\stop-assholes\output\`

**Start automation** (if container stopped):

```bash
cd ~/stop-assholes/deploy && docker compose up -d
```

---

### Deploy to cloud VPS (optional, 24/7)

Use when you want daily monitoring even when your laptop is closed.

**Full guide:** [deploy/VPS-GUIDE.md](deploy/VPS-GUIDE.md)

1. Rent a VPS (recommended: **Hetzner CX22** ~£4.50/mo, Ubuntu 24.04)
2. SSH in from PowerShell: `ssh root@YOUR_VPS_IP`
3. On the VPS, run **one block**:

```bash
apt update && apt install -y git docker.io docker-compose-v2
git clone https://github.com/tgollogly/ReclaimKit.git ~/stop-assholes
cd ~/stop-assholes
cp config.example.yaml config.yaml
nano config.yaml                    # same details as laptop — or copy config over
mkdir -p evidence/screenshots output
python3 main.py init 2>/dev/null || pip3 install -r requirements.txt
python3 main.py campaign init
cd deploy && docker compose up -d --build
docker compose ps
```

4. **Copy your laptop progress to VPS** (optional, from Ubuntu on laptop):

```bash
scp ~/stop-assholes/config.yaml root@YOUR_VPS_IP:~/stop-assholes/
scp -r ~/stop-assholes/evidence root@YOUR_VPS_IP:~/stop-assholes/
scp -r ~/stop-assholes/output root@YOUR_VPS_IP:~/stop-assholes/
```

5. On VPS, restart container: `cd ~/stop-assholes/deploy && docker compose up -d`

**VPS autosave:** same bind-mounts — data survives reboots at `~/stop-assholes/output/` on the server.

---

## How to test and deploy (all platforms)

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

**Windows:** see **[START HERE — Windows 11](#-start-here--windows-11)** at the top of this page.

---

## Windows 11 — WSL + Docker (details)

Everything you need is in **[START HERE](#-start-here--windows-11)** above. This section has extra detail.

### PowerShell vs WSL

ReclaimKit setup commands are **Linux commands**. They do **not** work in Windows PowerShell.

| Your prompt looks like… | Where you are | Will setup work? |
|-------------------------|---------------|------------------|
| `PS C:\Users\User>` | **PowerShell** (Windows) | **No** |
| `username@PC:~$` | **Ubuntu** (WSL/Linux) | **Yes** |
| `DESKTOP-xxx:/mnt/host/c/...#` | Docker's WSL (wrong) | **No** — open Ubuntu app |

**You are still in PowerShell if the line before your command starts with `PS C:\`.**

Run setup using the **one-liner or `setup-windows.ps1`** in [START HERE](#-start-here--windows-11) — do not paste bash commands into PowerShell.

### Prerequisites (one time, on Windows)

1. **WSL2 + Ubuntu** — PowerShell as Admin: `wsl --install -d Ubuntu` → restart  
2. **Docker Desktop** — install, enable **WSL integration** for Ubuntu  
3. Docker Desktop must say **Running** before setup

Check Ubuntu is installed:

```powershell
wsl -l -v
```

Full walkthrough: [docs/WINDOWS-WSL-DOCKER.md](docs/WINDOWS-WSL-DOCKER.md) · [PDF](docs/WINDOWS-WSL-DOCKER.pdf)

---

### Phase 1 — Test (safe, no emails)

Use the **PowerShell one-liner** in [START HERE](#-start-here--windows-11).

Or open **Ubuntu** from Start menu and paste:

```bash
sudo apt update && sudo apt install -y git
rm -rf ~/stop-assholes
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

## VPS — cloud server (optional)

See **[Laptop vs cloud VPS](#laptop-vs-cloud-vps--which-do-you-need)** above for when you need this.

Use a VPS (~£4.50/mo on Hetzner) when you want automation running 24/7 while your PC is off.

Full guide: [deploy/VPS-GUIDE.md](deploy/VPS-GUIDE.md) · [deploy/README.md](deploy/README.md)

```bash
# SSH into your VPS (Ubuntu) — from PowerShell: ssh root@YOUR_VPS_IP
apt update && apt install -y git docker.io docker-compose-v2
git clone https://github.com/tgollogly/ReclaimKit.git ~/stop-assholes
cd ~/stop-assholes
cp config.example.yaml config.yaml && nano config.yaml
mkdir -p evidence/screenshots output

python3 main.py init 2>/dev/null || pip3 install -r requirements.txt
python3 main.py campaign init
python3 main.py doctor
python3 main.py daemon once --dry-run

cd deploy && docker compose up -d --build
docker compose ps
./scripts/check-autosave.sh    # verify autosave on VPS

# After emailing Meta (from laptop or VPS):
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
| `Docker daemon not running` (but Docker Desktop open) | Docker Desktop → Settings → WSL Integration → enable **Ubuntu** → Apply & Restart → `wsl --shutdown` → reopen Ubuntu → `docker info` |
| Closed terminal — lost everything? | **No** — config, letters, progress saved in `~/stop-assholes/`. Just reopen Ubuntu. |
| How to save in nano | `Ctrl+X` → `Y` → `Enter` |
| `git clone` asks for password | Use GitHub token as password (username `tgollogly`), or make repo public |
| `&&` / `chmod` not found | You are in PowerShell — open Ubuntu (`wsl -d Ubuntu`) |
| `python3: command not found` on Windows | Use **WSL/Ubuntu**, not PowerShell |
| `doctor` warns about screenshots | Add PNG/JPG files to `evidence/screenshots/`, then re-run `campaign init` |
| Letters have placeholder text | Edit `config.yaml` with real details, then `campaign init` again |
| Container not running | `cd ~/stop-assholes/deploy && docker compose up -d` |
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

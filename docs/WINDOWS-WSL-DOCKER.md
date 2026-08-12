# Windows 11 — WSL2 + Docker (automated test)

Run ReclaimKit in **WSL2** with **Docker Desktop** — daily automation, auto-save, optional auto-email.

> **Do not paste `git clone`, `chmod`, or `sudo apt` into PowerShell** — they only work in Ubuntu/Linux.

---

## Quick setup (PowerShell)

1. Docker Desktop open and **Running**
2. Paste **one** of these in PowerShell (`PS C:\...>`):

```powershell
irm https://raw.githubusercontent.com/tgollogly/ReclaimKit/main/scripts/setup-windows.ps1 | iex
```

Or:

```powershell
wsl -d Ubuntu bash -c "sudo apt update && sudo apt install -y git && rm -rf ~/stop-assholes && git clone https://github.com/tgollogly/stop-assholes.git ~/stop-assholes && cd ~/stop-assholes && chmod +x scripts/wsl-setup-and-test.sh && ./scripts/wsl-setup-and-test.sh"
```

Pass = **`SETUP COMPLETE`**.

---

## Part 1 — One-time setup (Windows)

### 1. Install WSL2

**PowerShell as Administrator:**

```powershell
wsl --install
```

Restart if asked. Ubuntu is the default Linux.

### 2. Install Docker Desktop

1. Download: https://www.docker.com/products/docker-desktop/
2. Install and open Docker Desktop
3. **Settings → General** → enable **Use the WSL 2 based engine**
4. **Settings → Resources → WSL Integration** → enable **Ubuntu**
5. Wait until Docker Desktop says **Running**

### 3. Open Ubuntu (WSL)

Start menu → **Ubuntu**, or PowerShell:

```powershell
wsl
```

You should see a Linux prompt like `username@PC:~$`

---

## Part 2 — One script setup + test (WSL)

**Your prompt must look like `username@PC:~$` — not `PS C:\Users\User>`.**

**Easiest:** use the PowerShell one-liner in [Quick setup](#quick-setup-powershell) above.

**Manual:** open **Ubuntu** from Start menu, then paste:

```bash
sudo apt update && sudo apt install -y git
rm -rf ~/stop-assholes
git clone https://github.com/tgollogly/stop-assholes.git ~/stop-assholes
cd ~/stop-assholes
chmod +x scripts/wsl-setup-and-test.sh
./scripts/wsl-setup-and-test.sh
```

The script will:

1. Check Docker is running  
2. Create `config.yaml` from template  
3. Build the Docker image  
4. Run `doctor` (health check)  
5. Run `campaign init` (generate Round 1 letters)  
6. Run `daemon once --dry-run` (safe automation test)  
7. Start the container (daily cron at 08:00 UTC)  

**Expected end message:** `SETUP COMPLETE`

---

## Part 3 — Configure before emailing Meta

Still in WSL:

```bash
nano ~/stop-assholes/config.yaml
```

**Save in nano:** `Ctrl+X` → `Y` → `Enter`

Fill in:

- Real **email**, **address**, **phone**
- `post_origin: uncertain` (safest if unsure who posted)
- `meta_reports` (your Meta rejection details)

Add screenshots (from Windows you can copy to):

```
\\wsl$\Ubuntu\home\YOUR_USERNAME\stop-assholes\evidence\screenshots\
```

Or in WSL:

```bash
cp /mnt/c/Users/User/Pictures/your-screenshot.png ~/stop-assholes/evidence/screenshots/
```

Regenerate letters after config change:

```bash
cd ~/stop-assholes/deploy
docker compose run --rm stop-assholes python3 main.py campaign init
```

---

## Part 4 — Email Meta + record send

1. Open letter (from Windows Explorer or WSL):

   `~/stop-assholes/output/campaign-package-.../round-01-meta/meta_r1_gdpr_initial.txt`

2. Email **privacy@facebook.com** with screenshots attached

3. Record in ReclaimKit:

```bash
cd ~/stop-assholes/deploy
docker compose run --rm stop-assholes python3 main.py campaign sent --track meta --round 1
```

---

## Part 5 — Enable auto-email (optional, free Gmail)

See **[AUTO-EMAIL-SETUP.md](AUTO-EMAIL-SETUP.md)**

Quick version in WSL:

```bash
cd ~/stop-assholes
cp .env.example .env
nano .env   # RECLAIMKIT_SMTP_PASSWORD=your-gmail-app-password
nano config.yaml   # auto_send_emails: true, smtp.enabled: true
```

Uncomment in `deploy/docker-compose.yml`:

```yaml
env_file:
  - ../.env
```

Restart:

```bash
cd ~/stop-assholes/deploy
docker compose down && docker compose up -d --build
```

---

## Daily commands (WSL)

All from `~/stop-assholes/deploy`:

| Task | Command |
|------|---------|
| Check status | `docker compose run --rm stop-assholes python3 main.py campaign status` |
| View logs | `docker compose logs -f` |
| Cron log file | `cat ../output/cron.log` |
| Test automation (safe) | `docker compose run --rm stop-assholes python3 main.py daemon once --dry-run` |
| Run automation now | `docker compose run --rm stop-assholes python3 main.py daemon once` |
| Stop container | `docker compose down` |
| Start again | `docker compose up -d` |

---

## Doctor vs Docker

| | **doctor** | **Docker** |
|---|-----------|------------|
| What | Health check | Runs daily automation |
| Command | `docker compose run --rm stop-assholes python3 main.py doctor` | `docker compose up -d` |
| Auto-save | No | Yes — `output/` folder on your disk |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Docker daemon not running` | Start Docker Desktop on Windows |
| `wsl: command not found` | Run `wsl --install`, restart |
| `Cannot connect to Docker` | Docker Desktop → WSL Integration → Ubuntu ON |
| Doctor warns no screenshots | Add PNG/JPG to `evidence/screenshots/` |
| Cron not running yet | Runs daily 08:00 UTC — or run `daemon once` manually |
| Slow on `/mnt/c/` | Clone in `~/stop-assholes` (Linux home), not `C:\` |

---

## Undo everything (WSL)

```bash
cd ~/stop-assholes/deploy
docker compose down
cd ~
rm -rf ~/stop-assholes
```

---

## PDF guides

After clone, open in Windows:

- `\\wsl$\Ubuntu\home\YOUR_USERNAME\stop-assholes\docs\QUICK-START.pdf`
- `docs\COMPLETE-GUIDE.pdf`
- `docs\AUTO-EMAIL-SETUP.pdf`

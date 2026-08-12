<p align="center">
  <img src="assets/reclaimkit-hero.png" alt="ReclaimKit — Reputation Reclaim Toolkit" width="100%" />
</p>

<h1 align="center">ReclaimKit</h1>

<p align="center">
  <strong>Reputation Reclaim Toolkit</strong><br/>
  Multi-round privacy campaigns · Daily monitoring · Docker automation
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-1e3a5f?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="MIT License" />
  <img src="https://img.shields.io/badge/cost-%240%20software-059669?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Free software" />
  <img src="https://img.shields.io/badge/python-3.10%2B-0891b2?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/docker-ready-2563eb?style=for-the-badge&logo=docker&logoColor=white" alt="Docker ready" />
  <img src="https://img.shields.io/badge/tests-20%20passing-059669?style=for-the-badge&logo=pytest&logoColor=white" alt="20 tests passing" />
</p>

<p align="center">
  <a href="#four-phase-workflow"><img src="https://img.shields.io/badge/Workflow-4%20Phases-6366f1?style=flat-square" alt="Workflow" /></a>
  <a href="#quick-setup"><img src="https://img.shields.io/badge/Setup-Quick%20Start-0891b2?style=flat-square" alt="Setup" /></a>
  <a href="#configure-any-country"><img src="https://img.shields.io/badge/Config-Any%20Country-7c3aed?style=flat-square" alt="Configure" /></a>
  <a href="#documentation"><img src="https://img.shields.io/badge/Docs-Guides-2563eb?style=flat-square" alt="Documentation" /></a>
</p>

<br/>

> [!IMPORTANT]
> Remove harmful social posts and search results using **privacy erasure requests** — the same emails and forms reputation firms charge hundreds or thousands of dollars to send.

<br/>

## Four-phase workflow

<p align="center">
  <img src="https://img.shields.io/badge/Phase%201-Test-6366f1?style=for-the-badge" alt="Phase 1 Test" />
  <img src="https://img.shields.io/badge/Phase%202-Configure-0891b2?style=for-the-badge" alt="Phase 2 Configure" />
  <img src="https://img.shields.io/badge/Phase%203-Deploy-7c3aed?style=for-the-badge" alt="Phase 3 Deploy" />
  <img src="https://img.shields.io/badge/Phase%204-Go%20Live-059669?style=for-the-badge" alt="Phase 4 Go Live" />
</p>

```mermaid
flowchart LR
    A["① Test<br/>Health check"] --> B["② Configure<br/>config.yaml"]
    B --> C["③ Deploy<br/>Docker daemon"]
    C --> D["④ Go live<br/>Send Round 1"]

    style A fill:#6366f1,stroke:#4338ca,color:#fff
    style B fill:#0891b2,stroke:#0e7490,color:#fff
    style C fill:#7c3aed,stroke:#6d28d9,color:#fff
    style D fill:#059669,stroke:#047857,color:#fff
```

<table>
<thead>
<tr>
<th align="left"><img src="https://img.shields.io/badge/Phase-1-6366f1?style=flat-square" alt="1" /></th>
<th align="left">What</th>
<th align="left">Sends emails?</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Test</strong></td>
<td>Health check + dry-run</td>
<td><img src="https://img.shields.io/badge/emails-no-dc2626?style=flat-square" alt="No" /></td>
</tr>
<tr>
<td><strong>Configure</strong></td>
<td>Edit <code>config.yaml</code>, add screenshots</td>
<td><img src="https://img.shields.io/badge/emails-no-dc2626?style=flat-square" alt="No" /></td>
</tr>
<tr>
<td><strong>Deploy</strong></td>
<td>Start Docker (daily automation)</td>
<td><img src="https://img.shields.io/badge/emails-optional-d97706?style=flat-square" alt="Optional" /></td>
</tr>
<tr>
<td><strong>Go live</strong></td>
<td>Email platform privacy team, record send</td>
<td><img src="https://img.shields.io/badge/emails-yes-059669?style=flat-square" alt="Yes" /></td>
</tr>
</tbody>
</table>

> [!TIP]
> **Developers:** run <code>./scripts/audit.sh</code> for the full check — 20 tests, doctor, optional PDF build.

<br/>

## Quick setup

<p align="left">
  <img src="https://img.shields.io/badge/Windows-WSL%20%2B%20Docker-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/Linux%20%2F%20Mac-000000?style=for-the-badge&logo=linux&logoColor=white" alt="Linux Mac" />
  <img src="https://img.shields.io/badge/Cloud%20VPS-2563eb?style=for-the-badge&logo=digitalocean&logoColor=white" alt="Cloud VPS" />
</p>

### Windows 11 (WSL + Docker)

> [!NOTE]
> Run commands in **Ubuntu** (<code>useradmin@DESKTOP:~$</code>) — not PowerShell (<code>PS C:\</code>).

| Step | Action |
|:----:|--------|
| **1** | Install **Docker Desktop** → **Running** |
| **2** | Install **Ubuntu**: PowerShell Admin → `wsl --install -d Ubuntu` |
| **3** | Docker Desktop → **Settings → WSL Integration → Ubuntu ON** |
| **4** | Open **Ubuntu** and run the commands below |

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/tgollogly/ReclaimKit.git ~/reclaimkit
cd ~/reclaimkit
chmod +x scripts/wsl-setup-and-test.sh
./scripts/wsl-setup-and-test.sh
```

> [!TIP]
> Pass = output shows **`SETUP COMPLETE`**

<details>
<summary><strong>PowerShell one-liner</strong> <img src="https://img.shields.io/badge/click-to-expand-64748b?style=flat-square" alt="expand" /></summary>

```powershell
wsl -d Ubuntu bash -c "sudo apt update && sudo apt install -y git && git clone https://github.com/tgollogly/ReclaimKit.git ~/reclaimkit && cd ~/reclaimkit && chmod +x scripts/wsl-setup-and-test.sh && ./scripts/wsl-setup-and-test.sh"
```

</details>

### Linux / Mac

```bash
git clone https://github.com/tgollogly/ReclaimKit.git
cd ReclaimKit
pip install -r requirements.txt
python3 main.py init
python3 main.py doctor
python3 main.py daemon once --dry-run
python3 -m pytest tests/ -v
cd deploy && docker compose up -d --build
```

### Cloud VPS (24/7 automation)

```bash
git clone https://github.com/tgollogly/ReclaimKit.git ~/reclaimkit
cd ~/reclaimkit
cp config.example.yaml config.yaml && nano config.yaml
python3 main.py campaign init
cd deploy && docker compose up -d --build
./scripts/check-autosave.sh
```

See [deploy/VPS-GUIDE.md](deploy/VPS-GUIDE.md)

<br/>

## Configure (any country)

<p align="left">
  <img src="https://img.shields.io/badge/jurisdiction-GDPR-6366f1?style=flat-square" alt="GDPR" />
  <img src="https://img.shields.io/badge/jurisdiction-CCPA-0891b2?style=flat-square" alt="CCPA" />
  <img src="https://img.shields.io/badge/jurisdiction-LGPD-059669?style=flat-square" alt="LGPD" />
  <img src="https://img.shields.io/badge/jurisdiction-Custom-7c3aed?style=flat-square" alt="Custom" />
</p>

Edit `config.yaml`:

```yaml
subject:
  full_name: "Your Name"
  email: "you@example.com"
  country: "Your country"

jurisdiction:
  privacy_law: "GDPR"              # or CCPA, LGPD, etc.
  erasure_article: "Article 17"
  regulator_name: "your data protection authority"
  regulator_url: "https://example.com/complaint"
  google_delisting_region: "Your country"
```

> [!IMPORTANT]
> Regenerate letters after editing config: <code>python3 main.py campaign init</code>

<br/>

## Daily commands

> [!NOTE]
> Run from <code>~/reclaimkit/deploy</code> on laptop or VPS.

```bash
cd ~/reclaimkit/deploy
docker compose ps
docker compose run --rm reclaimkit python3 main.py campaign status
docker compose run --rm reclaimkit python3 main.py campaign sent --track meta --round 1
```

<br/>

## Autosave

<p align="left">
  <img src="https://img.shields.io/badge/persistence-enabled-059669?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Persistence enabled" />
</p>

Docker bind-mounts your data to disk — closing the terminal does **not** delete anything:

| Saved | Path |
|-------|------|
| <img src="https://img.shields.io/badge/type-config-6366f1?style=flat-square" alt="config" /> | `~/reclaimkit/config.yaml` |
| <img src="https://img.shields.io/badge/type-output-0891b2?style=flat-square" alt="output" /> | `~/reclaimkit/output/` |
| <img src="https://img.shields.io/badge/type-evidence-7c3aed?style=flat-square" alt="evidence" /> | `~/reclaimkit/evidence/` |

Verify: `./scripts/check-autosave.sh`

<br/>

## Laptop vs VPS

<table>
<thead>
<tr>
<th align="left"></th>
<th align="center"><img src="https://img.shields.io/badge/Laptop-Local-6366f1?style=flat-square" alt="Laptop" /></th>
<th align="center"><img src="https://img.shields.io/badge/VPS-Cloud-2563eb?style=flat-square" alt="VPS" /></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Cost</strong></td>
<td align="center"><img src="https://img.shields.io/badge/-Free-059669?style=flat-square" alt="Free" /></td>
<td align="center"><img src="https://img.shields.io/badge/-~$5%2Fmo-d97706?style=flat-square" alt="~$5/mo" /></td>
</tr>
<tr>
<td><strong>Runs when PC off?</strong></td>
<td align="center"><img src="https://img.shields.io/badge/-No-dc2626?style=flat-square" alt="No" /></td>
<td align="center"><img src="https://img.shields.io/badge/-Yes-059669?style=flat-square" alt="Yes" /></td>
</tr>
<tr>
<td><strong>Best for</strong></td>
<td align="center">Setup, editing, sending Round 1</td>
<td align="center">Background monitoring</td>
</tr>
</tbody>
</table>

<br/>

## Documentation

| Guide | Purpose |
|-------|---------|
| <img src="https://img.shields.io/badge/QUICK--START-0891b2?style=flat-square" alt="QS" /> [docs/QUICK-START.md](docs/QUICK-START.md) | Minimum steps |
| <img src="https://img.shields.io/badge/WINDOWS-0078D4?style=flat-square&logo=windows&logoColor=white" alt="Win" /> [docs/WINDOWS-WSL-DOCKER.md](docs/WINDOWS-WSL-DOCKER.md) | Windows setup |
| <img src="https://img.shields.io/badge/AUTO--EMAIL-7c3aed?style=flat-square" alt="Email" /> [docs/AUTO-EMAIL-SETUP.md](docs/AUTO-EMAIL-SETUP.md) | Optional SMTP |
| <img src="https://img.shields.io/badge/VPS-2563eb?style=flat-square&logo=digitalocean&logoColor=white" alt="VPS" /> [deploy/VPS-GUIDE.md](deploy/VPS-GUIDE.md) | Cloud server |
| <img src="https://img.shields.io/badge/COMPLETE-6366f1?style=flat-square" alt="Full" /> [docs/COMPLETE-GUIDE.md](docs/COMPLETE-GUIDE.md) | Full walkthrough |

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/MIT%20License-ReclaimKit%20contributors-1e3a5f?style=for-the-badge" alt="MIT License" />
</p>

<p align="center">
  <sub>Not legal advice · Not affiliated with Meta, Google, or any reputation-management service</sub>
</p>

<p align="center">
  <sub>See <a href="LICENSE">LICENSE</a> · Copyright © 2026 ReclaimKit contributors</sub>
</p>

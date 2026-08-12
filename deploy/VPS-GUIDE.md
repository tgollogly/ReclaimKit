# Cheap VPS guide — ReclaimKit + other automations

Run ReclaimKit daily monitoring on a small VPS (~£4–6/month). Same server can host other Docker tools, scripts, and self-hosted AI.

## Recommended providers (EU/US — pick a region near you)

| Provider | Price | Specs (typical) | Best for |
|----------|-------|-----------------|----------|
| **[Hetzner Cloud](https://www.hetzner.com/cloud)** | **~£4.50/mo** (CX22) | 2 vCPU, 4 GB RAM, 40 GB SSD, EU datacentres | **Best value** — Docker, cron, multiple containers |
| **[DigitalOcean](https://www.digitalocean.com/)** | **~$6/mo** | 1 vCPU, 1 GB RAM (basic droplet) | Simple UI, good docs |
| **[Vultr](https://www.vultr.com/)** | **~$6/mo** | 1 vCPU, 1 GB RAM | Many regions |
| **[Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)** | **£0** (always free) | Up to 4 ARM cores, 24 GB RAM (if approved) | Free but signup/setup can be awkward |

**Recommendation:** **Hetzner CX22** (~€4.59/month) — enough RAM for ReclaimKit + Docker Compose stack + lightweight automation.

## What fits on one £5 VPS

| Service | RAM | Notes |
|---------|-----|-------|
| ReclaimKit (Docker cron) | ~100 MB | This repo — daily monitor + Slack |
| **Ollama** (free local AI) | 2–4 GB | Run Llama/Mistral — needs CX22 or larger |
| n8n / Node-RED | ~512 MB | Workflow automation |
| Uptime Kuma | ~128 MB | Site monitoring |
| WireGuard VPN | ~64 MB | Secure remote access |
| Static websites | minimal | nginx + small apps |

Use **Docker Compose** to run several services on one VPS.

## Free AI on a VPS

| Option | Cost | Setup |
|--------|------|-------|
| **Ollama** (self-hosted) | Free (your VPS cost) | `curl -fsSL https://ollama.com/install.sh \| sh` then `ollama run llama3.2` |
| **OpenRouter free tier** | Free API credits | Call from Python scripts on VPS |
| **Google Gemini API** | Free tier limits | API key in `.env` |

For ReclaimKit itself you do **not** need AI — letters are pre-written templates.

## Quick Hetzner setup

1. Create account at hetzner.com → Cloud → Create server (Ubuntu 24.04, CX22, Falkenstein or Helsinki)
2. SSH in: `ssh root@YOUR_IP`
3. Install Docker:

```bash
apt update && apt install -y git docker.io docker-compose-v2
git clone https://github.com/tgollogly/ReclaimKit.git ~/reclaimkit
cd ~/reclaimkit
cp config.example.yaml config.yaml
nano config.yaml                   # real email, meta_reports, post_origin: uncertain
mkdir -p evidence/screenshots output
python3 main.py init 2>/dev/null || pip3 install -r requirements.txt
python3 main.py campaign init
python3 main.py campaign sent --track meta --round 1
cd deploy && docker compose up -d --build
./scripts/check-autosave.sh        # verify autosave
```

4. Slack webhook in `config.yaml` for daily alerts
5. Optional `.env` for SMTP auto-email

## Data persistence (auto-save)

**Enabled by default.** Docker bind-mounts host folders — nothing is stored only inside the container.

| Host path (laptop or VPS) | What is saved |
|---------------------------|---------------|
| `~/reclaimkit/config.yaml` | Your details |
| `~/reclaimkit/output/` | Letters, `campaign/state.json`, cron logs |
| `~/reclaimkit/evidence/` | Screenshots |

Verify anytime:

```bash
cd ~/reclaimkit && ./scripts/check-autosave.sh
```

See `deploy/docker-compose.yml` and `deploy/README.md`.

## Security

- SSH keys only (disable password login)
- Firewall: `ufw allow 22 && ufw enable`
- Never commit `config.yaml` or `.env`
- Keep VPS patched: `apt upgrade -y` weekly

## Cost summary

| Item | Monthly |
|------|---------|
| Hetzner CX22 | ~£4.50 |
| ReclaimKit software | £0 |
| SerpAPI (optional image search) | $0–50 |
| **Total minimum** | **~£5** |

Compare to Removify: **£400–£2,000 per item**.

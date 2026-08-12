# ReclaimKit — Quick Start

Remove harmful social content and search results using privacy erasure requests.

## 1. Install

```bash
git clone https://github.com/tgollogly/ReclaimKit.git
cd ReclaimKit
pip install -r requirements.txt
python3 main.py init
```

## 2. Configure

Edit `config.yaml` — your name, email, country, and `jurisdiction` block (privacy law + regulator for your country).

Copy screenshots → `evidence/screenshots/`

## 3. Test

```bash
python3 main.py campaign init
python3 main.py doctor
python3 main.py daemon once --dry-run
python3 -m pytest tests/ -v
./scripts/check-autosave.sh
```

## 4. Deploy (Docker)

```bash
cd deploy && docker compose up -d --build
docker compose ps
```

## 5. Email platform privacy team

Open `output/campaign-package-.../round-01-meta/meta_r1_erasure_initial.txt`

Email **privacy@facebook.com** with screenshots, then:

```bash
docker compose run --rm reclaimkit python3 main.py campaign sent --track meta --round 1
```

## 6. Optional VPS

See [deploy/VPS-GUIDE.md](../deploy/VPS-GUIDE.md) (~$5/mo for 24/7 automation).

---

| Doc | Purpose |
|-----|---------|
| [README.md](../README.md) | Test & deploy all platforms |
| [WINDOWS-WSL-DOCKER.md](WINDOWS-WSL-DOCKER.md) | Windows setup |
| [AUTO-EMAIL-SETUP.md](AUTO-EMAIL-SETUP.md) | Optional auto-send |

```bash
./scripts/audit.sh    # full repo check
```

Not legal advice. Configure `jurisdiction` in config.yaml for your country's privacy law.

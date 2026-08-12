<p align="center">
  <img src="assets/reclaimkit-hero.png" alt="ReclaimKit — UK/NI Reputation Reclaim Toolkit" width="100%" />
</p>

<h1 align="center">ReclaimKit</h1>

<p align="center">
  <strong>UK/NI Reputation Reclaim Toolkit</strong><br/>
  Multi-round GDPR campaigns · Daily monitoring · Slack alerts · VPS-ready
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="MIT License" />
  <img src="https://img.shields.io/badge/region-UK%20%2F%20NI-teal?style=flat-square" alt="UK/NI" />
  <img src="https://img.shields.io/badge/cost-%240%20software-success?style=flat-square" alt="Free software" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square" alt="Python 3.10+" />
</p>

---

> **ReclaimKit** helps you fight harmful Facebook posts and Google search results using the same legal channels reputation firms use — **GDPR erasure, defamation delisting, ICO complaints** — without paying **£400–£2,000 per case**.

<table>
<tr>
<td width="50%" valign="top">

### 🟢 What ReclaimKit does

- **6-round Meta escalation** (GDPR → ICO)
- **3-round Google delisting** drafts
- **Daily web + image monitoring**
- **Slack notifications** on new hits
- **VPS / Docker** deployment
- **Optional auto-email** to Meta

</td>
<td width="50%" valign="top">

### 🔴 What no software can do

- Force-delete Facebook posts instantly
- Auto-submit Google web forms (no API)
- Scrape private groups
- Guarantee removal — platforms decide

</td>
</tr>
</table>

---

## 💷 What removal services charge

| Service | Typical cost | Model |
|---------|-------------|--------|
| **Removify** | **£400–£2,000** (~$500–$2,500) per item | No win, no fee + deposit |
| **Erase.com** | **£800–£2,000+** per item | Custom quote |
| **Guaranteed Removals** | **£600–£1,500** per item | Pay on success |
| **NI solicitor** | **£500–£5,000+** | Hourly / letter before action |
| **ReclaimKit** | **£0** software · **~£5/mo** optional VPS | You run the same process |

Paid services submit the **same forms and emails** ReclaimKit generates — their value is persistence and wording. ReclaimKit automates that for you.

Sources: [Removify FAQ](https://removify.com/faq/how-much-does-it-cost-to-remove-a-google-review/), [industry comparison](https://www.truereview.co/post/removify-vs-erase-vs-guaranteed-removals-honest-comparison).

---

## 📖 Full documentation

| Guide | Links |
|-------|-------|
| **Quick Start** | [MD](docs/QUICK-START.md) · [PDF](docs/QUICK-START.pdf) |
| **Complete Guide** | [MD](docs/COMPLETE-GUIDE.md) · [PDF](docs/COMPLETE-GUIDE.pdf) |
| **Auto-email (free Gmail)** | [MD](docs/AUTO-EMAIL-SETUP.md) · [PDF](docs/AUTO-EMAIL-SETUP.pdf) |
| **VPS setup** | [MD](deploy/VPS-GUIDE.md) · [PDF](docs/VPS-GUIDE.pdf) |

```bash
./scripts/audit.sh          # verify codebase
./scripts/build-all-pdfs.sh # rebuild all PDFs
```

---

## ⚡ Quick start

```bash
git clone https://github.com/tgollogly/stop-assholes.git
cd stop-assholes
pip install -r requirements.txt
python3 main.py init
```

1. Edit **`config.yaml`** — your email, address, Slack webhook  
2. Add screenshots to **`evidence/screenshots/`**  
3. Run **`python3 main.py campaign init`**  
4. Email Meta using **`output/campaign-package-.../round-01-meta/`**  
5. Track: **`python3 main.py campaign sent --track meta --round 1`**

---

## 📋 Campaign rounds

<table>
<thead>
<tr><th>Track</th><th>Rounds</th><th>Trigger</th></tr>
</thead>
<tbody>
<tr><td><strong>Meta</strong></td><td>6</td><td>GDPR → reminder → Trust & Safety → rebuttal → ICO notice → post-ICO</td></tr>
<tr><td><strong>Google</strong></td><td>3</td><td>Defamation → personal info → resubmit with case history</td></tr>
<tr><td><strong>ICO</strong></td><td>1</td><td>After Meta round 4+ or 30 days without removal</td></tr>
</tbody>
</table>

Each letter includes a case reference (e.g. `TG-ER-THOMAS-GOLLO-META-R1`).

---

## 🖥️ Commands

| Command | Purpose |
|---------|---------|
| `init` | Create `config.yaml` and evidence folders |
| `evidence` | Build hashed evidence pack |
| `letters` | Generate standalone takedown letters |
| `campaign init` | Start campaign + Round 1 package |
| `campaign status` | Show progress dashboard |
| `campaign sent --track meta --round N` | Record submission |
| `campaign no-response --track meta` | 7-day silence → next round |
| `campaign refused --track meta --reason "..."` | Refusal → rebuttal |
| `campaign next --track meta --round N` | Generate specific round |
| `campaign success` | Mark content removed |
| `monitor` | Scan search for indexed URLs |
| `osint` | Document commenter handles |
| `guide` | Print removal action guide |
| `close` | Facebook closure checklist |
| `doctor` | Validate config, deps, letters |
| `daemon once` | Daily automation cycle |
| `daemon once --dry-run` | Test automation without writes |
| `all` | Evidence + campaign + osint + monitor |

VPS deploy: **`deploy/README.md`** · **`deploy/VPS-GUIDE.md`** (cheap servers + free AI)

---

## 🔔 VPS automation (~£5/month)

```bash
cd deploy && docker compose up -d --build
```

| Automated daily | Manual (~2 min when Slack pings) |
|-----------------|----------------------------------|
| Name search | Google removal web forms |
| Photo search (SerpAPI/TinEye) | — |
| Slack alerts | — |
| Next Meta letter / email | — |

---

## 🧪 Test & verify

```bash
python3 -m pytest tests/ -v      # 20 automated tests
python3 main.py doctor             # validate your setup
python3 main.py --config config.example.yaml doctor
./scripts/audit.sh                 # full repo audit
python3 main.py daemon once --dry-run
```

Use `.env.example` for VPS secrets (`RECLAIMKIT_SMTP_PASSWORD`, etc.) instead of storing passwords in `config.yaml`.

---

## 📄 License

**MIT License** — Copyright © 2026 **Thomas Gollogly**. You made this; you own it.

See **[LICENSE](LICENSE)** for full terms. Free to use, modify, and distribute with attribution.

> ReclaimKit is independent — not affiliated with Meta, Google, Removify, or any reputation service. Templates are not legal advice.

---

<p align="center">
  <sub>Built in Northern Ireland · GDPR Article 17 · Defamation Act (NI) 2022</sub>
</p>

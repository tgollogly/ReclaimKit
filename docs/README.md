# ReclaimKit documentation

| Document | Format | Description |
|----------|--------|-------------|
| **[Complete User Guide](COMPLETE-GUIDE.md)** | Markdown | Full step-by-step guide — setup, Meta GDPR campaign, Google, ICO, Facebook closure, FAQ |
| **[Complete User Guide (PDF)](COMPLETE-GUIDE.pdf)** | PDF | Same content, printable / offline |

## Quick links inside the guide

- [Will this work?](COMPLETE-GUIDE.md#1-will-this-work)
- [Day 1 — start the campaign](COMPLETE-GUIDE.md#7-day-1--start-the-campaign)
- [Send Round 1 to Meta](COMPLETE-GUIDE.md#8-how-to-send-round-1-to-meta)
- [Facebook login FAQ](COMPLETE-GUIDE.md#4-facebook-login--what-matters)
- [Close Facebook after removal](COMPLETE-GUIDE.md#12-closing-facebook-after-removal)
- [Meta rejected your report](COMPLETE-GUIDE.md#22-meta-rejected-your-report--what-now)
- [Community Standards vs GDPR](COMPLETE-GUIDE.md#21-community-standards-vs-gdpr)
- [Docker auto-save](COMPLETE-GUIDE.md#23-docker--does-it-auto-save)

## Regenerate the PDF

After editing `COMPLETE-GUIDE.md`:

```bash
./scripts/build-guide-pdf.sh
```

Requires `pandoc` and `wkhtmltopdf` (`sudo apt-get install pandoc wkhtmltopdf` on Debian/Ubuntu).

## Other docs

- [Main README](../README.md) — project overview and quick start
- [VPS deploy guide](../deploy/README.md) — Docker, cron, Slack, auto-email

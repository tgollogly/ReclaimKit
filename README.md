# Stop Assholes — Online Harassment Response Toolkit (UK/NI)

A command-line toolkit to help **Thomas Gollogly** (and others in similar situations) respond to harmful Facebook posts and Google search results under **Northern Ireland / UK law**.

## What this does

| Command | Purpose |
|---------|---------|
| `python main.py init` | Create `config.yaml` and evidence folders |
| `python main.py evidence` | Hash and package screenshots for solicitors/PSNI |
| `python main.py letters` | Generate Meta GDPR + Google removal letter drafts |
| `python main.py osint` | Document commenter handles and **legal** ID pathways |
| `python main.py monitor` | Scan public search for indexed harmful URLs |
| `python main.py guide` | Print NI legal action guide |
| `python main.py all` | Run the full workflow |

## What this cannot do

**No software can automatically remove content from Facebook, Google, or "the whole internet."** Removal requires:

1. Platform reports and formal legal requests (this tool generates those)
2. Google delisting (hides from search — does not delete Facebook posts)
3. PSNI investigation and/or NI High Court orders (for identifying anonymous posters)

Attempting to "hack" or scrape Facebook violates law and platform terms.

## Quick start

```bash
pip install -r requirements.txt
python main.py init
# Edit config.yaml — add your email, address, Facebook post URL
# Copy your screenshots into evidence/screenshots/
python main.py all
```

Review everything in the `output/` folder.

## Your case (pre-filled in config.example.yaml)

- **Group:** AreWeDatingTheSameGuy? Northern Ireland
- **Post:** Anonymous, 5 June — "Any red flags Thomas gollogly" + your photo
- **Comments:** False allegations (drugging, sexual misconduct) plus gossip

Documented commenter handles:

| Handle | Type | Identity via public OSINT? |
|--------|------|---------------------------|
| BrightPanda3834 | Auto-style pseudonym | No — needs Meta disclosure |
| IntelligentJaguar6700 | Auto-style pseudonym | No |
| EmpatheticPeapod4820 | Auto-style pseudonym | No |
| Anonymous participant 617 | Facebook anonymous | No |
| Keerzo Diesel | Possible real display name | Only via legal process |
| Pieter James | Possible real display name | Only via legal process |

## Priority actions (do these today)

### 1. Meta — UK GDPR Article 17

Email **privacy@facebook.com** with the generated letter (`01_meta_gdpr_article17.txt`).

Also submit via: Facebook → Settings → Privacy → Access and control your info.

**Deadline for Meta to respond: 1 month.**

### 2. Meta — Escalation

If your in-app report was ignored: https://www.facebook.com/help/contact/571927962827151

Use `02_meta_defamation_escalation.txt`.

### 3. Google — Delisting

- **Defamation:** https://support.google.com/legal/troubleshooter/1114905
- **Personal info / image without consent:** https://support.google.com/websearch/contact/content_removal_form
- **Monitor your name:** https://myactivity.google.com/results-about-you

Run `python main.py monitor` to find URLs to include.

### 4. PSNI (if content stays up)

False criminal allegations may be reportable. Call **101** with your evidence pack.

Ask about malicious communications and harassment under NI law.

### 5. Solicitor (if Meta refuses after 30 days)

NI defamation law differs from England & Wales. A solicitor can:

- Send a Letter Before Action
- Apply for a **Norwich Pharmacal order** forcing Meta to reveal anonymous poster identities
- Pursue damages under the Defamation Act (Northern Ireland) 2022

## Legal references

- [Defamation Act (Northern Ireland) 2022](https://www.legislation.gov.uk/nia/2022/30/enacted)
- [ICO — Right to erasure](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/)
- [Ask the Police — false social media posts](https://www.askthe.police.uk/faq/?id=10c5af20-a1e8-ec11-bb3c-000d3a0afe35)
- [Google defamation removal](https://support.google.com/legal-help-center/answer/16833565)

## Support contacts

- **Citizens Advice NI:** 0800 915 4605
- **ICO:** 0303 123 1113 — https://ico.org.uk/make-a-complaint/
- **PSNI non-emergency:** 101

---

*This toolkit provides information and document templates only. It is not legal advice.*

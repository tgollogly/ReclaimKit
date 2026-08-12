from __future__ import annotations


def print_legal_guide(no_police: bool = True) -> str:
    if no_police:
        return _removal_only_guide()
    return _full_guide()


def print_close_facebook_guide() -> str:
    return """
╔══════════════════════════════════════════════════════════════════════════════╗
║  REMOVE CONTENT, THEN CLOSE FACEBOOK — STEP BY STEP                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Do these in order. Do NOT delete your account until removal is confirmed or
you have exhausted Meta's GDPR process — you may lose access to report links.

STEP 1 — SUBMIT REMOVAL REQUESTS (before closing account)
---------------------------------------------------------
  □ Run: python3 main.py letters
  □ Email privacy@facebook.com with 01_meta_gdpr_article17.txt
  □ Submit escalation: facebook.com/help/contact/571927962827151
  □ Keep screenshots in evidence/screenshots/ (already have these)
  □ Save Meta's reply emails — you need proof if you escalate to your data protection authority

STEP 2 — GOOGLE (parallel, works without Facebook account)
----------------------------------------------------------
  □ Run: python3 main.py monitor
  □ Submit any harmful URLs via Google's forms (see output/takedown-letters/)
  □ Enable "Results about you": myactivity.google.com/results-about-you

STEP 3 — WAIT FOR META (up to 1 month for GDPR)
-----------------------------------------------
  □ Check the group post is gone (ask someone still in the group, or check
    before you close — you won't see it after deactivation)
  □ If no response in 2 weeks, send the escalation letter again
  □ If refused after 30 days: your data protection authority complaint (no police needed)
        https://your-regulator-url/make-a-complaint/

STEP 4 — CLOSE FACEBOOK (after removal confirmed OR after GDPR deadline)
------------------------------------------------------------------------
  Deactivate (reversible, 30 days) vs Delete (permanent):

  DEACTIVATE (temporary — profile hidden, can log back in):
    Settings & privacy → Settings → Accounts Centre → Personal details
    → Account ownership and control → Deactivation or deletion

  DELETE PERMANENTLY:
    Same path → Delete account → Confirm

  Before deleting:
    □ Download your data: Settings → Download your information
    □ Remove apps connected to Facebook (Settings → Apps and websites)
    □ Update logins on sites where you used "Log in with Facebook"
    □ Save any evidence / report reference numbers locally first

  Note: Deleting your account does NOT remove the group post. The post must
  be removed by Meta while your request is active, or via GDPR/your data protection authority pressure.

STEP 5 — ONGOING (after Facebook is closed)
-------------------------------------------
  □ Run python3 main.py monitor monthly for 3–6 months
  □ Re-submit Google delisting if new URLs appear
  □ If post reappears on another site, use same Google + GDPR approach

WHAT YOU ARE NOT DOING (by choice — that's fine)
-------------------------------------------------
  ✗ local law enforcement / police report
  ✗ Court / solicitor (unless Meta and your data protection authority both fail)
  ✗ Confronting commenters

Support without police:
  your data protection authority (data protection): your-regulator-url | 0303 123 1113
  Citizens Advice NI: 0800 915 4605
"""


def _removal_only_guide() -> str:
    return """
╔══════════════════════════════════════════════════════════════════════════════╗
║  REMOVAL-ONLY GUIDE — NO POLICE                                              ║
║  Get content removed → close Facebook → monitor Google                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

YOUR GOAL
---------
Remove the post and comments, delist from Google if indexed, then close Facebook.
You do not need police involvement for this path.

PRIORITY ORDER
--------------
1. python3 main.py letters     → generate Meta GDPR + Google drafts
2. Email privacy@facebook.com  → starts 1-month applicable privacy law clock
3. Escalation form if ignored  → facebook.com/help/contact/571927962827151
4. python3 main.py monitor      → check Google, submit delisting if needed
5. Confirm removal             → then python3 main.py close for account steps
6. your data protection authority if Meta refuses (30 days) → your-regulator-url/make-a-complaint/  (no police)

┌─────────────────────────────────────────────────────────────────────────────┐
│ META REMOVAL (main lever)                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ • applicable privacy law Article 17 — your photo + name used without consent                │
│ • False allegations in comments — unlawful processing causing harm           │
│ • Meta must respond within 1 calendar month                                  │
│ • Escalation if in-app report was ignored                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ GOOGLE (after Meta — hides from search, not source)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Defamation: support.google.com/legal/troubleshooter/1114905                │
│ • Personal info: support.google.com/websearch/contact/content_removal_form   │
│ • Works even after you delete Facebook                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ IF META REFUSES — your data protection authority, NOT POLICE                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Complaint to Information Commissioner's Office                             │
│ • Free, no court, no police                                                  │
│ • Reference your GDPR request date and Meta's refusal                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ CLOSE FACEBOOK — run: python3 main.py close                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Wait for removal OR send GDPR request first (needs active account to       │
│   track; evidence pack preserves everything offline)                         │
│ • Deleting Facebook does NOT remove the group post — Meta must delete it     │
└─────────────────────────────────────────────────────────────────────────────┘

WHAT NO SOFTWARE CAN DO
-----------------------
• Force instant removal — Meta has up to 1 month for GDPR
• Remove from every website — focus Meta + Google covers 99% of visibility

Run: python3 main.py close  — full Facebook closure checklist
"""


def _full_guide() -> str:
    return _removal_only_guide() + """

OPTIONAL ROUTES (not in your removal-only plan)
-----------------------------------------------
• local law enforcement 101 — only if you later want criminal investigation
• local solicitor — only if Meta + your data protection authority both fail and you want court action
"""

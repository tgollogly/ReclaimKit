from __future__ import annotations

from pathlib import Path


def print_legal_guide() -> str:
    guide = """
╔══════════════════════════════════════════════════════════════════════════════╗
║  NORTHERN IRELAND — ONLINE DEFAMATION & HARASSMENT ACTION GUIDE              ║
║  (Information only — not legal advice. Consult a NI solicitor.)              ║
╚══════════════════════════════════════════════════════════════════════════════╝

YOUR SITUATION
--------------
Private Facebook group post with your photo + name + false criminal allegations.
This can be addressed through multiple parallel routes:

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROUTE 1: META REMOVAL (fastest if successful)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ • In-app report (you've done this — good)                                     │
│ • UK GDPR Article 17 email to privacy@facebook.com (use generated letter)     │
│ • Escalation form: facebook.com/help/contact/571927962827151                  │
│ • Timeline: Meta must respond to GDPR requests within 1 month                  │
│ • If refused: complain to ICO (ico.org.uk/make-a-complaint)                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROUTE 2: GOOGLE DELISTING (hides from search, not source)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Defamation form: support.google.com/legal/troubleshooter/1114905          │
│ • Personal info form: support.google.com/websearch/contact/content_removal  │
│ • "Results about you": myactivity.google.com/results-about-you                │
│ • Effect: URLs hidden from Google.co.uk — content may still exist on Facebook │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROUTE 3: CRIMINAL (PSNI) — for false criminal allegations                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Call 101 or visit station with evidence pack                                │
│ • False allegations of drugging / sexual offences may be:                     │
│     - Malicious Communications (Communications Act 2003 s.127)                │
│     - Harassment (Protection from Harassment (NI) Order 1997)                 │
│ • PSNI CAN request poster identities from Meta (you cannot via OSINT)         │
│ • Askthe.police.uk NI FAQ: askthe.police.uk                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROUTE 4: CIVIL DEFAMATION (NI High Court)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Defamation Act (Northern Ireland) 2022                                      │
│ • You must prove statements are false and caused serious harm                 │
│ • Solicitor can send Letter Before Action to Meta + anonymous posters         │
│ • Norwich Pharmacal order: court compels Meta to reveal poster identities     │
│ • NI differs from England & Wales — use NI-experienced media solicitor        │
│ • Examples: Phoenix Law Belfast, Carson McDowell, Tughan & Co                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ROUTE 5: IDENTIFYING ANONYMOUS COMMENTERS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ WHAT THIS TOOL CAN DO:                                                        │
│   • Document handles (BrightPanda3834, Keerzo Diesel, etc.)                   │
│   • Classify which are anonymous vs possible real names                         │
│   • Prepare evidence for police/solicitor                                       │
│                                                                               │
│ WHAT YOU CANNOT DO LEGALLY YOURSELF:                                          │
│   • "OSINT doxing" — tracing people via private data is risky and may be      │
│     illegal under UK GDPR and harassment law                                  │
│   • Automated scraping of Facebook — violates ToS and may be unlawful         │
│                                                                               │
│ REALISTIC PATH TO IDENTITIES:                                                 │
│   • PSNI investigation → Meta disclosure                                      │
│   • Civil court order (Norwich Pharmacal) → Meta reveals account details     │
│   • Handles like "Keerzo Diesel" / "Pieter James" may be real display names  │
│     — note these for your solicitor; still need Meta to confirm                 │
└─────────────────────────────────────────────────────────────────────────────┘

PRIORITY ORDER (recommended)
----------------------------
1. Run this tool: evidence pack + takedown letters + monitor
2. Email Meta GDPR letter TODAY (starts 1-month clock)
3. Submit Google removal for any URLs found in monitor report
4. PSNI report if criminal allegations remain after 7 days
5. Solicitor consultation if Meta does not remove within 30 days

WHAT NO SOFTWARE CAN DO
-----------------------
• Force Facebook/Google to delete content instantly
• Access private group data without your login
• Reliably identify anonymous Facebook users from public internet alone
• Remove content from "the whole internet" — each platform requires separate action

CITIZENS ADVICE NI: 0800 915 4605 | citizensadvice.org.uk/ni
ICO (data protection): ico.org.uk | 0303 123 1113
PSNI non-emergency: 101
"""
    return guide

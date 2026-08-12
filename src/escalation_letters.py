"""
Multi-round escalation letter templates.

Each round increases legal specificity and pressure through legitimate channels only.
"""

from __future__ import annotations

from typing import Any, Callable

from src.letter_context import (
    case_ref,
    comment_block,
    false_allegations_summary,
    post_details,
    subject_line,
    today_long,
)

LetterFn = Callable[[dict[str, Any], dict[str, Any]], str]


def _header(ref: str, subject: str) -> str:
    return f"Case Reference: {ref}\nDate: {today_long()}\nSubject: {subject}\n"


# ---------------------------------------------------------------------------
# META TRACK — Rounds 1–6
# ---------------------------------------------------------------------------


def meta_round_1_gdpr_initial(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R1")

    return f"""{_header(ref, f"UK GDPR Article 17 — Right to Erasure — {sub['name']}")}

To:      Data Protection Officer
         Meta Platforms Ireland Limited
         Merrion Road, Dublin 4, D04 X2K5, Ireland
Email:   privacy@facebook.com
CC:      dpo@facebook.com

Dear Data Protection Officer,

FORMAL DATA SUBJECT REQUEST — ARTICLE 17 UK GDPR

I, {sub['name']}, a data subject resident in Northern Ireland, United Kingdom,
 hereby exercise my right to erasure under Article 17 of the UK General Data
Protection Regulation (UK GDPR) and section 47 of the Data Protection Act 2018.

Please treat this as a formal request requiring a response within one calendar
month under Article 12(3) UK GDPR.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PERSONAL DATA REQUIRING ERASURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(a) My photograph (selfie), published without my knowledge or consent;
(b) My personal name — "{sub['name']}" / "Thomas gollogly" — in connection with
    that image and defamatory commentary;
(c) All comments that identify, describe, or publish false statements about me;
(d) Metadata linking my identity to this content (including group post indexing).

{false_allegations_summary()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. PRECISE LOCATION OF DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Platform:     Facebook
Group:        {post['group']}
Post date:    {post['date']}
Post caption: "{post['caption']}"
Direct URL:   {post['url']}

Comments containing my personal data / false allegations:
{comment_block(config)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. LEGAL GROUNDS (Article 17(1) UK GDPR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(a) Article 17(1)(a) — Data no longer necessary: The post serves no legitimate
    purpose regarding me. I am not a party to any proceedings; no public-interest
    justification exists for publishing my image with solicited "red flags."

(b) Article 17(1)(c) — Withdrawal of consent: I never consented to this processing.
    No lawful basis under Article 6 applies to publishing my likeness and name in
    this context.

(c) Article 17(1)(d) — Objection: I object under Article 21. The processing causes
    disproportionate harm to my rights, dignity, and reputation as a private individual
    in Northern Ireland.

(d) Article 17(1)(e) — Unlawful processing: Publication of my image without consent,
    combined with false criminal allegations, constitutes unlawful processing.

Article 17(2) requires you to take reasonable steps to inform other controllers of
this erasure request where data has been made public.

Article 19 requires you to communicate erasure to recipients unless impossible or
 involving disproportionate effort.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. PRIOR REPORTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I have reported this content through Meta's in-app reporting tools. Content remains
live. This formal Article 17 request is without prejudice to my other legal rights.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. REQUESTED ACTIONS (within one month)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Permanently delete the post at the URL above, my photograph, and all comments;
2. Confirm deletion in writing to {sub['email']}, quoting reference {ref};
3. Confirm compliance with Articles 17(2) and 19 UK GDPR;
4. If refusing, provide specific reasons under Article 12(4) and identify the
   Article 17(3) exemption relied upon.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. DATA SUBJECT IDENTIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Full name:  {sub['name']}
Email:      {sub['email']}
Telephone:  {sub['phone']}
Address:
{sub['address']}

I will provide photographic identification upon request.

Yours faithfully,

{sub['name']}

---
Send to: privacy@facebook.com
Attach: screenshots from evidence/screenshots/
Quote case reference {ref} in all correspondence.
"""


def meta_round_2_gdpr_reminder(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R2")
    r1_date = ctx.get("meta_r1_sent", "[DATE OF ROUND 1 EMAIL]")
    r1_ref = case_ref(config, "META-R1")

    return f"""{_header(ref, f"REMINDER — Article 12(3) UK GDPR Deadline — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Dear Data Protection Officer,

Re: {r1_ref} — Article 17 erasure request dated {r1_date}
    Content URL: {post['url']}

I refer to my formal Article 17 request ({r1_ref}) sent on {r1_date}. I have received
{"no acknowledgement" if not ctx.get("meta_r1_ack") else "no substantive response"}.

Under Article 12(3) UK GDPR, you must respond without undue delay and in any event
within one month of receipt. That deadline is approaching or has passed.

The personal data identified in my original request remains publicly accessible.
Each day of continued processing causes further reputational and psychological harm.

IMMEDIATE ACTION REQUIRED
-------------------------
1. Confirm receipt of this reminder and provide your internal case reference;
2. Complete erasure of the post, image, name, and all comments at:
   {post['url']}
3. Provide written confirmation to {sub['email']} within 7 days.

Failure to respond lawfully will result in:
• A complaint to the Information Commissioner's Office under Article 77 UK GDPR;
• Escalation to Meta Trust & Safety with documented non-compliance;
• Reservation of all rights under the Defamation Act (Northern Ireland) 2022.

This is not a new request — it is a formal reminder of your existing obligation.

Yours faithfully,

{sub['name']}
Case reference: {ref} (links to {r1_ref})
"""


def meta_round_3_trust_safety(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R3")

    return f"""{_header(ref, f"TRUST & SAFETY ESCALATION — Policy Violations — {sub['name']}")}

Submit via: https://www.facebook.com/help/contact/571927962827151
Also email: privacy@facebook.com (Subject: {ref})

To: Meta Trust & Safety / Content Policy Enforcement

ESCALATION — CONTENT REMAINS LIVE DESPITE GDPR REQUEST AND IN-APP REPORTS

Complainant:     {sub['name']} ({sub['email']})
Case reference: {ref}
Post URL:        {post['url']}
Group:           {post['group']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIOLATIONS REQUIRING REMOVAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. COMMUNITY STANDARDS — Harassment and Bullying
   The post targets a named private individual with my photograph and solicits
   damaging commentary. This is coordinated harassment, not legitimate discussion.

2. COMMUNITY STANDARDS — Privacy Violations
   My image was published without consent in a context designed to expose and
   humiliate me.

3. COMMUNITY STANDARDS — Dangerous Organizations and Individuals / Violence
   Comments falsely attribute criminal conduct (drugging drinks, sexual offences).
   These are not opinions — they are false factual claims causing real-world harm.

4. UK GDPR — Unlawful processing (see {case_ref(config, 'META-R1')})
   Formal Article 17 request remains unresolved.

5. DEFAMATION ACT (NORTHERN IRELAND) 2022
   Statements convey serious criminal imputations that are false. I am a private
   individual, not a public figure. No public-interest defence applies.

DOCUMENTED COMMENTS (false allegations on record):
{comment_block(config)}

{false_allegations_summary()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION REQUIRED WITHIN 72 HOURS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Remove post and all comments at: {post['url']}
□ Restrict accounts posting demonstrably false criminal allegations
□ Confirm removal to {sub['email']} quoting {ref}

Continued publication after documented notice increases my losses and strengthens
any regulatory or civil action. I require source removal — not merely visibility
reduction.

Yours faithfully,

{sub['name']}
"""


def meta_round_4_gdpr_rebuttal(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R4")
    refusal = ctx.get("refusal_reason", "[INSERT META'S STATED REASON FOR REFUSAL]")

    return f"""{_header(ref, f"FORMAL REBUTTAL OF REFUSAL — Article 17 UK GDPR — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Dear Data Protection Officer,

Re: Your refusal / inadequate response regarding {case_ref(config, 'META-R1')}
    Post URL: {post['url']}

I reject your position that erasure is not required. My detailed rebuttal follows.

YOUR STATED POSITION (or effective position by non-removal):
{refusal}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REBUTTAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Article 17(3)(a) — Freedom of expression does NOT apply here.

   The EDPB and ICO guidance confirm that the right to erasure must be balanced
   against expression rights. That balance favours erasure where:
   • The data subject is a private individual (I am not a public figure);
   • The content contains false, serious criminal allegations;
   • The processing serves no journalistic, academic, or public-interest purpose;
   • The content was posted in a gossip group soliciting reputational harm.

   Anonymous "red flag" posts about private citizens are not protected public
   interest speech. They are targeted reputational attacks.

2. No legitimate interest under Article 6(1)(f) outweighs my rights.

   Meta cannot rely on legitimate interests to host my photograph and name alongside
   false claims of drugging and sexual misconduct. The harm is severe, documented,
   and ongoing.

3. Article 9 considerations — False sexual misconduct claims involve particularly
   sensitive imputations. Continued hosting is disproportionate.

4. Data Protection Act 2018, Schedule 2 Part 4 — No exemption applies to exempt
   Meta from erasure in these circumstances.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RENEWED DEMAND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I require immediate erasure of all data specified in {case_ref(config, 'META-R1')}.
Provide a substantive written response within 14 days addressing each point above.

If you maintain your refusal, I will file a formal complaint with the ICO citing:
• Failure to comply with Article 17;
• Failure to provide valid Article 17(3) exemption reasoning under Article 12(4);
• Continued unlawful processing causing documented harm.

Yours faithfully,

{sub['name']}
Case reference: {ref}
"""


def meta_round_5_pre_ico_notice(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R5")

    return f"""{_header(ref, f"FINAL NOTICE BEFORE ICO COMPLAINT — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Dear Data Protection Officer,

FINAL PRE-REGULATORY NOTICE

Case history:
  • {case_ref(config, 'META-R1')} — Article 17 request
  • {case_ref(config, 'META-R2')} — Article 12(3) reminder
  • {case_ref(config, 'META-R3')} — Trust & Safety escalation
  • {case_ref(config, 'META-R4')} — Formal rebuttal

Content STILL LIVE at: {post['url']}

You have failed to erase my personal data or provide a lawful exemption under
Article 17(3) UK GDPR with the specificity required by Article 12(4).

FINAL OPPORTUNITY
-----------------
Delete the post, photograph, name, and all comments within 7 days of this email.
Confirm in writing to {sub['email']}.

If erasure is not completed, I will submit a complaint to the Information
Commissioner's Office on day 8 without further notice. The complaint will include:

• Complete correspondence history;
• SHA-256 verified evidence pack;
• Screenshots proving ongoing publication;
• Request for ICO enforcement action under Article 58 UK GDPR.

This email constitutes fair notice. Continued processing after this notice may
aggravate any regulatory findings.

Yours faithfully,

{sub['name']}
Case reference: {ref}
"""


def meta_round_6_post_ico(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R6")
    ico_ref = ctx.get("ico_reference", "[ICO COMPLAINT REFERENCE WHEN RECEIVED]")

    return f"""{_header(ref, f"POST-ICO COMPLAINT — Continued Non-Compliance — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Dear Data Protection Officer,

Re: ICO complaint reference {ico_ref}
    Ongoing Article 17 breach — {post['url']}

I formally complained to the Information Commissioner's Office regarding your
failure to erase my personal data. That complaint reference is {ico_ref}.

Despite regulatory scrutiny, the content remains accessible. This demonstrates
continued non-compliance with UK GDPR and undermines your data protection obligations.

I require:
1. Immediate erasure pending ICO investigation;
2. Preservation of account logs relating to the post (standard regulatory hold);
3. Written confirmation to {sub['email']} and notification to the ICO of compliance.

I am also submitting updated Google delisting requests for any indexed URLs.

Regulatory and reputational costs of maintaining this content exceed any perceived
benefit of continued publication.

Yours faithfully,

{sub['name']}
Case reference: {ref}
"""


# ---------------------------------------------------------------------------
# GOOGLE TRACK — Rounds 1–3
# ---------------------------------------------------------------------------


def google_round_1_defamation(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "GOOG-R1")

    return f"""{_header(ref, "Google Legal Removal — Defamation — United Kingdom")}

Submit at: https://support.google.com/legal/troubleshooter/1114905
Select: Defamation → United Kingdom (Northern Ireland)

Complainant: {sub['name']}
Email: {sub['email']}
Jurisdiction: United Kingdom — complainant domiciled in Northern Ireland

URLS TO DELIST (add Google search result URL + underlying page URL):
  • {post['url']}
  • [Add any google.com/search?q=... URLs from: python3 main.py monitor]

STATEMENT OF FACT
-----------------
I am {sub['name']}, a private individual resident in Northern Ireland. Search results
for my name link to a Facebook group post in "{post['group']}" (dated {post['date']})
that publishes my photograph and name without consent alongside comments containing
false defamatory imputations of criminal and sexual misconduct.

WHY STATEMENTS ARE FALSE
------------------------
{false_allegations_summary()}

Each named comment in the post is demonstrably false gossip. No court has found
any basis for these claims. I have never been charged with or investigated for any
conduct described.

SERIOUS HARM
------------
The content is indexed against my name, causing direct reputational damage in my
professional and personal life in Northern Ireland. As a private individual, I have
a protectable reputation under UK and NI law including the Defamation Act
(Northern Ireland) 2022.

LEGAL BASIS FOR DELISTING
-------------------------
• UK defamation law — false statements causing serious reputational harm
• Google Legal Removals Policy — defamatory content
• UK GDPR Article 17 — delisting as complementary remedy (separate Meta request)

REQUEST
-------
Delist all specified URLs from Google Search results served to users in the United
Kingdom. I am pursuing source removal with Meta Platforms Ireland Limited.

Signed: {sub['name']}
Case reference: {ref}
"""


def google_round_2_personal_info(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "GOOG-R2")

    return f"""{_header(ref, "Google Personal Information Removal — Doxxing / Non-Consensual Image")}

Submit at: https://support.google.com/websearch/contact/content_removal_form
Also: https://myactivity.google.com/results-about-you

Complainant: {sub['name']}
Email: {sub['email']}

This request complements defamation submission {case_ref(config, 'GOOG-R1')}.

GROUNDS
-------
1. Personal photograph published without my consent, linked to my full name;
2. Page content includes implicit calls for harassment ("red flags" solicitation);
3. Aggregated personal data (name + image + location references in comments) posted
   with intent to harm, not legitimate purpose;
4. Qualifies under Google's doxxing policy: personal info + harmful context.

URLS:
  • {post['url']}
  • [Google search URLs from monitor report]

The underlying Facebook post is subject to UK GDPR Article 17 erasure proceedings.
Google delisting is necessary to prevent ongoing discovery via search while source
removal is pursued.

Signed: {sub['name']}
Case reference: {ref}
"""


def google_round_3_resubmit(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "GOOG-R3")
    prior = ctx.get("google_refusal", "Initial request denied or pending")

    return f"""{_header(ref, "Google Legal Removal — RESUBMISSION with additional grounds")}

Submit at: https://support.google.com/legal/troubleshooter/1114905

RESUBMISSION — Prior outcome: {prior}

Complainant: {sub['name']} | UK / Northern Ireland

ADDITIONAL INFORMATION NOT IN PRIOR SUBMISSION
----------------------------------------------
1. Formal UK GDPR Article 17 request filed with Meta ({case_ref(config, 'META-R1')});
2. Meta Trust & Safety escalation ({case_ref(config, 'META-R3')});
3. ICO complaint filed / pending ({ctx.get('ico_reference', 'pending')});
4. Content contains false criminal allegations — not mere negative opinion;
5. Complainant is a private individual; no public-interest justification exists.

The balance between access to information and privacy favours delisting for a
private citizen targeted by anonymous gossip with fabricated criminal claims.

URLS (unchanged — still requiring delisting):
  • {post['url']}

Please reassess under UK defamation principles and Google personal information
policies. Delisting in the UK jurisdiction is requested.

Signed: {sub['name']}
Case reference: {ref}
"""


# ---------------------------------------------------------------------------
# ICO TRACK — Round 1
# ---------------------------------------------------------------------------


def ico_round_1_complaint(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "ICO-R1")

    return f"""{_header(ref, f"ICO Complaint — Meta Platforms Ireland Limited — {sub['name']}")}

Submit at: https://ico.org.uk/make-a-complaint/
Phone: 0303 123 1113

COMPLAINANT
-----------
Name:    {sub['name']}
Email:   {sub['email']}
Address: {sub['address']}
Phone:   {sub['phone']}

ORGANISATION COMPLAINED ABOUT
-----------------------------
Meta Platforms Ireland Limited (Facebook)
Merrion Road, Dublin 4, D04 X2K5, Ireland

NATURE OF COMPLAINT
-------------------
Failure to comply with Article 17 (right to erasure) UK GDPR and Article 12
(response obligations).

SUMMARY
-------
On or about {ctx.get('meta_r1_sent', '[DATE]')}, I submitted a formal Article 17
erasure request (reference {case_ref(config, 'META-R1')}) to privacy@facebook.com
requiring deletion of:

• My photograph published without consent;
• My name linked to false criminal and sexual allegations;
• All associated comments in a Facebook group post.

Post URL: {post['url']}
Group: {post['group']}

Meta has {"refused erasure" if ctx.get("refusal_reason") else "failed to erase my data within the statutory period / failed to provide valid exemption"}.

{false_allegations_summary()}

CORRESPONDENCE HISTORY (attach all)
-----------------------------------
1. {case_ref(config, 'META-R1')} — Initial Article 17 request
2. {case_ref(config, 'META-R2')} — Article 12(3) reminder
3. {case_ref(config, 'META-R3')} — Trust & Safety escalation
4. {case_ref(config, 'META-R4')} — Rebuttal of refusal
5. {case_ref(config, 'META-R5')} — Final notice

EVIDENCE ATTACHMENTS
--------------------
• Evidence pack with SHA-256 manifest (output/evidence-pack-*/)
• Screenshots showing content still live at time of complaint

REMEDY SOUGHT
-------------
1. ICO investigation into Meta's handling of Article 17 request {case_ref(config, 'META-R1')};
2. Order or pressure for Meta to erase data without further delay;
3. Findings on Article 12(4) failure to provide valid Article 17(3) exemption reasoning.

I confirm this complaint is truthful and submitted in good faith.

Signed: {sub['name']}
Date: {today_long()}
Case reference: {ref}
"""


# ---------------------------------------------------------------------------
# Round registry
# ---------------------------------------------------------------------------

META_ROUNDS: dict[int, tuple[str, LetterFn, str, int]] = {
    1: ("meta_r1_gdpr_initial.txt", meta_round_1_gdpr_initial, "privacy@facebook.com", 0),
    2: ("meta_r2_gdpr_reminder.txt", meta_round_2_gdpr_reminder, "privacy@facebook.com", 7),
    3: ("meta_r3_trust_safety.txt", meta_round_3_trust_safety, "privacy@facebook.com + escalation form", 14),
    4: ("meta_r4_gdpr_rebuttal.txt", meta_round_4_gdpr_rebuttal, "privacy@facebook.com", 21),
    5: ("meta_r5_pre_ico_notice.txt", meta_round_5_pre_ico_notice, "privacy@facebook.com", 28),
    6: ("meta_r6_post_ico.txt", meta_round_6_post_ico, "privacy@facebook.com", 45),
}

GOOGLE_ROUNDS: dict[int, tuple[str, LetterFn, str, int]] = {
    1: ("google_r1_defamation.txt", google_round_1_defamation, "Google Legal Help Center", 0),
    2: ("google_r2_personal_info.txt", google_round_2_personal_info, "Google personal info form", 7),
    3: ("google_r3_resubmit.txt", google_round_3_resubmit, "Google Legal Help Center", 30),
}

ICO_ROUNDS: dict[int, tuple[str, LetterFn, str, int]] = {
    1: ("ico_r1_complaint.txt", ico_round_1_complaint, "https://ico.org.uk/make-a-complaint/", 30),
}

TRACKS = {
    "meta": META_ROUNDS,
    "google": GOOGLE_ROUNDS,
    "ico": ICO_ROUNDS,
}

MAX_META = max(META_ROUNDS)
MAX_GOOGLE = max(GOOGLE_ROUNDS)
MAX_ICO = max(ICO_ROUNDS)

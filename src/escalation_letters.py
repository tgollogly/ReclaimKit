"""
Multi-round escalation letter templates.

Each round increases legal specificity through legitimate channels only.
Wording uses config jurisdiction fields — set privacy law and regulator in config.yaml.
"""

from __future__ import annotations

from typing import Any, Callable

from src.letter_context import (
    case_ref,
    comment_block,
    erasure_request_title,
    false_allegations_summary,
    google_jurisdiction_label,
    group_pattern_block,
    harm_and_distress_block,
    jurisdiction_block,
    meta_reports_block,
    post_details,
    publication_context_block,
    publication_summary_for_google,
    regulator_name,
    regulator_url,
    residency_line,
    search_queries_block,
    section,
    subject_line,
    today_long,
    privacy_law_label,
)

LetterFn = Callable[[dict[str, Any], dict[str, Any]], str]


def _header(ref: str, subject: str) -> str:
    return f"Case Reference: {ref}\nDate: {today_long()}\nSubject: {subject}\n"


def _law(config: dict[str, Any]) -> dict[str, Any]:
    return jurisdiction_block(config)


# ---------------------------------------------------------------------------
# META TRACK — Rounds 1–6
# ---------------------------------------------------------------------------


def meta_round_1_gdpr_initial(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R1")
    j = _law(config)
    group_note = group_pattern_block(config)
    group_section = f"\n{group_note}\n" if group_note else ""
    pub = publication_context_block(config)

    return f"""{_header(ref, f"{erasure_request_title(config)} — {sub['name']}")}

To:      Data Protection Officer
         Meta Platforms Ireland Limited (Facebook)
         Merrion Road, Dublin 4, D04 X2K5, Ireland
Email:   privacy@facebook.com
CC:      dpo@facebook.com

Dear Data Protection Officer,

FORMAL DATA SUBJECT REQUEST — {j['erasure_article']} ({privacy_law_label(config)})

I, {sub['name']}, {residency_line(config)}, hereby exercise my right to erasure under
{j['erasure_article']} of {privacy_law_label(config)}.

{pub['intro']}

This is a formal legal request — not an informal report. Please route this email
to Meta's data protection / privacy team (not Community Standards moderation only)
and treat it as requiring a response within {j['response_days']} days where applicable.

{section("1. Personal data requiring erasure")}
{pub['personal_data']}

{false_allegations_summary(config)}

{harm_and_distress_block(config)}
{group_section}
{section("2. Precise location of data")}
Platform:     Facebook
Group:        {post['group']}
Post date:    {post['date']}
Post caption: "{post['caption']}"
Direct URL:   {post['url']}

Comments containing my personal data / false allegations:
{comment_block(config)}

{section(f"3. Legal grounds ({j['erasure_article']})")}
(a) Data no longer necessary for the purpose processed.
(b) {pub['consent_ground']}
(c) Objection — processing causes disproportionate harm to my rights as a private individual.
(d) {pub['unlawful_ground']}

{section("4. Prior in-app reports (Community Standards — not a privacy-law answer)")}
{meta_reports_block(config)}

{section("5. Requested actions")}
1. Permanently delete the post at the URL above, my photograph, and ALL comments;
2. Delete cached copies, previews, and notification payloads where technically feasible;
3. Confirm deletion in writing to {sub['email']}, quoting reference {ref};
4. If refusing, provide specific written reasons citing the applicable legal exemption.

{section("6. Data subject identification")}
Full name:  {sub['name']}
Email:      {sub['email']}
Telephone:  {sub['phone']}
Address:
{sub['address']}

{section("7. Evidence attached")}
- Screenshots of the post, comments, and platform support messages (evidence/screenshots/)

I reserve all rights under {privacy_law_label(config)}, including complaint to
{regulator_name(config)} where applicable.

Yours faithfully,

{sub['name']}

---
SEND CHECKLIST
--------------
To: privacy@facebook.com (CC: dpo@facebook.com)
Subject line MUST include: {ref}
Attach: all screenshots
After sending: python3 main.py campaign sent --track meta --round 1
"""


def meta_round_2_gdpr_reminder(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R2")
    j = _law(config)
    r1_date = ctx.get("meta_r1_sent", "[DATE OF ROUND 1 EMAIL]")
    r1_ref = case_ref(config, "META-R1")

    return f"""{_header(ref, f"REMINDER — Erasure request deadline — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Dear Data Protection Officer,

Re: {r1_ref} — erasure request dated {r1_date}
    Content URL: {post['url']}

I refer to my formal erasure request ({r1_ref}) sent on {r1_date}. The personal data
identified remains publicly accessible. Each day of continued processing causes further harm.

{section("Immediate action required")}
1. Confirm receipt and provide your internal privacy case reference;
2. Complete erasure at: {post['url']}
3. Provide written confirmation to {sub['email']} within 7 days.

{section("Consequences of continued non-compliance")}
- Formal complaint to {regulator_name(config)};
- Escalation to Meta Trust & Safety with documented non-compliance.

This is a formal reminder of your existing legal obligation under {privacy_law_label(config)}.

Yours faithfully,

{sub['name']}
Case reference: {ref}
"""


def meta_round_3_trust_safety(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R3")

    return f"""{_header(ref, f"TRUST & SAFETY ESCALATION — {sub['name']}")}

Submit via: https://www.facebook.com/help/contact/571927962827151
Also email: privacy@facebook.com (Subject: {ref})

ESCALATION — CONTENT REMAINS LIVE DESPITE PRIVACY REQUEST

Complainant:     {sub['name']} ({sub['email']})
Post URL:        {post['url']}
Group:           {post['group']}

{meta_reports_block(config)}

{section("Violations requiring removal")}
1. Bullying and harassment — named individual with photograph and solicited harmful comments
2. Privacy violations — image published without consent in a harmful context
3. False serious allegations in comments causing real-world harm
4. Unresolved erasure request ({case_ref(config, 'META-R1')}) under {privacy_law_label(config)}

{section("Documented comments")}
{comment_block(config)}

{false_allegations_summary(config)}

{harm_and_distress_block(config)}

{section("Action required within 72 hours")}
Remove post and all comments at: {post['url']}
Confirm removal to {sub['email']} quoting {ref}

Yours faithfully,

{sub['name']}
"""


def meta_round_4_gdpr_rebuttal(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R4")
    refusal = ctx.get("refusal_reason", "[INSERT PLATFORM'S STATED REASON FOR REFUSAL]")

    return f"""{_header(ref, f"FORMAL REBUTTAL OF REFUSAL — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Re: Your refusal regarding {case_ref(config, 'META-R1')}
    Post URL: {post['url']}

{section("Platform's stated position")}
{refusal}

{section("Rebuttal")}
1. Freedom of expression does not override erasure where the data subject is a private
   individual and content contains false harmful allegations without public-interest purpose.
2. "Does not violate Community Standards" is a moderation label — not a lawful erasure exemption.
3. Continued hosting is disproportionate and causes documented harm.

{section("Renewed demand")}
I require immediate erasure. If refusal continues, I will file a complaint with
{regulator_name(config)}.

Yours faithfully,

{sub['name']}
Case reference: {ref}
"""


def meta_round_5_pre_regulator_notice(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R5")

    return f"""{_header(ref, f"FINAL NOTICE BEFORE REGULATOR COMPLAINT — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

FINAL PRE-REGULATORY NOTICE

Content STILL LIVE at: {post['url']}

{section("Final opportunity — 7 days")}
Delete the post, photograph, name, and all comments.
Confirm in writing to {sub['email']}.

If erasure is not completed, I will submit a complaint to {regulator_name(config)} at
{regulator_url(config)} without further notice, including full correspondence and evidence.

Yours faithfully,

{sub['name']}
Case reference: {ref}
"""


def meta_round_6_post_regulator(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R6")
    reg_ref = ctx.get("regulator_reference", "[REGULATOR COMPLAINT REFERENCE]")

    return f"""{_header(ref, f"POST-REGULATOR COMPLAINT — {sub['name']}")}

To:      Data Protection Officer, Meta Platforms Ireland Limited
Email:   privacy@facebook.com

Re: {regulator_name(config)} complaint reference {reg_ref}
    Ongoing erasure breach — {post['url']}

I formally complained to {regulator_name(config)} regarding failure to erase my personal data.

Despite regulatory scrutiny, the content remains accessible.

I require immediate erasure, written confirmation, and notification to {regulator_name(config)}
when completed.

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
    region = google_jurisdiction_label(config)

    return f"""{_header(ref, f"Google Legal Removal — {region}")}

Submit at: https://support.google.com/legal/troubleshooter/1114905
Select the removal category that matches your jurisdiction ({region}).

Complainant: {sub['name']}
Email: {sub['email']}
Jurisdiction: {region}

{section("URLs to delist")}
Primary page:
  {post['url']}

Search result URLs:
{search_queries_block(config)}

{section("Statement of fact")}
I am {sub['name']}, {residency_line(config)}. Search results link to a Facebook group post
in "{post['group']}" (dated {post['date']}) that {publication_summary_for_google(config)}

{section("Why content is harmful and should be delisted")}
{false_allegations_summary(config)}

Documented comments:
{comment_block(config)}

{harm_and_distress_block(config)}

{section("Request")}
Delist specified URLs from Google Search results served to users in {region}.
Source removal is being pursued with Meta ({case_ref(config, 'META-R1')}).

Signed: {sub['name']}
Case reference: {ref}
Date: {today_long()}
"""


def google_round_2_personal_info(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "GOOG-R2")

    return f"""{_header(ref, "Google Personal Information Removal")}

Submit at: https://support.google.com/websearch/contact/content_removal_form

Complainant: {sub['name']}
Email: {sub['email']}

{section("Grounds")}
1. Personal photograph and full name linked with harmful context;
2. Content solicits harassment against a private individual;
3. Qualifies under Google's personal information / harmful content policies.

{section("URLs")}
  {post['url']}
{search_queries_block(config)}

Meta erasure request in progress: {case_ref(config, 'META-R1')}

Signed: {sub['name']}
Case reference: {ref}
"""


def google_round_3_resubmit(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "GOOG-R3")
    prior = ctx.get("google_refusal", "Initial request denied or pending")
    region = google_jurisdiction_label(config)

    return f"""{_header(ref, "Google Legal Removal — RESUBMISSION")}

RESUBMISSION — Prior outcome: {prior}

Complainant: {sub['name']} | {region}

{section("Additional information")}
1. Formal erasure request filed with Meta ({case_ref(config, 'META-R1')});
2. Trust & Safety escalation ({case_ref(config, 'META-R3')});
3. Regulator complaint: {ctx.get('regulator_reference', 'pending')};
4. Private individual — no public-interest justification for continued indexing.

{section("URLs still requiring delisting")}
  {post['url']}
{search_queries_block(config)}

Signed: {sub['name']}
Case reference: {ref}
"""


# ---------------------------------------------------------------------------
# REGULATOR TRACK — Round 1
# ---------------------------------------------------------------------------


def regulator_round_1_complaint(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "REG-R1")
    j = _law(config)

    return f"""{_header(ref, f"Privacy Complaint — Meta Platforms — {sub['name']}")}

Submit at: {regulator_url(config)}

{section("Complainant")}
Name:    {sub['name']}
Email:   {sub['email']}
Address: {sub['address']}
Phone:   {sub['phone']}

{section("Organisation complained about")}
Meta Platforms Ireland Limited (Facebook)
Merrion Road, Dublin 4, D04 X2K5, Ireland

{section("Nature of complaint")}
Failure to comply with {j['erasure_article']} (right to erasure) under {privacy_law_label(config)}.

{section("Summary")}
I submitted a formal erasure request ({case_ref(config, 'META-R1')}) to privacy@facebook.com
requiring deletion of my photograph, name, and harmful comments.

Post URL: {post['url']}
Group: {post['group']}

{meta_reports_block(config)}

{false_allegations_summary(config)}

{harm_and_distress_block(config)}

{section("Remedy sought")}
1. Regulatory investigation into Meta's handling of request {case_ref(config, 'META-R1')};
2. Order or pressure for Meta to erase data without further delay.

Signed: {sub['name']}
Date: {today_long()}
Case reference: {ref}
"""


# Aliases for backward compatibility
ico_round_1_complaint = regulator_round_1_complaint
meta_round_5_pre_ico_notice = meta_round_5_pre_regulator_notice
meta_round_6_post_ico = meta_round_6_post_regulator

# ---------------------------------------------------------------------------
# Round registry
# ---------------------------------------------------------------------------

META_ROUNDS: dict[int, tuple[str, LetterFn, str, int]] = {
    1: ("meta_r1_erasure_initial.txt", meta_round_1_gdpr_initial, "privacy@facebook.com", 0),
    2: ("meta_r2_erasure_reminder.txt", meta_round_2_gdpr_reminder, "privacy@facebook.com", 7),
    3: ("meta_r3_trust_safety.txt", meta_round_3_trust_safety, "privacy@facebook.com + escalation form", 14),
    4: ("meta_r4_rebuttal.txt", meta_round_4_gdpr_rebuttal, "privacy@facebook.com", 21),
    5: ("meta_r5_pre_regulator_notice.txt", meta_round_5_pre_regulator_notice, "privacy@facebook.com", 28),
    6: ("meta_r6_post_regulator.txt", meta_round_6_post_regulator, "privacy@facebook.com", 45),
}

GOOGLE_ROUNDS: dict[int, tuple[str, LetterFn, str, int]] = {
    1: ("google_r1_removal.txt", google_round_1_defamation, "Google Legal Help Center", 0),
    2: ("google_r2_personal_info.txt", google_round_2_personal_info, "Google personal info form", 7),
    3: ("google_r3_resubmit.txt", google_round_3_resubmit, "Google Legal Help Center", 30),
}

REGULATOR_ROUNDS: dict[int, tuple[str, LetterFn, str, int]] = {
    1: ("regulator_r1_complaint.txt", regulator_round_1_complaint, "regulator_url from config", 30),
}

ICO_ROUNDS = REGULATOR_ROUNDS  # backward compatibility

TRACKS = {
    "meta": META_ROUNDS,
    "google": GOOGLE_ROUNDS,
    "regulator": REGULATOR_ROUNDS,
    "ico": REGULATOR_ROUNDS,  # backward compatibility
}

MAX_META = max(META_ROUNDS)
MAX_GOOGLE = max(GOOGLE_ROUNDS)
MAX_REGULATOR = max(REGULATOR_ROUNDS)
MAX_ICO = MAX_REGULATOR

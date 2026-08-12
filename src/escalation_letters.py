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
    group_pattern_block,
    harm_and_distress_block,
    meta_reports_block,
    post_details,
    publication_context_block,
    publication_summary_for_google,
    search_queries_block,
    section,
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
    group_note = group_pattern_block(config)
    group_section = f"\n{group_note}\n" if group_note else ""
    pub = publication_context_block(config)

    return f"""{_header(ref, f"UK GDPR Article 17 — Right to Erasure — {sub['name']}")}

To:      Data Protection Officer
         Meta Platforms Ireland Limited (Facebook)
         Merrion Road, Dublin 4, D04 X2K5, Ireland
Email:   privacy@facebook.com
CC:      dpo@facebook.com

Dear Data Protection Officer,

FORMAL DATA SUBJECT REQUEST — ARTICLE 17 UK GDPR

I, {sub['name']}, a data subject resident in Northern Ireland, United Kingdom,
hereby exercise my right to erasure under Article 17 of the UK General Data
Protection Regulation (UK GDPR) and section 47 of the Data Protection Act 2018.

{pub['intro']}

This is a formal legal request — not an informal report. Please route this email
to Meta's data protection / privacy team (not Community Standards moderation only)
and treat it as requiring a response within one calendar month under Article 12(3)
UK GDPR.

{section("1. Personal data requiring erasure")}
{pub['personal_data']}

{false_allegations_summary()}

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

{section("3. Legal grounds (Article 17(1) UK GDPR)")}
(a) Article 17(1)(a) — Data no longer necessary for the purpose processed.
    I require this data erased. No journalistic, academic, or public-interest
    justification exists for continued processing of my image with solicited allegations.

{pub['consent_ground']}

(c) Article 17(1)(d) — Objection under Article 21. Processing causes disproportionate
    harm to my rights, dignity, and reputation as a private individual in Northern
    Ireland.

{pub['unlawful_ground']}

Article 17(2) requires reasonable steps to inform other controllers where data was
made public. Article 19 requires communication of erasure to recipients unless
impossible or involving disproportionate effort.

{section("4. Prior in-app reports (Community Standards — not a GDPR answer)")}
{meta_reports_block(config)}

{section("5. Requested actions (within one calendar month)")}
1. Permanently delete the post at the URL above, my photograph, and ALL comments;
2. Delete cached copies, previews, and notification payloads where technically feasible;
3. Confirm deletion in writing to {sub['email']}, quoting reference {ref};
4. Confirm compliance with Articles 17(2) and 19 UK GDPR;
5. If refusing, provide specific written reasons under Article 12(4) and identify the
   exact Article 17(3) exemption relied upon (Community Standards labels are not sufficient).

{section("6. Data subject identification")}
Full name:  {sub['name']}
Email:      {sub['email']}
Telephone:  {sub['phone']}
Address:
{sub['address']}

I will provide photographic identification upon request if reasonably required to
verify identity. I have not been asked to send ID in advance.

{section("7. Evidence attached")}
- Screenshots of the post, comments, and Meta support messages (evidence/screenshots/)
- This letter constitutes timestamped formal notice

I reserve all rights under UK GDPR (including complaint to the ICO under Article 77)
and under the Defamation Act (Northern Ireland) 2022. This request is made in good
faith for removal of my personal data only.

Yours faithfully,

{sub['name']}

---
SEND CHECKLIST
--------------
To: privacy@facebook.com (CC: dpo@facebook.com)
Subject line MUST include: {ref}
Attach: all screenshots including Meta "We didn't remove the photo" message if applicable
After sending: python3 main.py campaign sent --track meta --round 1
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
CC:      dpo@facebook.com

Dear Data Protection Officer,

Re: {r1_ref} — Article 17 erasure request dated {r1_date}
    Content URL: {post['url']}

I refer to my formal Article 17 request ({r1_ref}) sent on {r1_date}. I have received
{"no acknowledgement" if not ctx.get("meta_r1_ack") else "no substantive response or erasure"}.

Under Article 12(3) UK GDPR, you must respond without undue delay and in any event
within one month of receipt. That statutory deadline is approaching or has passed.

The personal data identified in my original request remains publicly accessible.
Each day of continued processing causes further reputational and psychological harm.

{section("Immediate action required")}
1. Confirm receipt of this reminder and provide your internal GDPR case reference;
2. Complete erasure of the post, image, name, and all comments at:
   {post['url']}
3. Provide written confirmation to {sub['email']} within 7 days.

{section("Consequences of continued non-compliance")}
- Formal complaint to the Information Commissioner's Office (Article 77 UK GDPR);
- Escalation to Meta Trust & Safety with documented GDPR non-compliance;
- Reservation of all rights under the Defamation Act (Northern Ireland) 2022.

This is not a new request — it is a formal reminder of your existing legal obligation.
Community Standards outcomes do not override Article 17.

Yours faithfully,

{sub['name']}
Case reference: {ref} (links to {r1_ref})
"""


def meta_round_3_trust_safety(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "META-R3")

    return f"""{_header(ref, f"TRUST & SAFETY ESCALATION — Policy + GDPR — {sub['name']}")}

Submit via: https://www.facebook.com/help/contact/571927962827151
Also email: privacy@facebook.com (Subject: {ref})

To: Meta Trust & Safety / Content Policy Enforcement

ESCALATION — CONTENT REMAINS LIVE DESPITE GDPR REQUEST AND IN-APP REPORTS

Complainant:     {sub['name']} ({sub['email']})
Case reference:  {ref}
Post URL:        {post['url']}
Group:           {post['group']}

{meta_reports_block(config)}

{section("Violations requiring removal")}
1. COMMUNITY STANDARDS — Bullying and harassment
   The post targets a named private individual with my photograph and solicits
   damaging commentary. This is coordinated reputational harm, not legitimate discussion.

2. COMMUNITY STANDARDS — Privacy violations
   My image was published without consent in a context designed to expose and humiliate.

3. COMMUNITY STANDARDS — Safety / criminal allegations
   Comments falsely attribute criminal conduct (drugging drinks, sexual offences).
   These are presented as factual claims causing real-world harm, not protected opinion.

4. UK GDPR — Unlawful processing (see {case_ref(config, 'META-R1')})
   Formal Article 17 request remains unresolved. GDPR erasure is mandatory unless a
   valid Article 17(3) exemption is documented under Article 12(4).

5. DEFAMATION ACT (NORTHERN IRELAND) 2022
   Statements convey serious criminal imputations that are false. I am a private
   individual. No public-interest defence applies to anonymous gossip with fabricated claims.

{section("Documented comments (false allegations on record)")}
{comment_block(config)}

{false_allegations_summary()}

{harm_and_distress_block(config)}

{section("Action required within 72 hours")}
[ ] Remove post and all comments at: {post['url']}
[ ] Confirm removal to {sub['email']} quoting {ref}
[ ] Confirm GDPR case handler has been assigned (separate from CS moderation)

Continued publication after documented notice increases my losses and strengthens
regulatory and civil remedies. I require SOURCE REMOVAL — not merely reduced visibility.

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
CC:      dpo@facebook.com

Dear Data Protection Officer,

Re: Your refusal / inadequate response regarding {case_ref(config, 'META-R1')}
    Post URL: {post['url']}

I reject your position that erasure is not required. My detailed rebuttal follows.

{section("Meta's stated position (or effective position by non-removal)")}
{refusal}

{section("Rebuttal")}
1. Article 17(3)(a) — Freedom of expression does NOT apply here.

   ICO and EDPB guidance confirm erasure must be balanced against expression rights.
   That balance favours erasure where:
   - The data subject is a private individual (I am not a public figure);
   - Content contains false, serious criminal allegations;
   - Processing serves no journalistic, academic, or public-interest purpose;
   - Content was posted in a gossip group soliciting reputational harm.

   "Does not violate Community Standards" is a moderation label — not an Article 17(3)
   exemption cited under Article 12(4).

2. No legitimate interest under Article 6(1)(f) outweighs my rights.

   Meta cannot rely on legitimate interests to host my photograph and name alongside
   false claims of drugging and sexual misconduct.

3. Sensitive imputations — false sexual misconduct claims involve particularly harmful
   processing. Continued hosting is disproportionate.

4. Data Protection Act 2018 — No applicable exemption permits continued processing.

{section("Renewed demand")}
I require immediate erasure of all data specified in {case_ref(config, 'META-R1')}.
Provide a substantive written response within 14 days addressing each point above.

If you maintain refusal, I will file a formal ICO complaint citing:
- Failure to comply with Article 17;
- Failure to provide valid Article 17(3) reasoning under Article 12(4);
- Continued unlawful processing causing documented harm.

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
CC:      dpo@facebook.com

Dear Data Protection Officer,

FINAL PRE-REGULATORY NOTICE

Case history:
  - {case_ref(config, 'META-R1')} — Article 17 request
  - {case_ref(config, 'META-R2')} — Article 12(3) reminder
  - {case_ref(config, 'META-R3')} — Trust & Safety escalation
  - {case_ref(config, 'META-R4')} — Formal rebuttal

Content STILL LIVE at: {post['url']}

You have failed to erase my personal data or provide a lawful exemption under
Article 17(3) UK GDPR with the specificity required by Article 12(4).

{section("Final opportunity — 7 days")}
Delete the post, photograph, name, and all comments.
Confirm in writing to {sub['email']}.

If erasure is not completed, I will submit an ICO complaint on day 8 without further
notice. The complaint will include:

- Complete correspondence history;
- SHA-256 verified evidence pack;
- Screenshots proving ongoing publication;
- Meta Community Standards rejection messages;
- Request for ICO enforcement under Article 58 UK GDPR.

Continued processing after this notice may aggravate regulatory findings.

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
failure to erase my personal data. Complaint reference: {ico_ref}.

Despite regulatory scrutiny, the content remains accessible. This demonstrates
continued non-compliance with UK GDPR.

I require:
1. Immediate erasure pending ICO investigation;
2. Written confirmation to {sub['email']};
3. Notification to the ICO of compliance when completed.

I am submitting updated Google delisting requests for any indexed URLs.

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
Select: Defamation -> United Kingdom

Complainant: {sub['name']}
Email: {sub['email']}
Jurisdiction: United Kingdom — complainant domiciled in Northern Ireland

{section("URLs to delist")}
Primary page:
  {post['url']}

Search result URLs (add each google.com/search link that shows this content):
{search_queries_block(config)}

{section("Statement of fact")}
I am {sub['name']}, a private individual resident in Northern Ireland. Search results
for my name link to a Facebook group post in "{post['group']}" (dated {post['date']})
that {publication_summary_for_google(config)}

{section("Why statements are false")}
{false_allegations_summary()}

Documented comments (each false):
{comment_block(config)}

{section("Serious harm (Defamation Act (Northern Ireland) 2022)")}
The content causes serious reputational harm to me as a private individual. Publication
of false criminal allegations linked to my name in Google Search affects employment,
relationships, and safety. The serious harm threshold is clearly met.

Meta in-app Community Standards reports were rejected; source removal is being pursued
via UK GDPR Article 17 ({case_ref(config, 'META-R1')}). Delisting is necessary to limit
ongoing discovery while source erasure is enforced.

{section("Legal basis for delisting")}
- UK defamation law — false statements causing serious reputational harm
- Google Search Legal Removals Policy — defamatory content
- UK GDPR Article 17 — complementary remedy (separate Meta request in progress)
- Google "Results about you" / personal safety policies for non-consensual exposure

{section("Request")}
Delist all specified URLs from Google Search results served to users in the United
Kingdom (including Northern Ireland). I am pursuing source removal with Meta Platforms
Ireland Limited.

Signed: {sub['name']}
Case reference: {ref}
Date: {today_long()}
"""


def google_round_2_personal_info(config: dict[str, Any], ctx: dict[str, Any]) -> str:
    sub = subject_line(config)
    post = post_details(config)
    ref = case_ref(config, "GOOG-R2")

    return f"""{_header(ref, "Google Personal Information Removal — Non-Consensual Image / Doxxing")}

Submit at: https://support.google.com/websearch/contact/content_removal_form
Also enable: https://myactivity.google.com/results-about-you

Complainant: {sub['name']}
Email: {sub['email']}

This request complements defamation submission {case_ref(config, 'GOOG-R1')}.

{section("Grounds")}
1. Personal photograph and full name linked in Google Search with harmful context;
2. Page content solicits harassment ("red flags" / warning posts about a private citizen);
3. Aggregated personal data (name + image + location references in comments) posted
   to cause harm, not for legitimate purpose;
4. Qualifies under Google's policies for personal information shared with harmful intent;
5. Complainant is a private individual in Northern Ireland — no public figure exemption.

{section("URLs")}
  {post['url']}
{search_queries_block(config)}

The underlying Facebook post is subject to UK GDPR Article 17 proceedings ({case_ref(config, 'META-R1')}).
Google delisting prevents ongoing discovery via search while source removal is pursued.

{harm_and_distress_block(config)}

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

{section("Additional information not in prior submission")}
1. Formal UK GDPR Article 17 request filed with Meta ({case_ref(config, 'META-R1')});
2. Meta Trust & Safety escalation ({case_ref(config, 'META-R3')});
3. ICO complaint filed / pending ({ctx.get('ico_reference', 'pending')});
4. Meta rejected in-app Community Standards reports — GDPR process ongoing;
5. Content contains false criminal allegations — not mere negative opinion;
6. Complainant is a private individual; no public-interest justification exists.

The balance between access to information and privacy favours delisting for a
private citizen targeted by anonymous gossip with fabricated criminal claims.

{section("URLs still requiring delisting")}
  {post['url']}
{search_queries_block(config)}

Please reassess under UK defamation principles and Google personal information
policies. Delisting for UK jurisdiction is requested.

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

{section("Complainant")}
Name:    {sub['name']}
Email:   {sub['email']}
Address: {sub['address']}
Phone:   {sub['phone']}

{section("Organisation complained about")}
Meta Platforms Ireland Limited (Facebook)
Merrion Road, Dublin 4, D04 X2K5, Ireland

{section("Nature of complaint")}
Failure to comply with Article 17 (right to erasure) UK GDPR and Article 12
(response obligations).

{section("Summary")}
On or about {ctx.get('meta_r1_sent', '[DATE]')}, I submitted a formal Article 17
erasure request (reference {case_ref(config, 'META-R1')}) to privacy@facebook.com
requiring deletion of:

- My photograph published without consent;
- My name linked to false criminal and sexual allegations;
- All associated comments in a Facebook group post.

Post URL: {post['url']}
Group: {post['group']}

{meta_reports_block(config)}

Meta has {"refused erasure or relied on Community Standards" if ctx.get("refusal_reason") else "failed to erase my data within the statutory period / failed to provide valid exemption"}.

{false_allegations_summary()}

{harm_and_distress_block(config)}

{section("Correspondence history (attach all)")}
1. {case_ref(config, 'META-R1')} — Initial Article 17 request
2. {case_ref(config, 'META-R2')} — Article 12(3) reminder
3. {case_ref(config, 'META-R3')} — Trust & Safety escalation
4. {case_ref(config, 'META-R4')} — Rebuttal of refusal
5. {case_ref(config, 'META-R5')} — Final notice

{section("Evidence attachments")}
- Evidence pack with SHA-256 manifest (output/evidence-pack-*/)
- Screenshots showing content still live
- Meta support messages rejecting Community Standards reports

{section("Remedy sought")}
1. ICO investigation into Meta's handling of Article 17 request {case_ref(config, 'META-R1')};
2. Order or regulatory pressure for Meta to erase data without further delay;
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

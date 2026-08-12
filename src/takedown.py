from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _format_address(subject: dict[str, Any]) -> str:
    parts = [
        subject.get("address_line1", ""),
        subject.get("city", ""),
        subject.get("county", ""),
        subject.get("postcode", ""),
        subject.get("country", "United Kingdom"),
    ]
    return "\n".join(p for p in parts if p)


def generate_meta_gdpr_letter(config: dict[str, Any]) -> str:
    """UK GDPR Article 17 right-to-erasure request to Meta."""
    subject = config["subject"]
    fb = config["case"]["facebook"]
    name = subject["full_name"]
    today = datetime.now(timezone.utc).strftime("%d %B %Y")

    comment_block = _comment_summary(config)

    return f"""Subject: URGENT — UK GDPR Article 17 Right to Erasure Request — {name}

Date: {today}

To: Meta Platforms Ireland Limited (Data Protection Officer)
     Merrion Road, Dublin 4, D04 X2K5, Ireland
     privacy@facebook.com

Dear Data Protection Officer,

I, {name}, am writing to exercise my rights under Article 17 of the UK General Data
Protection Regulation (UK GDPR) and the Data Protection Act 2018.

PERSONAL DATA TO BE ERASED
--------------------------
1. My photograph (a selfie), posted without my consent.
2. My full name ("Thomas Gollogly" / "Thomas gollogly") in connection with that image.
3. All comments identifying me or repeating allegations about me.

LOCATION OF DATA
----------------
Facebook Group: {fb['group_name']}
Post date (approx.): {fb['post_date']}
Post caption: "{fb['post_caption']}"
Post URL (if known): {fb['post_url'] or '[please insert URL from Facebook Share link]'}

COMMENTS CONTAINING MY PERSONAL DATA / FALSE ALLEGATIONS
----------------------------------------------------------
{comment_block}

LEGAL GROUNDS FOR ERASURE (Article 17(1))
----------------------------------------
(a) The data is no longer necessary for any legitimate purpose;
(c) I withdraw any consent that may have been implied (there was none — I did not
    authorise this post or use of my image);
(d) I object to processing; the data is being used to cause me serious harm;
(e) The processing is unlawful — my image and name are used without consent in a
    context making false and damaging allegations.

The allegations (including claims of drugging drinks and sexual misconduct) are
wholly false. I deny them absolutely. Publication causes ongoing and serious damage
to my reputation and mental health.

I have already reported this content via Meta's in-app reporting tools
(reported: {fb.get('reported_to_meta', False)}; reference: {fb.get('meta_report_reference') or 'N/A'}).

REQUESTED ACTION
----------------
Within one calendar month (Article 12(3) UK GDPR), please:
1. Permanently delete the post, my photograph, and all related comments.
2. Confirm deletion in writing to {subject['email']}.
3. Under Article 19, inform any recipients to whom this data was disclosed.
4. Under Article 17(2), take reasonable steps to inform other controllers processing
   this data of my erasure request.

IDENTIFICATION
--------------
Full name: {name}
Email: {subject['email']}
Phone: {subject.get('phone', 'N/A')}
Address:
{_format_address(subject)}

I can provide photographic ID and additional proof of identity on request.

If you refuse this request, please provide reasons under Article 12(4) and inform
me of my right to complain to the Information Commissioner's Office (ICO):
https://ico.org.uk/make-a-complaint/

I also reserve all rights under the Defamation Act (Northern Ireland) 2022.

Yours faithfully,

{name}
"""


def generate_meta_defamation_escalation(config: dict[str, Any]) -> str:
    """Follow-up escalation if initial report was ignored."""
    subject = config["subject"]
    fb = config["case"]["facebook"]
    name = subject["full_name"]
    today = datetime.now(timezone.utc).strftime("%d %B %Y")

    return f"""Subject: ESCALATION — Defamatory Content & UK GDPR Breach — {name}

Date: {today}

To: Meta Legal / Trust & Safety Escalations
     https://www.facebook.com/help/contact/571927962827151

Dear Meta Trust & Safety Team,

This is a formal escalation regarding content that remains live despite my prior report.

COMPLAINANT: {name} ({subject['email']})
GROUP: {fb['group_name']}
POST DATE: {fb['post_date']}
POST URL: {fb['post_url'] or '[insert URL]'}

SUMMARY
-------
An anonymous post displays my photograph alongside my name with a caption soliciting
"red flags." Comments contain serious false allegations including drugging drinks and
sexual misconduct. These statements are defamatory under the Defamation Act
(Northern Ireland) 2022 and constitute unlawful processing of my personal data.

I deny every allegation. The content is not opinion — it asserts criminal conduct
falsely attributed to me.

ACTION REQUIRED
---------------
1. Immediate removal of the post and all defamatory comments.
2. Suspension of accounts posting demonstrably false criminal allegations.
3. Written confirmation to {subject['email']} within 72 hours.

I am preparing complaints to the ICO and am instructing solicitors specialising in
NI defamation law. Continued publication after notice aggravates damages.

{config['case'].get('summary', '').strip()}

Yours faithfully,
{name}
"""


def generate_google_defamation_request(config: dict[str, Any]) -> str:
    """Draft text for Google's Legal Help Center defamation form."""
    subject = config["subject"]
    fb = config["case"]["facebook"]
    name = subject["full_name"]

    return f"""GOOGLE DEFAMATION REMOVAL REQUEST — DRAFT TEXT
================================================
Submit at: https://support.google.com/legal/troubleshooter/1114905
Select: Defamation → United Kingdom

Complainant: {name}
Country for delisting: United Kingdom (Northern Ireland)

URLs TO REMOVE (add each Google search result URL showing the harmful content):
  [ ] https://www.google.com/search?q=...
  [ ] [direct Facebook URL if indexed]
  [ ] [any other indexed pages]

STATEMENT OF FACT
-----------------
My name is {name}. I am domiciled in Northern Ireland, United Kingdom.

False and defamatory statements about me appear in Google Search results, linking
to a Facebook group post in "{fb['group_name']}" dated approximately {fb['post_date']}.

The post uses my photograph and name without consent. Comments falsely allege
criminal conduct including drugging people's drinks and sexual misconduct. I deny
these allegations absolutely. They are not true and are seriously damaging to my
reputation.

WHY STATEMENTS ARE FALSE
------------------------
I have never engaged in any conduct described in those comments. The allegations
are anonymous gossip with no factual basis, posted in a "red flags" gossip group
designed to harm reputations.

HARM TO REPUTATION
------------------
The content appears when my name is searched professionally and personally. It causes
ongoing distress, reputational harm, and anxiety. I am employed / known in my community
in Northern Ireland.

JURISDICTION
------------
Northern Ireland is clearly the most appropriate jurisdiction. I live in Northern Ireland.
The Facebook group is specifically "Northern Ireland." The harm occurs here.

REQUEST
-------
Please delist the specified URLs from Google Search results for users in the
United Kingdom pursuant to UK defamation law and Google's defamation policy.

Note: Google delisting removes search visibility only. I am separately pursuing
removal at source via Meta and legal action under the Defamation Act (NI) 2022.

Signed: {name}
Email: {subject['email']}
"""


def generate_google_personal_info_request(config: dict[str, Any]) -> str:
    """Draft for Google's personal info / doxxing removal form."""
    subject = config["subject"]
    name = subject["full_name"]

    return f"""GOOGLE PERSONAL INFORMATION REMOVAL — DRAFT TEXT
=====================================================
Submit at: https://support.google.com/websearch/contact/content_removal_form

This form covers: image published without consent + name linked to harmful context.

Complainant: {name}
Email: {subject['email']}

Explanation:
My photograph and full name appear in Google Search results linking to a Facebook
post I did not authorise. The page contains false allegations and harassment. I did
not consent to my image or name being used in this context.

URLs:
  [List each Google search result URL and the underlying Facebook/page URL]

I request removal under Google's policies on personal information published without
consent and doxxing (personal info with implicit harm/harassment).

Signed: {name}
"""


def _comment_summary(config: dict[str, Any]) -> str:
    commenters = config["case"].get("alleged_commenters", [])
    if not commenters:
        return "  (No comments listed in config — add them to config.yaml)"
    lines = []
    for idx, c in enumerate(commenters, 1):
        lines.append(
            f"{idx}. User \"{c['display_name']}\" ({c.get('posted_approx', 'date unknown')}):\n"
            f"   \"{c['comment']}\""
        )
    return "\n".join(lines)


def write_takedown_letters(config: dict[str, Any], output_dir: Path | None = None) -> Path:
    out = output_dir or Path(config["evidence"]["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    letter_dir = out / f"takedown-letters-{timestamp}"
    letter_dir.mkdir(parents=True, exist_ok=True)

    letters = {
        "01_meta_gdpr_article17.txt": generate_meta_gdpr_letter(config),
        "02_meta_defamation_escalation.txt": generate_meta_defamation_escalation(config),
        "03_google_defamation_request.txt": generate_google_defamation_request(config),
        "04_google_personal_info_request.txt": generate_google_personal_info_request(config),
    }
    for filename, content in letters.items():
        (letter_dir / filename).write_text(content, encoding="utf-8")

    readme = letter_dir / "HOW_TO_SUBMIT.txt"
    readme.write_text(
        """HOW TO SUBMIT THESE LETTERS
=============================

META (Facebook):
  1. GDPR letter: Email privacy@facebook.com AND submit via
     Settings > Privacy > How Meta uses your info > Access and control your info
     > Submit a privacy request
  2. Escalation form: https://www.facebook.com/help/contact/571927962827151
  3. Keep copies of everything you send and Meta's replies.

GOOGLE:
  1. Defamation: https://support.google.com/legal/troubleshooter/1114905
  2. Personal info: https://support.google.com/websearch/contact/content_removal_form
  3. "Results about you": https://myactivity.google.com/results-about-you
  4. Google removes from Search only — source removal still needed via Meta.

IMPORTANT:
  - No software can force removal. These are the official legal channels.
  - Google UK delisting does not delete Facebook content.
  - If Meta refuses after 30 days, complain to ICO: https://ico.org.uk/make-a-complaint/
  - For serious false criminal allegations, consider PSNI report (101) and a NI solicitor.
""",
        encoding="utf-8",
    )
    return letter_dir

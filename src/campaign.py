"""Campaign state: tracks submission rounds and generates next escalation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.escalation_letters import ICO_ROUNDS, META_ROUNDS, TRACKS
from src.security import clamp_text
from src.letter_context import case_ref, today_long

STATE_VERSION = 1
DEFAULT_STATE_PATH = Path("output/campaign/state.json")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _today_short() -> str:
    return datetime.now(timezone.utc).strftime("%d %B %Y")


def load_state(path: Path | None = None) -> dict[str, Any]:
    state_path = path or DEFAULT_STATE_PATH
    if not state_path.exists():
        raise FileNotFoundError(
            f"No campaign found at {state_path}. Run: python3 main.py campaign init"
        )
    with state_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_state(state: dict[str, Any], path: Path | None = None) -> Path:
    state_path = path or DEFAULT_STATE_PATH
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _utc_now_iso()
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state_path


def init_campaign(config: dict[str, Any], output_dir: Path | None = None) -> dict[str, Any]:
    out = output_dir or Path(config["evidence"]["output_dir"])
    state_path = out / "campaign" / "state.json"
    if state_path.exists():
        return load_state(state_path)

    state: dict[str, Any] = {
        "version": STATE_VERSION,
        "created_at": _utc_now_iso(),
        "updated_at": _utc_now_iso(),
        "subject": config["subject"]["full_name"],
        "post_url": config["case"]["facebook"]["post_url"],
        "case_root": case_ref(config),
        "status": "active",
        "removed": False,
        "tracks": {
            "meta": {"round": 0, "max_round": max(META_ROUNDS), "events": []},
            "google": {"round": 0, "max_round": max(TRACKS["google"]), "events": []},
            "ico": {"round": 0, "max_round": max(TRACKS["ico"]), "events": []},
        },
        "context": {},
        "history": [],
    }
    save_state(state, state_path)
    return state


def _ctx_from_state(state: dict[str, Any]) -> dict[str, Any]:
    ctx = dict(state.get("context", {}))
    for track, data in state["tracks"].items():
        for event in data.get("events", []):
            if event.get("type") == "sent" and track == "meta" and event.get("round") == 1:
                ctx.setdefault("meta_r1_sent", event.get("date", _today_short()))
            if event.get("type") == "refused" and track == "meta":
                ctx.setdefault("refusal_reason", event.get("reason", ""))
            if event.get("type") == "refused" and track == "google":
                ctx.setdefault("google_refusal", event.get("reason", ""))
            if event.get("type") == "sent" and track == "ico":
                ctx.setdefault("ico_reference", event.get("reference", ""))
    return ctx


def generate_round_package(
    config: dict[str, Any],
    state: dict[str, Any],
    track: str,
    round_num: int,
    package_dir: Path,
) -> Path:
    rounds = TRACKS[track]
    if round_num not in rounds:
        raise ValueError(f"No letter for {track} round {round_num}")

    filename, letter_fn, send_to, _ = rounds[round_num]
    ctx = _ctx_from_state(state)
    content = letter_fn(config, ctx)

    round_dir = package_dir / f"round-{round_num:02d}-{track}"
    round_dir.mkdir(parents=True, exist_ok=True)

    letter_path = round_dir / filename
    letter_path.write_text(content, encoding="utf-8")

    instructions = round_dir / "SUBMIT.txt"
    instructions.write_text(
        _submit_instructions(track, round_num, send_to, case_ref(config, f"{track.upper()}-R{round_num}")),
        encoding="utf-8",
    )
    return round_dir


def _submit_instructions(track: str, round_num: int, send_to: str, ref: str) -> str:
    lines = [
        f"ROUND {round_num} — {track.upper()}",
        "=" * 50,
        f"Case reference: {ref}",
        f"Send to: {send_to}",
        "",
    ]
    if track == "meta":
        lines.extend([
            "1. Email the letter to privacy@facebook.com",
            "2. Paste the case reference in the email subject line",
            "3. Attach screenshots from evidence/screenshots/",
            "4. If round 3+, also submit: facebook.com/help/contact/571927962827151",
            "5. After sending, run:",
            f"   python3 main.py campaign sent --track meta --round {round_num}",
        ])
    elif track == "google":
        lines.extend([
            "1. Open the URL in the letter header",
            "2. Paste letter content into the form fields",
            "3. After submitting, run:",
            f"   python3 main.py campaign sent --track google --round {round_num}",
        ])
    elif track == "ico":
        lines.extend([
            "1. Submit at https://ico.org.uk/make-a-complaint/",
            "2. Attach evidence pack + all Meta correspondence",
            "3. After submitting, run:",
            f"   python3 main.py campaign sent --track ico --round {round_num} --reference YOUR-ICO-REF",
        ])
    return "\n".join(lines) + "\n"


def advance_track(state: dict[str, Any], track: str) -> int:
    current = state["tracks"][track]["round"]
    maximum = state["tracks"][track]["max_round"]
    if current >= maximum:
        return current
    return current + 1


def record_sent(
    state: dict[str, Any],
    track: str,
    round_num: int,
    *,
    reference: str = "",
) -> dict[str, Any]:
    data = state["tracks"][track]
    if round_num != data["round"] + 1 and data["round"] != 0:
        # Allow re-recording same round or next sequential round
        if round_num <= data["round"]:
            pass  # idempotent re-record
        elif round_num > data["round"] + 1:
            raise ValueError(
                f"Expected round {data['round'] + 1} for {track}, got {round_num}. "
                "Send rounds in order."
            )
    data["round"] = max(data["round"], round_num)
    event = {
        "type": "sent",
        "round": round_num,
        "date": _today_short(),
        "timestamp": _utc_now_iso(),
    }
    if reference:
        event["reference"] = reference
    data["events"].append(event)
    state["history"].append(f"{track} round {round_num} sent on {_today_short()}")
    if track == "meta" and round_num == 1:
        state.setdefault("context", {})["meta_r1_sent"] = _today_short()
    return state


def record_refusal(
    state: dict[str, Any],
    track: str,
    reason: str,
) -> dict[str, Any]:
    if track not in state["tracks"]:
        raise ValueError(f"Unknown track: {track!r}")
    reason = clamp_text(reason.strip(), 4000)
    if not reason:
        raise ValueError("Refusal reason cannot be empty")
    data = state["tracks"][track]
    event = {
        "type": "refused",
        "round": data["round"],
        "date": _today_short(),
        "timestamp": _utc_now_iso(),
        "reason": reason,
    }
    data["events"].append(event)
    state["history"].append(f"{track} refused at round {data['round']}: {reason[:80]}")
    if track == "meta":
        state.setdefault("context", {})["refusal_reason"] = reason
    elif track == "google":
        state.setdefault("context", {})["google_refusal"] = reason
    return state


def record_no_response(state: dict[str, Any], track: str, days: int) -> dict[str, Any]:
    data = state["tracks"][track]
    event = {
        "type": "no_response",
        "round": data["round"],
        "days": days,
        "date": _today_short(),
        "timestamp": _utc_now_iso(),
    }
    data["events"].append(event)
    state["history"].append(f"{track} no response after {days} days at round {data['round']}")
    return state


def record_success(state: dict[str, Any], note: str = "") -> dict[str, Any]:
    state["status"] = "completed"
    state["removed"] = True
    state["history"].append(f"SUCCESS — content removed. {note}".strip())
    return state


def next_actions(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Determine what should be sent next across all tracks."""
    actions: list[dict[str, Any]] = []
    for track, data in state["tracks"].items():
        nxt = data["round"] + 1
        if nxt <= data["max_round"]:
            actions.append({
                "track": track,
                "round": nxt,
                "reason": _next_reason(state, track, nxt),
            })
    return actions


def _next_reason(state: dict[str, Any], track: str, round_num: int) -> str:
    data = state["tracks"][track]
    if data["round"] == 0:
        return "Initial submission — start here"
    last_events = [e for e in data["events"] if e["type"] in ("refused", "no_response")]
    if last_events:
        last = last_events[-1]
        if last["type"] == "refused":
            return f"Previous round refused — escalate with round {round_num}"
        return f"No response — escalate with round {round_num}"
    if data["round"] > 0:
        events_sent = [e for e in data["events"] if e["type"] == "sent"]
        if events_sent:
            return f"Follow-up round {round_num} (recommended if no removal yet)"
    return f"Proceed to round {round_num}"


def generate_next_package(
    config: dict[str, Any],
    state: dict[str, Any],
    *,
    track: str | None = None,
    force_round: int | None = None,
) -> tuple[Path, list[str]]:
    """Generate letter package for the next required round(s)."""
    out = Path(config["evidence"]["output_dir"])
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    package_dir = out / f"campaign-package-{timestamp}"
    package_dir.mkdir(parents=True, exist_ok=True)

    generated: list[str] = []

    def _gen(t: str, rnd: int) -> None:
        generate_round_package(config, state, t, rnd, package_dir)
        generated.append(f"{t} round {rnd}")

    if track:
        data = state["tracks"][track]
        rnd = force_round or (data["round"] + 1)
        if rnd > data["max_round"]:
            raise ValueError(f"{track} track complete — all {data['max_round']} rounds used.")
        _gen(track, rnd)
    else:
        meta_r = state["tracks"]["meta"]["round"]
        google_r = state["tracks"]["google"]["round"]
        ico_r = state["tracks"]["ico"]["round"]

        if meta_r == 0:
            _gen("meta", 1)
        elif meta_r < state["tracks"]["meta"]["max_round"]:
            _gen("meta", meta_r + 1)

        if google_r == 0:
            _gen("google", 1)
        elif google_r < state["tracks"]["google"]["max_round"] and meta_r >= 2:
            _gen("google", google_r + 1)

        if ico_r == 0 and meta_r >= 4:
            _gen("ico", 1)
        elif ico_r < state["tracks"]["ico"]["max_round"] and meta_r >= 5:
            _gen("ico", ico_r + 1)

    if not generated:
        raise ValueError(
            "No letters to generate for current campaign state. "
            "Use: python3 main.py campaign next --track meta"
        )

    master = package_dir / "README.txt"
    master.write_text(_package_readme(state, generated), encoding="utf-8")
    return package_dir, generated


def _package_readme(state: dict[str, Any], generated: list[str]) -> str:
    lines = [
        "CAMPAIGN ESCALATION PACKAGE",
        "=" * 50,
        f"Generated: {today_long()}",
        f"Case root: {state.get('case_root', 'N/A')}",
        f"Status: {state['status']}",
        "",
        "Generated this session:",
    ]
    lines.extend(f"  • {g}" for g in generated)
    lines.extend([
        "",
        "WORKFLOW",
        "------",
        "1. Send each letter in this package",
        "2. Record: python3 main.py campaign sent --track meta --round N",
        "3. If refused: python3 main.py campaign refused --track meta --reason \"...\"",
        "4. If no reply in 7+ days: python3 main.py campaign no-response --track meta",
        "5. Get next package: python3 main.py campaign next",
        "6. When removed: python3 main.py campaign success",
        "",
        "TRACK PROGRESS:",
    ])
    for track, data in state["tracks"].items():
        lines.append(f"  {track}: round {data['round']}/{data['max_round']}")
    return "\n".join(lines) + "\n"


def format_status(state: dict[str, Any]) -> str:
    lines = [
        "CAMPAIGN STATUS",
        "=" * 50,
        f"Subject: {state.get('subject')}",
        f"Post: {state.get('post_url')}",
        f"Overall: {state['status']}" + (" ✓ REMOVED" if state.get("removed") else ""),
        "",
        "TRACKS:",
    ]
    for track, data in state["tracks"].items():
        lines.append(f"  {track.upper():6} — round {data['round']}/{data['max_round']}")
        for event in data["events"][-3:]:
            lines.append(f"           {event['type']} (round {event.get('round', '?')}) {event.get('date', '')}")

    actions = next_actions(state)
    if actions and not state.get("removed"):
        lines.extend(["", "NEXT RECOMMENDED:"])
        for a in actions[:3]:
            lines.append(f"  → {a['track']} round {a['round']}: {a['reason']}")
        lines.append("")
        lines.append("Run: python3 main.py campaign next")

    if state.get("history"):
        lines.extend(["", "RECENT HISTORY:"])
        for item in state["history"][-5:]:
            lines.append(f"  • {item}")

    return "\n".join(lines) + "\n"

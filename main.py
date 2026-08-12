#!/usr/bin/env python3
"""CLI for online harassment evidence, takedown requests, and monitoring."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.campaign import (
    format_status,
    generate_next_package,
    init_campaign,
    load_state,
    record_no_response,
    record_refusal,
    record_sent,
    record_success,
    save_state,
)
from src.config import load_config
from src.evidence import build_evidence_pack
from src.legal_guide import print_close_facebook_guide, print_legal_guide
from src.monitor import write_monitor_report
from src.osint import write_osint_report
from src.takedown import write_takedown_letters


def cmd_init(_: argparse.Namespace) -> int:
    example = Path("config.example.yaml")
    target = Path("config.yaml")
    if target.exists():
        print(f"config.yaml already exists at {target.resolve()}")
        return 0
    if not example.exists():
        print("config.example.yaml missing — cannot init.", file=sys.stderr)
        return 1
    target.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
    evidence_dir = Path("./evidence/screenshots")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created {target.resolve()}")
    print(f"Created {evidence_dir.resolve()} — add your screenshots there.")
    print("Edit config.yaml with your email, address, and Facebook post URL.")
    print("\nNext: python3 main.py campaign init")
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        pack_dir = build_evidence_pack(config)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Evidence pack created: {pack_dir.resolve()}")
    return 0


def cmd_letters(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    package_dir = write_takedown_letters(config)
    print(f"Campaign letters created: {package_dir.resolve()}")
    print("After sending, run: python3 main.py campaign sent --track meta --round 1")
    return 0


def cmd_osint(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    report_path = write_osint_report(config)
    print(f"OSINT report created: {report_path.resolve()}")
    return 0


def cmd_monitor(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    try:
        report_path = write_monitor_report(config)
    except ImportError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"Search monitor report: {report_path.resolve()}")
    return 0


def cmd_guide(args: argparse.Namespace) -> int:
    config = None
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        pass
    no_police = config.get("preferences", {}).get("no_police", True) if config else True
    print(print_legal_guide(no_police=no_police))
    return 0


def cmd_close(_: argparse.Namespace) -> int:
    print(print_close_facebook_guide())
    return 0


def cmd_campaign_init(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state = init_campaign(config)
    package_dir, generated = generate_next_package(config, state)
    save_state(state)
    print(format_status(state))
    print(f"\nPackage ready: {package_dir.resolve()}")
    print("Generated:", ", ".join(generated))
    print("\nSend the letters, then: python3 main.py campaign sent --track meta --round 1")
    return 0


def cmd_campaign_status(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state = load_state(Path(config["evidence"]["output_dir"]) / "campaign" / "state.json")
    print(format_status(state))
    return 0


def cmd_campaign_next(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state_path = Path(config["evidence"]["output_dir"]) / "campaign" / "state.json"
    state = load_state(state_path)
    package_dir, generated = generate_next_package(
        config,
        state,
        track=args.track,
        force_round=args.round,
    )
    save_state(state)
    print(format_status(state))
    print(f"\nNext package: {package_dir.resolve()}")
    print("Generated:", ", ".join(generated) if generated else "See README in package")
    return 0


def cmd_campaign_sent(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state_path = Path(config["evidence"]["output_dir"]) / "campaign" / "state.json"
    state = load_state(state_path)
    record_sent(state, args.track, args.round, reference=args.reference or "")
    save_state(state, state_path)
    print(format_status(state))
    print(f"\nRecorded: {args.track} round {args.round} sent.")
    print("If no removal in 7 days: python3 main.py campaign no-response --track", args.track)
    return 0


def cmd_campaign_refused(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state_path = Path(config["evidence"]["output_dir"]) / "campaign" / "state.json"
    state = load_state(state_path)
    record_refusal(state, args.track, args.reason)
    save_state(state, state_path)
    package_dir, generated = generate_next_package(config, state, track=args.track)
    save_state(state, state_path)
    print(format_status(state))
    print(f"\nRefusal recorded. Escalation package: {package_dir.resolve()}")
    print("Generated:", ", ".join(generated))
    return 0


def cmd_campaign_no_response(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state_path = Path(config["evidence"]["output_dir"]) / "campaign" / "state.json"
    state = load_state(state_path)
    record_no_response(state, args.track, args.days)
    save_state(state, state_path)
    package_dir, generated = generate_next_package(config, state, track=args.track)
    save_state(state, state_path)
    print(format_status(state))
    print(f"\nNo-response recorded ({args.days} days). Next package: {package_dir.resolve()}")
    print("Generated:", ", ".join(generated))
    return 0


def cmd_campaign_success(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    state_path = Path(config["evidence"]["output_dir"]) / "campaign" / "state.json"
    state = load_state(state_path)
    record_success(state, args.note or "")
    save_state(state, state_path)
    print(format_status(state))
    print("\nCongratulations — content removed. Run: python3 main.py close")
    return 0


def cmd_all(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    print("=== Step 1: Evidence pack ===")
    try:
        pack = build_evidence_pack(config)
        print(f"  Created: {pack}")
    except FileNotFoundError as exc:
        print(f"  Skipped: {exc}")

    print("\n=== Step 2: Campaign init (round 1 letters) ===")
    state = init_campaign(config)
    package_dir, generated = generate_next_package(config, state)
    save_state(state)
    print(f"  Created: {package_dir}")
    print(f"  Generated: {', '.join(generated)}")

    print("\n=== Step 3: OSINT documentation ===")
    osint = write_osint_report(config)
    print(f"  Created: {osint}")

    print("\n=== Step 4: Search monitor ===")
    try:
        monitor = write_monitor_report(config)
        print(f"  Created: {monitor}")
    except ImportError as exc:
        print(f"  Skipped: {exc}")

    print("\n=== Step 5: Send letters & track campaign ===")
    print("  python3 main.py campaign sent --track meta --round 1")
    print("  python3 main.py campaign status")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Multi-round removal campaign for online harassment (UK/NI).",
    )
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create config.yaml and evidence folders")
    sub.add_parser("evidence", help="Build hashed evidence pack from screenshots")
    sub.add_parser("letters", help="Generate round-1 campaign letters")
    sub.add_parser("osint", help="Document commenter handles")
    sub.add_parser("monitor", help="Scan public search for indexed URLs")
    sub.add_parser("guide", help="Print removal action guide")
    sub.add_parser("close", help="Checklist to close Facebook after removal")
    sub.add_parser("all", help="Evidence + campaign init + osint + monitor")

    campaign = sub.add_parser("campaign", help="Multi-round escalation campaign")
    campaign_sub = campaign.add_subparsers(dest="campaign_cmd", required=True)

    campaign_sub.add_parser("init", help="Start campaign and generate round 1 letters")
    campaign_sub.add_parser("status", help="Show campaign progress")

    p_next = campaign_sub.add_parser("next", help="Generate next escalation package")
    p_next.add_argument("--track", choices=["meta", "google", "ico"], default=None)
    p_next.add_argument("--round", type=int, default=None)

    p_sent = campaign_sub.add_parser("sent", help="Record that you sent a letter")
    p_sent.add_argument("--track", required=True, choices=["meta", "google", "ico"])
    p_sent.add_argument("--round", type=int, required=True)
    p_sent.add_argument("--reference", default="", help="ICO or Meta case reference")

    p_ref = campaign_sub.add_parser("refused", help="Record refusal and generate next round")
    p_ref.add_argument("--track", required=True, choices=["meta", "google", "ico"])
    p_ref.add_argument("--reason", required=True, help="What they said / why content remains")

    p_nr = campaign_sub.add_parser("no-response", help="Record silence and generate next round")
    p_nr.add_argument("--track", required=True, choices=["meta", "google", "ico"])
    p_nr.add_argument("--days", type=int, default=7)

    p_ok = campaign_sub.add_parser("success", help="Mark content as removed")
    p_ok.add_argument("--note", default="")

    args = parser.parse_args()

    if args.command == "campaign":
        campaign_handlers = {
            "init": cmd_campaign_init,
            "status": cmd_campaign_status,
            "next": cmd_campaign_next,
            "sent": cmd_campaign_sent,
            "refused": cmd_campaign_refused,
            "no-response": cmd_campaign_no_response,
            "success": cmd_campaign_success,
        }
        return campaign_handlers[args.campaign_cmd](args)

    handlers = {
        "init": cmd_init,
        "evidence": cmd_evidence,
        "letters": cmd_letters,
        "osint": cmd_osint,
        "monitor": cmd_monitor,
        "guide": cmd_guide,
        "close": cmd_close,
        "all": cmd_all,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())

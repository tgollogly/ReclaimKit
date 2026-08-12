#!/usr/bin/env python3
"""CLI for online harassment evidence, takedown requests, and monitoring."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.config import load_config
from src.evidence import build_evidence_pack
from src.legal_guide import print_legal_guide
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
    letter_dir = write_takedown_letters(config)
    print(f"Takedown letters created: {letter_dir.resolve()}")
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


def cmd_guide(_: argparse.Namespace) -> int:
    print(print_legal_guide())
    return 0


def cmd_all(args: argparse.Namespace) -> int:
    """Run full workflow: evidence (if present), letters, osint, monitor, guide summary."""
    config = load_config(args.config)
    print("=== Step 1: Evidence pack ===")
    try:
        pack = build_evidence_pack(config)
        print(f"  Created: {pack}")
    except FileNotFoundError as exc:
        print(f"  Skipped: {exc}")

    print("\n=== Step 2: Takedown letters ===")
    letters = write_takedown_letters(config)
    print(f"  Created: {letters}")

    print("\n=== Step 3: OSINT documentation ===")
    osint = write_osint_report(config)
    print(f"  Created: {osint}")

    print("\n=== Step 4: Search monitor ===")
    try:
        monitor = write_monitor_report(config)
        print(f"  Created: {monitor}")
    except ImportError as exc:
        print(f"  Skipped: {exc}")

    print("\n=== Step 5: Legal guide ===")
    print("  Run: python main.py guide")
    print("\nDone. Review output/ folder and submit letters to Meta and Google.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evidence, takedown letters, OSINT docs, and search monitoring "
        "for online harassment (UK/NI).",
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to config file (default: config.yaml)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create config.yaml from example and evidence folders")
    sub.add_parser("evidence", help="Build hashed evidence pack from screenshots")
    sub.add_parser("letters", help="Generate Meta GDPR and Google removal letter drafts")
    sub.add_parser("osint", help="Document commenter handles and legal ID pathways")
    sub.add_parser("monitor", help="Scan public search for indexed harmful URLs")
    sub.add_parser("guide", help="Print NI legal action guide")
    sub.add_parser("all", help="Run evidence + letters + osint + monitor")

    args = parser.parse_args()
    handlers = {
        "init": cmd_init,
        "evidence": cmd_evidence,
        "letters": cmd_letters,
        "osint": cmd_osint,
        "monitor": cmd_monitor,
        "guide": cmd_guide,
        "all": cmd_all,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())

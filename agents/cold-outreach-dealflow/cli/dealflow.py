"""CLI for Cold Outreach Dealflow (end-to-end hardened: runs from any cwd)."""
import os
import sys
import importlib.util

_AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_REPO_ROOT = os.path.abspath(os.path.join(_AGENT_DIR, ".."))
for _p in (_REPO_ROOT, _AGENT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load(name: str, relpath: str):
    """Load engine module by explicit file path (hyphenated dirs are not importable)."""
    path = os.path.join(_AGENT_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_engine_mod = _load("core.outreach_engine", "core/outreach_engine.py")
ColdOutreachDealflow = _engine_mod.ColdOutreachDealflow

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Cold Outreach Dealflow CLI")
    sub = parser.add_subparsers(dest="command")

    p_seq = sub.add_parser("sequence", help="Generate 3-touchpoint technical B2B email sequence")
    p_seq.add_argument("--name", default="Sarah Jenkins", help="Target contact name")
    p_seq.add_argument("--company", default="MantleFinance", help="Target company")
    p_seq.add_argument("--stack", default="Solana & Rust", help="Target tech stack")

    p_sow = sub.add_parser("sow", help="Generate formal Statement of Work (SOW) contract")
    p_sow.add_argument("--client", default="MantleFinance", help="Client name")
    p_sow.add_argument("--scope", default="Autonomous agent streaming engine & DEX arbitrage pipeline", help="Scope summary")
    p_sow.add_argument("--fee", type=float, default=9500.0, help="Total fee USD")

    args = parser.parse_args()

    if args.command == "sequence":
        touches = ColdOutreachDealflow.generate_sequence(args.name, args.company, args.stack)
        print(f"📬 3-Touchpoint B2B Technical Sequence for {args.name} ({args.company}):\n")
        for t in touches:
            print(f"--- TOUCHPOINT {t.step_number} (Deliverability: {int(t.deliverability_score*100)}%) ---")
            print(f"Subject: {t.subject}\n")
            print(f"{t.body}\n")
    elif args.command == "sow":
        proposal = ColdOutreachDealflow.generate_sow(args.client, args.scope, args.fee)
        print("📄 Statement of Work (SOW) Generated:")
        print(proposal.sow_markdown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

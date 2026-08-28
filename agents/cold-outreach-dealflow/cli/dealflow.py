"""CLI for Cold Outreach Dealflow"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.cold_outreach_dealflow.core.outreach_engine import ColdOutreachDealflow


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
        print(f"📬 3-Touchpoint B2B Technical Sequence for {args.name} ({args.company}):
")
        for t in touches:
            print(f"--- TOUCHPOINT {t.step_number} (Deliverability: {int(t.deliverability_score*100)}%) ---")
            print(f"Subject: {t.subject}
")
            print(f"{t.body}
")
    elif args.command == "sow":
        proposal = ColdOutreachDealflow.generate_sow(args.client, args.scope, args.fee)
        print("📄 Statement of Work (SOW) Generated:")
        print(proposal.sow_markdown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

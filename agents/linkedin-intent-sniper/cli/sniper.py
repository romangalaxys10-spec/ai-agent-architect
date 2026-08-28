"""CLI for LinkedIn Intent Sniper"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.linkedin_intent_sniper.core.intent_engine import LinkedInIntentSniper


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Intent Sniper CLI")
    sub = parser.add_subparsers(dest="command")

    p_snipe = sub.add_parser("snipe", help="Analyze prospect profile and draft tailored outreach note")
    p_snipe.add_argument("--name", default="Alex Rivera", help="Prospect name")
    p_snipe.add_argument("--headline", default="CTO at SolanaScale | Scaling DEX infrastructure", help="Headline")
    p_snipe.add_argument("--company", default="SolanaScale", help="Company name")
    p_snipe.add_argument("--post", default="Struggling with slot latency and RPC dropouts during high volatility...", help="Recent post")

    args = parser.parse_args()

    if args.command == "snipe":
        prospect = LinkedInIntentSniper.analyze_prospect(args.name, args.headline, args.company, args.post)
        print(f"🎯 LinkedIn Prospect Intent Analysis for {args.name}:")
        print(json.dumps(prospect.__dict__, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

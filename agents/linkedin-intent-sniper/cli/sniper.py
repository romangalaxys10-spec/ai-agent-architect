"""CLI for Linkedin Intent Sniper (end-to-end hardened: runs from any cwd)."""
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


_engine_mod = _load("core.intent_engine", "core/intent_engine.py")
LinkedInIntentSniper = _engine_mod.LinkedInIntentSniper

import argparse
import json


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

"""CLI for the Steve Jobs Agent — focus audits and binary quality verdicts."""
import os
import sys

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for _p in (_REPO_ROOT, _AGENT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import argparse
from core.focus_engine import SteveJobsFocusEngine


def main():
    parser = argparse.ArgumentParser(
        description="Steve Jobs Agent — Focus filter, Rule of Three, binary verdicts"
    )
    parser.add_argument("--name", required=True, help="Product / agent name")
    parser.add_argument("--pitch", required=True, help="One-sentence pitch")
    parser.add_argument("--features", required=True, help="Comma-separated feature list")
    args = parser.parse_args()

    features = [f.strip() for f in args.features.split(",") if f.strip()]
    audit = SteveJobsFocusEngine.audit(args.name, args.pitch, features)
    print(SteveJobsFocusEngine.format_audit(audit))


if __name__ == "__main__":
    main()

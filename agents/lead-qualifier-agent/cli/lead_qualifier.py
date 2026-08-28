"""CLI for the Lead Qualifier Agent — Scores leads on BANT evidence, tiers MQL/SQL, and writes the disqualifier truth"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _pick(inline, path):
    if path:
        return _read(path)
    return inline or ""


def main():
    parser = argparse.ArgumentParser(description='Lead Qualifier Agent — BANT scoring + tiering + next actions')
    parser.add_argument('--lead', help='Lead profile text (inline)')
    parser.add_argument('--file', help='Path to a lead profile file')
    args = parser.parse_args()

    from core.lead_qualifier_engine import LeadQualifierEngine
    text = _pick(args.lead, args.file)
    if not text.strip():
        raise SystemExit("Provide --lead or --file")
    verdict = LeadQualifierEngine.qualify(text)
    print(LeadQualifierEngine.format_verdict(verdict))


if __name__ == "__main__":
    main()

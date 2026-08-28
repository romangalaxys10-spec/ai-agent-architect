"""CLI for the Fact Check Agent — Decomposes claims into atomic assertions and verifies each against evidence"""
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
    parser = argparse.ArgumentParser(description='Fact Check Agent — atomic claim verification with evidence trail')
    parser.add_argument('--claim', required=True, help='Claim to verify')
    parser.add_argument('--evidence', help="Evidence texts separated by lines of '---' (inline)")
    parser.add_argument('--file', help='Path to evidence file (blocks separated by ---)')
    args = parser.parse_args()

    from core.fact_check_engine import FactCheckEngine
    text = _pick(args.evidence, args.file)
    blocks = [b.strip() for b in text.split("\n---\n") if b.strip()] if text.strip() else []
    report = FactCheckEngine.verify(args.claim, blocks)
    print(FactCheckEngine.format_report(report))


if __name__ == "__main__":
    main()

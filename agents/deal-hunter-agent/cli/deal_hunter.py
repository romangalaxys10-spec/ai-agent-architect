"""CLI for the Deal Hunter Agent — Evaluates deals: price history percentile, rating confidence, buy/wait verdict"""
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
    parser = argparse.ArgumentParser(description='Deal Hunter Agent — deal evaluation with buy/wait verdicts')
    parser.add_argument('--candidates', help='JSON array of products (inline)')
    parser.add_argument('--file', help='Path to a JSON products file')
    parser.add_argument('--needs', default='', help='Comma-separated must-have features')
    args = parser.parse_args()

    from core.deal_hunter_engine import DealHunterEngine
    raw = _pick(args.candidates, args.file)
    if not raw.strip():
        raise SystemExit("Provide --candidates or --file")
    import json as _json
    try:
        candidates = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Candidates JSON parse error: {e}")
    needs = [n.strip() for n in args.needs.split(",") if n.strip()]
    verdict = DealHunterEngine.evaluate(candidates, needs=needs)
    print(DealHunterEngine.format_verdict(verdict))


if __name__ == "__main__":
    main()

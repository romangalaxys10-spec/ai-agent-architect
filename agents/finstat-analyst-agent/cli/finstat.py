"""CLI for the FinStat Analyst Agent — Analyzes financial statements: margins, burn, runway, red flags, health score"""
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
    parser = argparse.ArgumentParser(description='FinStat Analyst Agent — statement analysis + red flags + health score')
    parser.add_argument('--data', help='JSON {periods: [...], items: {revenue: [...], ...}} (inline)')
    parser.add_argument('--file', help='Path to a JSON statements file')
    args = parser.parse_args()

    from core.finstat_engine import FinStatAnalystEngine
    raw = _pick(args.data, args.file)
    if not raw.strip():
        raise SystemExit("Provide --data or --file")
    import json as _json
    try:
        data = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Statements JSON parse error: {e}")
    analysis = FinStatAnalystEngine.analyze(data)
    print(FinStatAnalystEngine.format_analysis(analysis))


if __name__ == "__main__":
    main()

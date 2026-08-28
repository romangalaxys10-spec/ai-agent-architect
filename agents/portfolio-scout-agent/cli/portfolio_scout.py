"""CLI for the Portfolio Scout Agent — Reviews holdings: allocation drift, concentration, correlation proxy, rebalance plan"""
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
    parser = argparse.ArgumentParser(description='Portfolio Scout Agent — allocation + concentration + rebalance plan')
    parser.add_argument('--holdings', help='JSON array of holdings (inline)')
    parser.add_argument('--file', help='Path to a JSON holdings file')
    args = parser.parse_args()

    from core.portfolio_scout_engine import PortfolioScoutEngine
    raw = _pick(args.holdings, args.file)
    if not raw.strip():
        raise SystemExit("Provide --holdings or --file")
    import json as _json
    try:
        holdings = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Holdings JSON parse error: {e}")
    report = PortfolioScoutEngine.analyze(holdings)
    print(PortfolioScoutEngine.format_report(report))


if __name__ == "__main__":
    main()

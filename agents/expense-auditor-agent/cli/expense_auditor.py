"""CLI for the Expense Auditor Agent — Audits expense reports: caps, categories, duplicates, suspicious patterns"""
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
    parser = argparse.ArgumentParser(description='Expense Auditor Agent — policy compliance + fraud heuristics')
    parser.add_argument('--expenses', help='JSON array of expense lines (inline)')
    parser.add_argument('--file', help='Path to a JSON expenses file')
    parser.add_argument('--meal-cap', type=float, default=75.0, help='Per-meal cap')
    parser.add_argument('--hotel-cap', type=float, default=250.0, help='Per-night hotel cap')
    args = parser.parse_args()

    from core.expense_auditor_engine import ExpenseAuditorEngine
    raw = _pick(args.expenses, args.file)
    if not raw.strip():
        raise SystemExit("Provide --expenses or --file")
    import json as _json
    try:
        expenses = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Expenses JSON parse error: {e}")
    policy = {"meal_cap": args.meal_cap, "hotel_cap": args.hotel_cap}
    report = ExpenseAuditorEngine.audit(expenses, policy=policy)
    print(ExpenseAuditorEngine.format_report(report))


if __name__ == "__main__":
    main()

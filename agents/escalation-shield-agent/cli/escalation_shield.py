"""CLI for the Escalation Shield Agent — Computes churn-risk from account signals and prescribes the save play before escalation"""
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
    parser = argparse.ArgumentParser(description='Escalation Shield Agent — churn risk scoring + save-play prescription')
    parser.add_argument('--signals', help='JSON account signals (inline)')
    parser.add_argument('--file', help='Path to a JSON signals file')
    args = parser.parse_args()

    from core.escalation_shield_engine import EscalationShieldEngine
    raw = _pick(args.signals, args.file)
    if not raw.strip():
        raise SystemExit("Provide --signals or --file")
    import json as _json
    try:
        data = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Signals JSON parse error: {e}")
    assessment = EscalationShieldEngine.assess(data)
    print(EscalationShieldEngine.format_assessment(assessment))


if __name__ == "__main__":
    main()

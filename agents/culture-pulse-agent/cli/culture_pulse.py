"""CLI for the Culture Pulse Agent — Analyzes engagement surveys: eNPS, distribution, comment themes, segment gaps"""
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
    parser = argparse.ArgumentParser(description='Culture Pulse Agent — engagement survey analysis + interventions')
    parser.add_argument('--survey', help='JSON array of responses {segment, score, comment} (inline)')
    parser.add_argument('--file', help='Path to a JSON responses file')
    args = parser.parse_args()

    from core.culture_pulse_engine import CulturePulseEngine
    raw = _pick(args.survey, args.file)
    if not raw.strip():
        raise SystemExit("Provide --survey or --file")
    import json as _json
    try:
        responses = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Survey JSON parse error: {e}")
    report = CulturePulseEngine.analyze(responses)
    print(CulturePulseEngine.format_report(report))


if __name__ == "__main__":
    main()

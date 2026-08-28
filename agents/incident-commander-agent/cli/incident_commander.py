"""CLI for the Incident Commander Agent — Classifies severity, runs the response runbook, drafts comms and postmortem"""
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
    parser = argparse.ArgumentParser(description='Incident Commander Agent — SEV classification + runbook + comms')
    parser.add_argument('--signals', help='Alert/monitor text (inline)')
    parser.add_argument('--file', help='Path to a signals file')
    args = parser.parse_args()

    from core.incident_commander_engine import IncidentCommanderEngine
    text = _pick(args.signals, args.file)
    if not text.strip():
        raise SystemExit("Provide --signals or --file")
    plan = IncidentCommanderEngine.command(text)
    print(IncidentCommanderEngine.format_plan(plan))


if __name__ == "__main__":
    main()

"""CLI for the Bug Triage Agent — Classifies bug reports, builds repro checklists, and ranks root-cause hypotheses"""
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
    parser = argparse.ArgumentParser(description='Bug Triage Agent — defect classification, repro checklist, RCA hypotheses')
    parser.add_argument('--report', help='Bug report text (inline)')
    parser.add_argument('--file', help='Path to a bug report file')
    args = parser.parse_args()

    from core.bug_triage_engine import BugTriageEngine
    text = _pick(args.report, args.file)
    if not text.strip():
        raise SystemExit("Provide --report or --file")
    report = BugTriageEngine.triage(text)
    print(BugTriageEngine.format_report(report))


if __name__ == "__main__":
    main()

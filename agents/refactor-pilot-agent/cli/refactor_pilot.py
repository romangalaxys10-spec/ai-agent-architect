"""CLI for the Refactor Pilot Agent — Detects code smells and flies a risk-gated, step-by-step refactoring flight plan"""
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
    parser = argparse.ArgumentParser(description='Refactor Pilot Agent — smell detection + risk-gated refactoring plan')
    parser.add_argument('--file', help='Path to the Python source file')
    parser.add_argument('--source', help='Python source code inline')
    parser.add_argument('--aggressiveness', type=int, default=2, choices=[1, 2, 3], help='1=safe, 2=balanced, 3=deep')
    args = parser.parse_args()

    from core.refactor_pilot_engine import RefactorPilotEngine
    source = _pick(args.source, args.file)
    if not source.strip():
        raise SystemExit("Provide --source or --file")
    plan = RefactorPilotEngine.plan(source, aggressiveness=args.aggressiveness)
    print(RefactorPilotEngine.format_plan(plan))


if __name__ == "__main__":
    main()

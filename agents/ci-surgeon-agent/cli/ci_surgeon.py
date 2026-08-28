"""CLI for the CI Surgeon Agent — Parses CI failure logs, isolates root cause class, and prescribes the fix playbook"""
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
    parser = argparse.ArgumentParser(description='CI Surgeon Agent — CI failure diagnosis with fix playbooks')
    parser.add_argument('--log', help='CI log text (inline)')
    parser.add_argument('--file', help='Path to a CI log file')
    args = parser.parse_args()

    from core.ci_surgeon_engine import CISurgeonEngine
    text = _pick(args.log, args.file)
    if not text.strip():
        raise SystemExit("Provide --log or --file")
    diag = CISurgeonEngine.diagnose(text)
    print(CISurgeonEngine.format_diagnosis(diag))


if __name__ == "__main__":
    main()

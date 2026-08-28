"""CLI for the Dependency Guardian Agent — Audits dependency manifests for risk, staleness, and safe upgrade ordering"""
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
    parser = argparse.ArgumentParser(description='Dependency Guardian Agent — dependency risk audit + upgrade ordering')
    parser.add_argument('--deps', help='requirements.txt-style content (inline)')
    parser.add_argument('--file', help='Path to requirements.txt')
    args = parser.parse_args()

    from core.dep_guardian_engine import DepGuardianEngine
    text = _pick(args.deps, args.file)
    if not text.strip():
        raise SystemExit("Provide --deps or --file")
    audit = DepGuardianEngine.audit(text)
    print(DepGuardianEngine.format_audit(audit))


if __name__ == "__main__":
    main()

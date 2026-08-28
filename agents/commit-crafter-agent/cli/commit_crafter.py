"""CLI for the Commit Crafter Agent — Turns raw diffs into conventional commits, changelog entries, and semver bumps"""
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
    parser = argparse.ArgumentParser(description='Commit Crafter Agent — conventional commits + changelog + semver')
    parser.add_argument('--diff', help='Unified diff text (inline)')
    parser.add_argument('--file', help='Path to a .diff/.patch file')
    parser.add_argument('--breaking', action='store_true', help='Hint that the change is breaking')
    args = parser.parse_args()

    from core.commit_crafter_engine import CommitCrafterEngine
    text = _pick(args.diff, args.file)
    if not text.strip():
        raise SystemExit("Provide --diff or --file")
    pack = CommitCrafterEngine.craft(text, breaking_hint=args.breaking)
    print(CommitCrafterEngine.format_pack(pack))


if __name__ == "__main__":
    main()

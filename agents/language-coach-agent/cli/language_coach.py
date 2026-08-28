"""CLI for the Language Coach Agent — Analyzes learner writing: level estimate, error taxonomy, drills, CEFR path"""
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
    parser = argparse.ArgumentParser(description='Language Coach Agent — learner text analysis + drill generation')
    parser.add_argument('--text', help='Learner text (inline)')
    parser.add_argument('--file', help='Path to a learner text file')
    parser.add_argument('--target-lang', default='english', help='Language being learned')
    parser.add_argument('--level', default='unknown', choices=['unknown', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'], help='Known level (else estimated)')
    args = parser.parse_args()

    from core.language_coach_engine import LanguageCoachEngine
    text = _pick(args.text, args.file)
    if not text.strip():
        raise SystemExit("Provide --text or --file")
    plan = LanguageCoachEngine.coach(text, target_lang=args.target_lang, level=args.level)
    print(LanguageCoachEngine.format_plan(plan))


if __name__ == "__main__":
    main()

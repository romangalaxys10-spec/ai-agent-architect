"""CLI for the Interview Coach Agent — Designs structured interviews: question bank, rubrics, legal guardrails, scorecards"""
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
    parser = argparse.ArgumentParser(description='Interview Coach Agent — structured interview design + rubrics')
    parser.add_argument('--role', required=True, help='Role title')
    parser.add_argument('--level', default='senior', choices=['junior', 'mid', 'senior', 'staff', 'principal'], help='Level')
    parser.add_argument('--competencies', default='coding, system design, collaboration, ownership', help='Comma-separated competencies')
    args = parser.parse_args()

    from core.interview_coach_engine import InterviewCoachEngine
    comps = [c.strip() for c in args.competencies.split(",") if c.strip()]
    kit = InterviewCoachEngine.design(args.role, args.level, comps)
    print(InterviewCoachEngine.format_kit(kit))


if __name__ == "__main__":
    main()

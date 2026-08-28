"""CLI for the Onboarding Guide Agent — Builds 30/60/90 onboarding plans with week-1 schedule, access, buddy wiring"""
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
    parser = argparse.ArgumentParser(description='Onboarding Guide Agent — 30/60/90 plans + week-1 schedule')
    parser.add_argument('--role', required=True, help='Role title')
    parser.add_argument('--team', default='Platform Engineering', help='Team name')
    parser.add_argument('--start-date', default='Monday', help='Start date or weekday')
    args = parser.parse_args()

    from core.onboarding_guide_engine import OnboardingGuideEngine
    plan = OnboardingGuideEngine.plan(args.role, args.team, args.start_date)
    print(OnboardingGuideEngine.format_plan(plan))


if __name__ == "__main__":
    main()

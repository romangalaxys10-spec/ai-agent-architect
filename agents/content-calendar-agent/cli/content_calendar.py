"""CLI for the Content Calendar Agent — Generates 4-week calendars with format mix, hooks, and channel adaptations"""
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
    parser = argparse.ArgumentParser(description='Content Calendar Agent — editorial calendar generation')
    parser.add_argument('--goal', required=True, help='Content goal')
    parser.add_argument('--audience', default='technical practitioners', help='Target audience')
    parser.add_argument('--channels', default='blog, linkedin, x', help='Comma-separated channels')
    parser.add_argument('--weeks', type=int, default=4, help='Calendar length in weeks')
    args = parser.parse_args()

    from core.content_calendar_engine import ContentCalendarEngine
    channels = [c.strip() for c in args.channels.split(",") if c.strip()]
    calendar = ContentCalendarEngine.generate(args.goal, args.audience, channels, weeks=args.weeks)
    print(ContentCalendarEngine.format_calendar(calendar))


if __name__ == "__main__":
    main()

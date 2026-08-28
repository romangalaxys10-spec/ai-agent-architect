"""CLI for the Meeting Brief Agent — Builds pre-meeting briefs: attendee map, agenda, talk tracks, objection plays"""
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
    parser = argparse.ArgumentParser(description='Meeting Brief Agent — pre-meeting briefing generation')
    parser.add_argument('--topic', required=True, help='Meeting topic')
    parser.add_argument('--attendees', required=True, help='Comma-separated attendee names w/ optional roles')
    parser.add_argument('--context', default='', help='Account / project context notes')
    args = parser.parse_args()

    from core.meeting_brief_engine import MeetingBriefEngine
    attendees = [a.strip() for a in args.attendees.split(",") if a.strip()]
    brief = MeetingBriefEngine.brief(args.topic, attendees, args.context)
    print(MeetingBriefEngine.format_brief(brief))


if __name__ == "__main__":
    main()

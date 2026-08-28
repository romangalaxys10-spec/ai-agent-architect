"""CLI for the Meeting Scribe Agent — Converts raw meeting notes/transcripts into decisions, owners, deadlines, questions"""
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
    parser = argparse.ArgumentParser(description='Meeting Scribe Agent — notes to decisions + action items')
    parser.add_argument('--notes', help='Meeting notes/transcript text (inline)')
    parser.add_argument('--file', help='Path to a notes file')
    args = parser.parse_args()

    from core.meeting_scribe_engine import MeetingScribeEngine
    text = _pick(args.notes, args.file)
    if not text.strip():
        raise SystemExit("Provide --notes or --file")
    digest = MeetingScribeEngine.extract(text)
    print(MeetingScribeEngine.format_digest(digest))


if __name__ == "__main__":
    main()

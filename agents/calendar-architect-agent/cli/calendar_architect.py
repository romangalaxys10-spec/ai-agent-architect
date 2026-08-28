"""CLI for the Calendar Architect Agent — Schedules tasks against real constraints: deadlines, energy, focus blocks, conflicts"""
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
    parser = argparse.ArgumentParser(description='Calendar Architect Agent — constraint-aware day scheduling')
    parser.add_argument('--day', help='JSON day spec {work_start, work_end, meetings[], tasks[]} (inline)')
    parser.add_argument('--file', help='Path to a JSON day spec')
    args = parser.parse_args()

    from core.calendar_architect_engine import CalendarArchitectEngine
    raw = _pick(args.day, args.file)
    if not raw.strip():
        raise SystemExit("Provide --day or --file")
    import json as _json
    try:
        spec = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Day JSON parse error: {e}")
    schedule = CalendarArchitectEngine.schedule(spec)
    print(CalendarArchitectEngine.format_schedule(schedule))


if __name__ == "__main__":
    main()

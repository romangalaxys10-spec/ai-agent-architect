"""CLI for the SLA Sentinel Agent — Projects SLA breach risk per ticket and orders the queue by preventable-breach value"""
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
    parser = argparse.ArgumentParser(description='SLA Sentinel Agent — breach projection + queue intervention order')
    parser.add_argument('--queue', help='JSON array of tickets (inline)')
    parser.add_argument('--file', help='Path to a JSON ticket queue file')
    args = parser.parse_args()

    from core.sla_sentinel_engine import SLASentinelEngine
    raw = _pick(args.queue, args.file)
    if not raw.strip():
        raise SystemExit("Provide --queue or --file")
    import json as _json
    try:
        tickets = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Queue JSON parse error: {e}")
    projection = SLASentinelEngine.project(tickets)
    print(SLASentinelEngine.format_projection(projection))


if __name__ == "__main__":
    main()

"""CLI for the Ticket Router Agent — Classifies support tickets, extracts entities, and routes to queue with SLA clock"""
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
    parser = argparse.ArgumentParser(description='Ticket Router Agent — intent classification + queue routing + SLA')
    parser.add_argument('--ticket', help='Ticket text (inline)')
    parser.add_argument('--file', help='Path to a ticket text file')
    args = parser.parse_args()

    from core.ticket_router_engine import TicketRouterEngine
    text = _pick(args.ticket, args.file)
    if not text.strip():
        raise SystemExit("Provide --ticket or --file")
    decision = TicketRouterEngine.route(text)
    print(TicketRouterEngine.format_decision(decision))


if __name__ == "__main__":
    main()

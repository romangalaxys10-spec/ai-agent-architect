"""CLI for the Trip Compass Agent — Builds day-by-day itineraries with pacing, budget split, packing, contingencies"""
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
    parser = argparse.ArgumentParser(description='Trip Compass Agent — itinerary + budget + packing + contingencies')
    parser.add_argument('--destination', required=True, help='Destination')
    parser.add_argument('--days', type=int, default=3, help='Trip length in days')
    parser.add_argument('--preferences', default='culture, food, walking', help='Comma-separated interests')
    parser.add_argument('--budget', type=float, default=1000.0, help='Total budget')
    parser.add_argument('--pace', default='balanced', choices=['relaxed', 'balanced', 'intense'], help='Daily pace')
    args = parser.parse_args()

    from core.trip_compass_engine import TripCompassEngine
    prefs = [p.strip() for p in args.preferences.split(",") if p.strip()]
    itinerary = TripCompassEngine.plan(args.destination, args.days, prefs, args.budget, pace=args.pace)
    print(TripCompassEngine.format_itinerary(itinerary))


if __name__ == "__main__":
    main()

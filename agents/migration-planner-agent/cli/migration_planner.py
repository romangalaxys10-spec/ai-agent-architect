"""CLI for the Migration Planner Agent — Plans framework/version migrations as phased, reversible, dual-run campaigns"""
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
    parser = argparse.ArgumentParser(description='Migration Planner Agent — phased migration campaign planning')
    parser.add_argument('--from', dest='from_tech', required=True, help="Current tech (e.g. 'Python 3.9')")
    parser.add_argument('--to', dest='to_tech', required=True, help="Target tech (e.g. 'Python 3.12')")
    parser.add_argument('--inventory', default='', help='Optional code inventory text (file listing / grep output)')
    args = parser.parse_args()

    from core.migration_planner_engine import MigrationPlannerEngine
    plan = MigrationPlannerEngine.plan(args.from_tech, args.to_tech, args.inventory)
    print(MigrationPlannerEngine.format_plan(plan))


if __name__ == "__main__":
    main()

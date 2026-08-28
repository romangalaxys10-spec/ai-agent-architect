"""CLI for the Cloud Cost Optimizer Agent — Finds idle and oversized resources, computes waste, and writes the savings plan"""
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
    parser = argparse.ArgumentParser(description='Cloud Cost Optimizer Agent — waste detection + savings plan')
    parser.add_argument('--inventory', help='JSON array of resources (inline)')
    parser.add_argument('--file', help='Path to a JSON inventory file')
    args = parser.parse_args()

    from core.cloud_cost_engine import CloudCostOptimizerEngine
    raw = _pick(args.inventory, args.file)
    if not raw.strip():
        raise SystemExit("Provide --inventory or --file")
    import json as _json
    try:
        inventory = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Inventory JSON parse error: {e}")
    plan = CloudCostOptimizerEngine.optimize(inventory)
    print(CloudCostOptimizerEngine.format_plan(plan))


if __name__ == "__main__":
    main()

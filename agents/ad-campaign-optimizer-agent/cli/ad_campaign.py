"""CLI for the Ad Campaign Optimizer Agent — Computes CTR/CPC/CPA/ROAS, flags waste, and reallocates budget with experiment plan"""
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
    parser = argparse.ArgumentParser(description='Ad Campaign Optimizer Agent — performance audit + budget reallocation')
    parser.add_argument('--campaigns', help='JSON array of campaign stat rows (inline)')
    parser.add_argument('--file', help='Path to a JSON campaigns file')
    parser.add_argument('--breakeven-roas', type=float, default=2.0, help='Breakeven ROAS (default 2.0)')
    args = parser.parse_args()

    from core.ad_campaign_engine import AdCampaignOptimizerEngine
    raw = _pick(args.campaigns, args.file)
    if not raw.strip():
        raise SystemExit("Provide --campaigns or --file")
    import json as _json
    try:
        campaigns = _json.loads(raw)
    except _json.JSONDecodeError as e:
        raise SystemExit(f"Campaigns JSON parse error: {e}")
    plan = AdCampaignOptimizerEngine.optimize(campaigns, breakeven_roas=args.breakeven_roas)
    print(AdCampaignOptimizerEngine.format_plan(plan))


if __name__ == "__main__":
    main()

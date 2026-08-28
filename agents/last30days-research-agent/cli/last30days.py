"""CLI for Last 30 Days Research Agent"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from core.recency_radar import RecencyRadarEngine


def main():
    parser = argparse.ArgumentParser(description="Last 30 Days Research Agent CLI")
    parser.add_argument("--query", required=True, help="Topic or ecosystem to research over the trailing 30 days")
    
    args = parser.parse_args()
    report = RecencyRadarEngine.curate_recent_intel(args.query)
    print(f"🛰️ Recency Intelligence Report for '{args.query}' ({report.timeframe}):")
    print("
--- TOP COMMUNITY CONSENSUS FINDINGS ---")
    for f in report.top_consensus_findings:
        print(f"• {f}")
    print("
--- CONTRARIAN DEVELOPER VIEWS ---")
    for c in report.contrarian_community_views:
        print(f"• {c}")
    print("
--- RECENT COMMUNITY SIGNALS ---")
    for s in report.signals:
        print(f"[{s.source}] {s.title} ({s.engagement_metric}, {s.timestamp_days_ago}d ago): {s.key_insight}")


if __name__ == "__main__":
    main()

"""CLI for Anti-Slop Content Engine"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.anti_slop_content_engine.core.content_engine import AntiSlopContentEngine


def main():
    parser = argparse.ArgumentParser(description="Anti-Slop Content Engine CLI")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("create", help="Generate viral X thread and LinkedIn technical case study")
    p_gen.add_argument("--topic", default="Building Zero-Credit Anti-Slop AI Agents", help="Topic headline")
    p_gen.add_argument("--breakthrough", default="Self-contained deterministic design engine with zero third-party credits", help="Breakthrough details")
    p_gen.add_argument("--metrics", default="0.04ms latency, 100% local execution, 0$ credit cost", help="Metrics achieved")

    args = parser.parse_args()

    if args.command == "create":
        pkg = AntiSlopContentEngine.synthesize_content(args.topic, args.breakthrough, args.metrics)
        print("✍️ Anti-Slop Content Package Synthesized:")
        print(f"• Slop Linter Passed: {pkg.slop_linter_passed}")
        print("
--- X/TWITTER THREAD ---")
        for i, tw in enumerate(pkg.x_thread_tweets):
            print(f"[{i+1}/{len(pkg.x_thread_tweets)}]
{tw}
")
        print("--- LINKEDIN POST ---")
        print(pkg.linkedin_post)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

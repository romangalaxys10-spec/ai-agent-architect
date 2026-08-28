"""CLI for Discord Community Radar"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.discord_community_radar.core.radar_engine import DiscordCommunityRadar


def main():
    parser = argparse.ArgumentParser(description="Discord Community Radar CLI")
    sub = parser.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="Scan message text for high-value intent signals")
    p_scan.add_argument("--author", default="solana_founder_42", help="Author username")
    p_scan.add_argument("--channel", default="#dev-help", help="Discord channel")
    p_scan.add_argument("--msg", default="Need an experienced engineer to build a Yellowstone gRPC sniper bot, $5k budget. Who is free?", help="Message text")

    args = parser.parse_args()

    if args.command == "scan":
        sig = DiscordCommunityRadar.process_message(args.author, args.channel, args.msg)
        print("🛰️ Discord Community Telemetry Radar:")
        print(json.dumps(sig.__dict__, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

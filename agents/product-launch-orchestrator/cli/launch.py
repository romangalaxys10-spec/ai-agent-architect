"""CLI for Product Launch Orchestrator"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import argparse
import json
from agents.product_launch_orchestrator.core.launch_engine import ProductLaunchOrchestrator


def main():
    parser = argparse.ArgumentParser(description="Product Launch Orchestrator CLI")
    sub = parser.add_subparsers(dest="command")

    p_pkg = sub.add_parser("create", help="Generate full multi-platform launch campaign package")
    p_pkg.add_argument("--name", default="SuperDesign Agent", help="Product/Repo name")
    p_pkg.add_argument("--url", default="https://github.com/romangalaxys10-spec/superdesign-agent", help="GitHub repo URL")

    args = parser.parse_args()

    if args.command == "create":
        camp = ProductLaunchOrchestrator.generate_launch_package(args.name, args.url)
        print("🚀 Multi-Platform Product Launch Package Created:")
        print(f"• Target Product: {camp.product_name}")
        print("
--- SHOW HN POST ---")
        print(camp.show_hn_post)
        print("
--- PRODUCT HUNT PITCH ---")
        print(json.dumps(camp.product_hunt_pitch, indent=2))
        print("
--- 3-DAY LAUNCH TIMELINE ---")
        for step in camp.three_day_timeline:
            print(f"• [{step['day']}]: {step['action']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

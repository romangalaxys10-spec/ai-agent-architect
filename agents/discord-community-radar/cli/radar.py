"""CLI for Discord Community Radar (end-to-end hardened: runs from any cwd)."""
import os
import sys
import importlib.util

_AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_REPO_ROOT = os.path.abspath(os.path.join(_AGENT_DIR, ".."))
for _p in (_REPO_ROOT, _AGENT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load(name: str, relpath: str):
    """Load engine module by explicit file path (hyphenated dirs are not importable)."""
    path = os.path.join(_AGENT_DIR, relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_engine_mod = _load("core.radar_engine", "core/radar_engine.py")
DiscordCommunityRadar = _engine_mod.DiscordCommunityRadar

import argparse
import json


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

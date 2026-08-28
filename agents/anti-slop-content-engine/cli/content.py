"""CLI for Anti Slop Content Engine (end-to-end hardened: runs from any cwd)."""
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


_engine_mod = _load("core.content_engine", "core/content_engine.py")
AntiSlopContentEngine = _engine_mod.AntiSlopContentEngine

import argparse
import json


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
        print("\n--- X/TWITTER THREAD ---")
        for i, tw in enumerate(pkg.x_thread_tweets):
            print(f"[{i+1}/{len(pkg.x_thread_tweets)}]\n{tw}\n")
        print("--- LINKEDIN POST ---")
        print(pkg.linkedin_post)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

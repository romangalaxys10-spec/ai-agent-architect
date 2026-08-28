"""CLI for Colab T4 GPU Agent — detect / setup / benchmark / run on free T4"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import pathlib


def _read(p: str) -> str:
    return pathlib.Path(p).read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Colab T4 GPU Agent — detect/setup/benchmark on free NVIDIA T4")
    parser.add_argument("--text", help="Input text to analyze (inline)")
    parser.add_argument("--file", help="Path to input file")
    parser.add_argument("--check", action="store_true", help="Detect Colab/T4/CUDA")
    parser.add_argument("--setup", action="store_true", help="Show/run setup plan")
    parser.add_argument("--dry-run", action="store_true", help="Dry-run setup (default for --setup)")
    parser.add_argument("--benchmark", action="store_true", help="Benchmark VRAM/TTFT (simulated locally)")
    parser.add_argument("--run", help="Prompt to run (requires Colab T4 for live inference)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    from core.colab_t4_engine import ColabT4Engine

    # Default if no flag: --check
    if not any([args.check, args.setup, args.benchmark, args.run]):
        args.check = True

    text = ""
    if args.file:
        text = _read(args.file)
    elif args.text:
        text = args.text
    elif args.run:
        text = args.run

    if args.setup:
        # --dry-run is default when --setup on non-Colab; explicit flag controls live
        dry = args.dry_run or not args.check  # if only --setup, dry-run
        # If user passes --setup --dry-run => dry; --setup alone => dry locally, live in Colab
        # Honor explicit --dry-run presence via parse count: use args.dry_run if set, else True locally
        # Simple: if --setup and no --json, dry_run = args.dry_run is False => check env
        import os as _os
        if not args.dry_run:
            # Heuristic: if not in Colab, keep dry-run even if flag not set
            try:
                import google.colab  # noqa
                dry = False
            except Exception:
                dry = True
                if "--dry-run" not in sys.argv:
                    pass  # keep dry for local safety
        analysis = ColabT4Engine.setup_plan(dry_run=dry)
    elif args.benchmark:
        analysis = ColabT4Engine.benchmark()
    elif args.run is not None:
        # Offline demo: treat as check + simulated run
        base = ColabT4Engine.check(text)
        # Attach run hint
        base.metrics["prompt"] = args.run[:120]
        base.next_steps.insert(0, f'Run prompt: "{args.run[:60]}" — live inference only in Colab T4 (this host simulated)')
        analysis = base
    else:
        analysis = ColabT4Engine.check(text)

    if args.json:
        import json as _json
        print(_json.dumps({"verdict": analysis.verdict, "score": analysis.score, "metrics": analysis.metrics, "findings": [{"severity": f.severity, "title": f.title, "detail": f.detail, "fix": f.fix} for f in analysis.findings], "next_steps": analysis.next_steps}, indent=2))
    else:
        print(ColabT4Engine.format_report(analysis))


if __name__ == "__main__":
    main()

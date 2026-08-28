"""CLI for Power & Battery Sentinel — Sleep/wake orchestration, battery health, thermal throttling, and charge-limit policies"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse
def _read(p):
    import pathlib
    return pathlib.Path(p).read_text(encoding="utf-8")
def main():
    parser=argparse.ArgumentParser(description="Power & Battery Sentinel — Sleep/wake orchestration, battery health, thermal throttling, and charge-limit policies")
    parser.add_argument("--text", help="Input text to analyze (inline)")
    parser.add_argument("--file", help="Path to input file")
    parser.add_argument("--os", choices=["linux","macos","windows","agnostic"], help="Override detected OS")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args=parser.parse_args()
    text=""
    if args.file:
        text=_read(args.file)
    elif args.text:
        text=args.text
    else:
        import sys as _sys
        if not _sys.stdin.isatty():
            text=_sys.stdin.read()
        if not text or not text.strip():
            parser.error("Provide --text or --file (or pipe via stdin)")
    from core.power_battery_engine import PowerBatteryEngine
    analysis=PowerBatteryEngine.analyze(text, os_hint=args.os)
    if args.json:
        import json as _json
        print(_json.dumps({"verdict": analysis.verdict, "score": analysis.score, "metrics": analysis.metrics, "findings": [{"severity": f.severity, "title": f.title, "detail": f.detail, "fix": f.fix} for f in analysis.findings], "next_steps": analysis.next_steps}, indent=2))
    else:
        print(PowerBatteryEngine.format_report(analysis))
if __name__=="__main__":
    main()

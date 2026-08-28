"""CLI for Spotlight & Search Pilot — Indexed search, intent disambiguation, quick-open ranking, and recent-items forensics"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse
def _read(p):
    import pathlib
    return pathlib.Path(p).read_text(encoding="utf-8")
def main():
    parser=argparse.ArgumentParser(description="Spotlight & Search Pilot — Indexed search, intent disambiguation, quick-open ranking, and recent-items forensics")
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
    from core.spotlight_search_engine import SpotlightSearchEngine
    analysis=SpotlightSearchEngine.analyze(text, os_hint=args.os)
    if args.json:
        import json as _json
        print(_json.dumps({"verdict": analysis.verdict, "score": analysis.score, "metrics": analysis.metrics, "findings": [{"severity": f.severity, "title": f.title, "detail": f.detail, "fix": f.fix} for f in analysis.findings], "next_steps": analysis.next_steps}, indent=2))
    else:
        print(SpotlightSearchEngine.format_report(analysis))
if __name__=="__main__":
    main()

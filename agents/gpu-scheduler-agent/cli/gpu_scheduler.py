"""CLI for GPU Scheduler — CUDA/MPS, VRAM bin-packing, and preemption for LLM"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse, pathlib
def _read(p):
    return pathlib.Path(p).read_text(encoding="utf-8")
def main():
    parser=argparse.ArgumentParser(description="GPU Scheduler — CUDA/MPS, VRAM bin-packing, and preemption for LLM")
    parser.add_argument("--text", help="Input text to analyze (inline)")
    parser.add_argument("--file", help="Path to input file")
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
    from core.gpu_scheduler_engine import GpuSchedulerEngine
    analysis=GpuSchedulerEngine.analyze(text)
    if args.json:
        import json as _json
        print(_json.dumps({"verdict": analysis.verdict, "score": analysis.score, "metrics": analysis.metrics, "findings": [{"severity": f.severity, "title": f.title, "detail": f.detail, "fix": f.fix} for f in analysis.findings], "next_steps": analysis.next_steps}, indent=2))
    else:
        print(GpuSchedulerEngine.format_report(analysis))
if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""narrate.py — batch TTS narration via Microsoft Edge neural voices (edge-tts).
Usage: python3 narrate.py --script narration.txt --outdir narr/ [--voice en-US-ChristopherNeural]
Script format: one narration line per file, lines ordered top-to-bottom (line_01.mp3 ...).
Blank lines and #comments are skipped."""
import argparse, os, subprocess, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--outdir", default="narr")
    ap.add_argument("--voice", default="en-US-ChristopherNeural")
    ap.add_argument("--rate", default="-8%")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    lines = [l.strip() for l in open(args.script)
             if l.strip() and not l.strip().startswith("#")]
    for i, line in enumerate(lines, 1):
        out = os.path.join(args.outdir, f"line_{i:02d}.mp3")
        if os.path.exists(out) and os.path.getsize(out) > 5000:
            print(out, "exists"); continue
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", args.voice,
                            f"--rate={args.rate}", "--text", line, "--write-media", out],
                           capture_output=True, text=True)
        ok = os.path.exists(out) and os.path.getsize(out) > 5000
        print(out, "ok" if ok else f"FAIL {r.stderr[-100:]}")

if __name__ == "__main__":
    main()

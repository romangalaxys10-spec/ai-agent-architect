#!/usr/bin/env python3
"""fetch_segments.py — download curated time windows from verified CC-BY videos.
Usage: python3 fetch_segments.py --manifest manifest.txt --out segs/ [--height 720]
Manifest line format:  name|videoId|HH:MM:SS|HH:MM:SS
Requires an ffmpeg binary on PATH (yt-dlp needs it for section cutting).
Tip: imageio_ffmpeg ships a static one:
  ln -sf $(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())') ~/bin/ffmpeg
"""
import argparse, subprocess, sys, os, concurrent.futures
from pathlib import Path

def fetch(name, vid, start, end, out, height):
    dst = Path(out) / f"{name}.mp4"
    if dst.exists() and dst.stat().st_size > 50000:
        return f"{name}: exists"
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "-q",
        "-f", f"bv*[height<={height}]+ba/b[height<={height}]/b", "-S", f"res:{height}",
        "--download-sections", f"*{start}-{end}", "--force-keyframes-at-cuts",
        "-o", str(dst), f"https://www.youtube.com/watch?v={vid}"],
        capture_output=True, text=True)
    ok = dst.exists() and dst.stat().st_size > 50000
    return f"{name}: {'ok' if ok else 'FAIL ' + (r.stderr or '')[-120:]}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="segs")
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    jobs = []
    for line in open(args.manifest):
        line = line.strip()
        if not line or line.startswith("#"): continue
        name, vid, start, end = line.split("|")
        jobs.append((name, vid, start, end))
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for res in ex.map(lambda j: fetch(*j, args.out, args.height), jobs):
            print(res)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""curate.py — find license-VERIFIED CC-BY YouTube videos for a theme.
Usage: python3 curate.py --query "aerial nature 4k" --out verified.txt [--max 30]
YouTube's CC search filter (sp=EiQIASgD) is unreliable: every candidate's license
metadata is individually verified. Only explicit CC-BY videos are kept."""
import argparse, subprocess, sys, urllib.parse, concurrent.futures

QUERIES_EXTRA = ["no copyright 4k", "free stock footage", "no copyright cinematic"]
def search_ids(q, exe):
    url = ("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q)
           + "&sp=EiQIASgD")
    r = subprocess.run([exe, "--flat-playlist", "--print", "%(id)s", url],
                       capture_output=True, text=True)
    return [x.strip() for x in r.stdout.splitlines() if len(x.strip()) == 11]

def verify(vid, exe):
    r = subprocess.run([exe, "--print", "%(license)s|%(duration)s|%(channel)s|%(title)s",
                        "--no-download", f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True)
    line = (r.stdout or "").strip().splitlines()[0] if (r.stdout or "").strip() else ""
    if "Creative Commons Attribution license" in line:
        return f"{vid} => {line}"
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--out", default="verified.txt")
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--yt-dlp", default=sys.executable + " -m yt_dlp")
    args = ap.parse_args()
    exe = args.yt_dlp if " " in args.yt_dlp else [args.yt_dlp]
    if isinstance(exe, str): exe = exe.split()
    ids = set()
    for q in [args.query] + [f"{args.query} {x}" for x in QUERIES_EXTRA]:
        ids.update(search_ids(q, exe))
        if len(ids) >= args.max: break
    ids = sorted(ids)[:args.max]
    print(f"candidates: {len(ids)} — verifying licenses in parallel...")
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for res in ex.map(lambda v: verify(v, exe), ids):
            if res:
                found.append(res); print("  CC-BY:", res)
    with open(args.out, "w") as f:
        f.write("\n".join(found))
    print(f"verified CC-BY: {len(found)} -> {args.out}")

if __name__ == "__main__":
    main()

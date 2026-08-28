#!/usr/bin/env python3
"""build_edit.py — pro master builder: uniform segments -> xfade chain ->
narration at scene starts -> ducked music bed -> title + attribution end card.
Output is universal H.264 yuv420p + faststart (plays on QuickTime/iPhone/web).
Usage:
  python3 build_edit.py --clips segs/ --narr narr/ --music music.mp3 \
      --title "EARTH AND SKY" --credits credits.txt --out final.mp4
  # optional: --order a1,a2,u1  (default: sorted filenames)
  # optional: --line-segments 0,2,8   (narration line N at segment N; default: every segment)
Clips must be 720p-friendly video files (webm/mp4/mkv all fine; auto-uniformized).
"""
import argparse, glob, os, re, subprocess, sys
import imageio_ffmpeg

def base(f):
    b = os.path.basename(f)
    while b.endswith('.mp4') or b.endswith('.webm') or b.endswith('.mkv'):
        b = b[:-4]
    return b

FF = imageio_ffmpeg.get_ffmpeg_exe()
F = 0.8  # crossfade seconds

def dur(f):
    err = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", err)
    return (int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))) if m else 10.0

def uniform(src, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 50000: return
    vf = ("scale=1280:720:force_original_aspect_ratio=decrease,"
          "pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p")
    subprocess.run([FF,"-y","-i",src,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
                    "-vf",vf,"-map","0:v","-map","1:a","-shortest",
                    "-c:v","libx264","-preset","fast","-crf","20",
                    "-c:a","aac","-ar","48000",dst],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clips", required=True)
    ap.add_argument("--narr", required=True)
    ap.add_argument("--music", default=None)
    ap.add_argument("--title", default="A VISUAL JOURNEY")
    ap.add_argument("--title-sub", default="")
    ap.add_argument("--credits", default=None, help="text file shown on end card")
    ap.add_argument("--order", default=None, help="comma-separated segment names")
    ap.add_argument("--line-segments", default=None, help="csv: narration line i+1 at segment i")
    ap.add_argument("--out", default="master.mp4")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.clips, "*.mp4")) +
                   glob.glob(os.path.join(args.clips, "*.webm")) +
                   glob.glob(os.path.join(args.clips, "*.mkv")))
    if args.order:
        names = args.order.split(",")
        files = sorted(files, key=lambda f: names.index(base(f))
                       if os.path.splitext(os.path.basename(f))[0] in names else 999)
    normdir = os.path.join(args.clips, "_normalized")
    os.makedirs(normdir, exist_ok=True)
    procs = []
    for f in files:
        dst = os.path.join(normdir, os.path.splitext(os.path.basename(f))[0] + ".mp4")
        uniform(f, dst)
    segs = [f for f in sorted(glob.glob(os.path.join(normdir, "*.mp4")))
            if not os.path.basename(f).startswith("_")]
    if args.order:
        names = args.order.split(",")
        segs = [f for f in segs if base(f) in names] if args.order else segs
    segs = sorted(segs, key=lambda f: names.index(base(f)))
    n = len(segs)
    if n < 2: print("need >= 2 clips"); sys.exit(1)

    # end card
    END = os.path.join(normdir, "_endcard.mp4")
    vf = (f"fade=t=in:st=0:d=1.2,"
          f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:text='{args.title}':"
          f"fontsize=58:fontcolor=white:x=(w-text_w)/2:y=h*0.36")
    if args.credits and os.path.exists(args.credits):
        vf += (",drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile=" +
               os.path.abspath(args.credits) +
               ":fontsize=20:fontcolor=0xBEBEBE:line_spacing=8:x=(w-text_w)/2:y=h*0.58")
    subprocess.run([FF,"-y","-f","lavfi","-i","color=black:size=1280x720:rate=30:duration=10",
                    "-f","lavfi","-i","anullsrc=r=48000:cl=stereo:duration=10",
                    "-vf",vf,"-map","0:v","-map","1:a","-c:v","libx264","-preset","fast","-crf","20",
                    "-pix_fmt","yuv420p","-c:a","aac","-shortest",END], capture_output=True, text=True)
    segs = segs + [END]

    durs = [dur(s) for s in segs]
    offs, t = [], durs[0]
    for i in range(1, len(segs)):
        offs.append(t - F); t = t + durs[i] - F
    total = t
    starts = [0.0] + [o + F for o in offs]

    fp = [f"[0:v]fade=t=in:st=0:d=0.8,drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:"
          f"text='{args.title}':fontsize=68:fontcolor=white:borderw=2:bordercolor=black@0.6:"
          f"x=(w-text_w)/2:y=h*0.12:enable='lt(t,5)'[v0t]"]
    cur_v, cur_a = "v0t", "0:a"
    for i in range(1, len(segs)):
        fp.append(f"[{cur_v}][{i}:v]xfade=transition=fade:duration={F}:offset={offs[i-1]:.3f}[vx{i}]")
        fp.append(f"[{cur_a}][{i}:a]acrossfade=d={F}:c1=tri:c2=tri[ax{i}]")
        cur_v, cur_a = f"vx{i}", f"ax{i}"
    fs = max(0.0, total - 1.6)
    fp.append(f"[{cur_v}]fade=t=out:st={fs:.2f}:d=1.6[vf]")

    narr_files = sorted(glob.glob(os.path.join(args.narr, "line_*.mp3")))
    use = []
    if narr_files:
        seg_idx = ([int(x) for x in args.line_segments.split(",")]
                   if args.line_segments else list(range(len(narr_files))))
        use = [(si, i) for i, si in enumerate(seg_idx) if si < len(segs)]
    # silent base so amix always has enough inputs
    fp.append(f"[{cur_a}]volume=0.15[amb]")
    streams = "[amb]"
    ai = len(segs) + (1 if args.music else 0)
    fp.append(f"[{len(segs)}:a]atrim=0:{total:.2f},volume=0.22,afade=t=out:st={fs:.2f}:d=2.5[music]") if args.music else None
    if args.music: streams = "[music]" + streams
    n_in = (2 if args.music else 1) + len(use)
    input_files = segs + ([args.music] if args.music else []) + \
                  [narr_files[j] for _, j in use]
    for k, (si, j) in enumerate(use):
        idx = ai + k
        fp.append(f"[{idx}:a]adelay={round(starts[si]*1000+900)}:all=1,"
                  f"apad=whole_dur={total:.2f}[vo{k}]")
        streams += f"[vo{k}]"
    fp.append(f"{streams}amix=inputs={n_in}:normalize=0:duration=longest[mx]")
    fp.append(f"[mx]atrim=0:{total:.2f},alimiter=limit=0.95[af]")

    cmd = [FF, "-y"]
    for s in segs: cmd += ["-i", s]
    if args.music: cmd += ["-stream_loop", "-1", "-i", args.music]
    for _, j in use: cmd += ["-i", narr_files[j]]
    cmd += ["-filter_complex", ";".join(fp), "-map", "[vf]", "-map", "[af]",
            "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-c:a", "aac", "-ar", "48000", "-b:a", "160k",
            "-movflags", "+faststart", args.out]
    open("/tmp/fc_debug.txt","w").write(";".join(fp))
    open("/tmp/cmd_debug.txt","w").write(" ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"MASTER OK: {args.out} {round(os.path.getsize(args.out)/1e6,1)}MB | "
              f"{round(total,1)}s | {len(segs)-1} scenes")
    else:
        print("FAIL:", r.stderr[-600:]); sys.exit(1)

if __name__ == "__main__":
    main()

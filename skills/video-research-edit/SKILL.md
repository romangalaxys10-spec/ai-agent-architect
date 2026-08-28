---
name: video-research-edit
description: Curate license-verified YouTube footage (CC-BY only), download segments, build a narrated professional edit (crossfades, music bed, title/credits cards), and publish to YouTube via headless Firefox with injected session cookies. 100% legal remix pipeline — every clip's license is individually verified before use.
version: 1.1.0
author: AI Agent Architect
---

# Video Research & Edit — Legal Remix Pipeline

> "Every clip verified. Every edit smooth. Every credit given."

Turns a theme into a published, professionally-edited video using **only** properly-licensed
(Creative Commons Attribution) footage — plus your own generated content.

## 🎯 Activation Triggers

- "curate a video from YouTube CC content"
- "remix free footage into a video"
- "build a 5 minute video from licensed clips"
- "upload this video to my YouTube channel"

## 🧯 Legal Rules (non-negotiable)

1. **Verify each video's license field individually** — YouTube's CC search filter
   (`sp=EiQIASgD`) lies; ~80% of its results are actually standard copyright (license `NA`).
   Only accept `license == "Creative Commons Attribution license (reuse allowed)"`.
2. **Never use videos whose license is `NA`/missing**, even if titled "no copyright".
3. **Attribution is a license condition**: publish `ATTRIBUTIONS.txt` content in the video
   description and/or credits card. No attribution = infringement.
4. Only upload to channels/accounts you own. The headless uploader is for **your own**
   channel, using **your own** logged-in session cookies.

## 🔧 Requirements

- Python 3.10+, `yt-dlp`, `edge-tts` (pip)
- `ffmpeg` on PATH (or `imageio_ffmpeg.get_ffmpeg_exe()`)
- Firefox + `marionette_driver` for the upload stage; user logged into YouTube in Firefox
- macOS note: launching Firefox from agent shells trips a sandbox bug (kernel SIGKILLs
  content processes on macOS 27 beta). Launch via LaunchServices (`open -na`) — works.

## 📋 Workflow

### 1. Curate (license-verified)
```bash
python3 scripts/curate.py --query "aerial nature 4k" --out candidates/
# → candidates/verified.txt  (only explicit CC-BY videos, with duration+channel)
```
Runs CC-filtered YouTube searches across several query variants, then batch-verifies each
candidate's actual license metadata in parallel. Expect ~10% verification pass rate.

### 2. Fetch segments
```bash
python3 scripts/fetch_segments.py --manifest manifest.txt --out segs/
# manifest lines:  name|videoId|HH:MM:SS|HH:MM:SS
```
Downloads only the listed time windows at ≤720p (keyframe-accurate cuts). Put the static
`ffmpeg` binary on PATH (`imageio_ffmpeg` ships one) or yt-dlp section cutting fails.

### 3. Narrate
```bash
python3 scripts/narrate.py --script narration.txt --outdir narr/
# one line per file; edge-tts Microsoft neural voices (no API key)
```

### 4. Build the master
```bash
python3 scripts/build_edit.py --clips segs/ --narr narr/ --music music.mp3 \
    --title "MY FILM" --out final.mp4
```
Uniformizes every segment (720p/30fps/yuv420p, silent), chains 0.8s video crossfades +
audio blends, places narration lines at scene starts, ducks a music bed, adds title +
attribution end card, outputs universal H.264 **yuv420p** (Apple players reject yuv444p).

### 5. Publish (headless, zero browser interference)
```bash
python3 scripts/yt_upload_headless.py --video final.mp4 \
    --title-file title.txt --description-file description.txt --public
```
Harvests session cookies from the user's running Firefox (Marionette, port 2828), spawns a
dedicated **headless** Firefox instance (`open -na` + fresh profile + port 2829), injects
cookies, drives YouTube Studio: attach → title/description → not-made-for-kids → public →
publish. Prints the public watch URL.

## ⚠️ Gotchas (learned the hard way)

- `open -a` ignores `--args` when the app is already running — use `open -na`.
- Marionette holds one client connection: stop other automation before connecting.
- Marionette `el.click()` = real event sequence; JS `.click()` does not fire mousedown
  (arco/YouTube menus won't close on JS clicks).
- Hidden `<input type=file>`: unhide via `style.cssText` before `send_keys`.
- Marionette `m.close()` can close the browser window — avoid it entirely.
- Studio cookies are domain-scoped: harvest while a youtube.com tab is current
  (Marionette returns cookies for the active page's domain).
- Always export `-pix_fmt yuv420p` + `-movflags +faststart`.

## 📄 Attribution Example

See `ATTRIBUTIONS.example.txt` — creator, title, link, license per clip. Publish this in
the description; CC-BY makes it a license condition, not a courtesy.

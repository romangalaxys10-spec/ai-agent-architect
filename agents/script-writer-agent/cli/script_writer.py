"""CLI for the Script Writer Agent — Writes video scripts: 5-second hook, beat structure, retention tactics, cutdowns"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _pick(inline, path):
    if path:
        return _read(path)
    return inline or ""


def main():
    parser = argparse.ArgumentParser(description='Script Writer Agent — video script + retention beats + cutdowns')
    parser.add_argument('--topic', required=True, help='Video topic')
    parser.add_argument('--duration', type=int, default=480, help='Duration in seconds')
    parser.add_argument('--style', default='educational', choices=['educational', 'entertaining', 'documentary', 'promotional'], help='Script style')
    parser.add_argument('--platform', default='youtube', choices=['youtube', 'tiktok', 'shorts', 'linkedin'], help='Primary platform')
    args = parser.parse_args()

    from core.script_writer_engine import ScriptWriterEngine
    script = ScriptWriterEngine.write(args.topic, duration_s=args.duration, style=args.style, platform=args.platform)
    print(ScriptWriterEngine.format_script(script))


if __name__ == "__main__":
    main()

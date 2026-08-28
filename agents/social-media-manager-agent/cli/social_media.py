"""CLI for the Social Media Manager Agent — Generates post variants, hashtag sets, thread structures, response templates"""
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
    parser = argparse.ArgumentParser(description='Social Media Manager Agent — post variants + hashtags + reply kit')
    parser.add_argument('--topic', required=True, help='Post topic or key message')
    parser.add_argument('--platform', default='x', choices=['x', 'linkedin', 'instagram', 'bluesky', 'mastodon'], help='Platform')
    parser.add_argument('--voice', default='technical, direct, no-hype', help='Brand voice descriptors')
    args = parser.parse_args()

    from core.social_media_engine import SocialMediaManagerEngine
    pack = SocialMediaManagerEngine.generate(args.topic, args.platform, args.voice)
    print(SocialMediaManagerEngine.format_pack(pack))


if __name__ == "__main__":
    main()

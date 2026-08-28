"""CLI for the SEO Content Strategist Agent — Designs topic clusters, search intent, outlines, and internal link plans"""
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
    parser = argparse.ArgumentParser(description='SEO Content Strategist Agent — topic cluster + outline + link plan')
    parser.add_argument('--keyword', required=True, help='Head keyword')
    parser.add_argument('--audience', default='technical decision makers', help='Target audience')
    parser.add_argument('--intent', default='auto', choices=['auto', 'informational', 'commercial', 'transactional', 'navigational'], help='Search intent')
    args = parser.parse_args()

    from core.seo_content_engine import SEOContentStrategistEngine
    strategy = SEOContentStrategistEngine.strategy(args.keyword, args.audience, args.intent)
    print(SEOContentStrategistEngine.format_strategy(strategy))


if __name__ == "__main__":
    main()

"""CLI for the Doc Scribe Agent — Reverse-engineers living documentation from source: API refs, examples, README blocks"""
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
    parser = argparse.ArgumentParser(description='Doc Scribe Agent — documentation generation from Python source')
    parser.add_argument('--file', help='Path to the Python source file')
    parser.add_argument('--source', help='Python source code inline')
    parser.add_argument('--style', default='markdown', choices=['markdown', 'rst'], help='Output doc style')
    args = parser.parse_args()

    from core.doc_scribe_engine import DocScribeEngine
    source = _pick(args.source, args.file)
    if not source.strip():
        raise SystemExit("Provide --source or --file")
    pack = DocScribeEngine.document(source, style=args.style)
    print(DocScribeEngine.format_docs(pack))


if __name__ == "__main__":
    main()

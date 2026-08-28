"""CLI for the Copy Editor Agent — Edits for clarity: passive voice, filler, sentence length, jargon, readability"""
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
    parser = argparse.ArgumentParser(description='Copy Editor Agent — clarity editing + readability scoring')
    parser.add_argument('--text', help='Text to edit (inline)')
    parser.add_argument('--file', help='Path to a text file')
    args = parser.parse_args()

    from core.copy_editor_engine import CopyEditorEngine
    text = _pick(args.text, args.file)
    if not text.strip():
        raise SystemExit("Provide --text or --file")
    report = CopyEditorEngine.edit(text)
    print(CopyEditorEngine.format_report(report))


if __name__ == "__main__":
    main()

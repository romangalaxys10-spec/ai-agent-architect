"""CLI for the Resume Screener Agent — Scores resume-job fit with evidence per skill, plus bias-safe language enforcement"""
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
    parser = argparse.ArgumentParser(description='Resume Screener Agent — evidence-based resume-job fit scoring')
    parser.add_argument('--resume', help='Resume text (inline)')
    parser.add_argument('--resume-file', help='Path to a resume file')
    parser.add_argument('--job', help='Job requirements text (inline)')
    parser.add_argument('--job-file', help='Path to a job description file')
    args = parser.parse_args()

    from core.resume_screener_engine import ResumeScreenerEngine
    resume = args.resume if args.resume else (_read(args.resume_file) if args.resume_file else "")
    job = args.job if args.job else (_read(args.job_file) if args.job_file else "")
    if not resume.strip() or not job.strip():
        raise SystemExit("Provide --resume/--resume-file and --job/--job-file")
    result = ResumeScreenerEngine.screen(resume, job)
    print(ResumeScreenerEngine.format_result(result))


if __name__ == "__main__":
    main()

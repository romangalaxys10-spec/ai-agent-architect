"""
Commit Crafter Engine.
Parses unified diffs into conventional-commit messages, Keep-a-Changelog
entries, and semver bump recommendations.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class CommitPack:
    commit_type: str
    scope: str
    subject: str
    body: List[str]
    breaking: bool
    semver_bump: str
    changelog_entry: str
    footer: str = ""

PATH_TYPE_HINTS = [
    (r"\btest", "test", "tests"),
    (r"\bdocs?/|\.(md|rst)$|README|CHANGELOG", "docs", "documentation"),
    (r"\.github/|Dockerfile|Makefile|\.toml$|\.cfg$|\.ya?ml$", "build", "build/tooling"),
    (r"\.(css|scss|less)$", "style", "styles"),
    (r"^(refactor|refactoring)/|\brefactor\b", "refactor", "refactorings"),
]

class CommitCrafterEngine:
    """Commits are history's interface — craft them like a public API."""

    @classmethod
    def craft(cls, diff_text: str, breaking_hint: bool = False) -> CommitPack:
        files = re.findall(r"^diff --git a/(\S+) b/(\S+)", diff_text, re.M)
        paths = [b for _, b in files] or re.findall(r"^\+\+\+ b/(\S+)", diff_text, re.M)

        added = len(re.findall(r"^\+(?!\+)", diff_text, re.M))
        removed = len(re.findall(r"^-(?!-)", diff_text, re.M))

        # figure out commit type
        commit_type, scope = "chore", ""
        if paths:
            top = paths[0].split("/")[0]
            scope = top if top and not top.startswith(".") and "." not in top else ""
        for pattern, t, _ in PATH_TYPE_HINTS:
            if any(re.search(pattern, p) for p in paths):
                commit_type = t
                break

        new_tests = any(re.search(r"\btest", p) for p in paths)
        src_paths = [p for p in paths if not re.search(r"\btest|\.md$|docs?/", p)]
        if src_paths and new_tests and commit_type not in ("fix",):
            commit_type = "feat" if added > removed * 1.5 else commit_type

        # detect intent from hunk contents
        lower = diff_text.lower()
        is_fix = bool(re.search(r"(bug|fix(?:ed|es)?|resolv|clos\w+ #\d+|patch)", lower))
        if is_fix and commit_type not in ("feat",):
            commit_type = "fix"
        new_feature = bool(re.search(r"(def |function |export (default )?(async )?function|class |component|endpoint|route)", diff_text)) and added > removed
        if new_feature and commit_type in ("chore",):
            commit_type = "feat"

        breaking = breaking_hint or bool(
            re.search(r"(BREAKING[ :]CHANGE|!!:|\bremove[sd]? (public )?api\b|\bdeprecat\b)", diff_text, re.I))

        # subject: name the primary path intent
        primary = paths[0] if paths else "changes"
        primary_name = re.sub(r"\.[a-z]+$", "", primary.split("/")[-1]).replace("_", " ").replace("-", " ")
        if not primary_name or primary_name == "":
            primary_name = "workspace"
        subject_map = {
            "feat": f"add {primary_name} capability",
            "fix": f"correct {primary_name} behavior",
            "test": f"cover {primary_name} with tests",
            "docs": f"document {primary_name}",
            "build": f"update build/tooling for {primary_name}",
            "style": f"format {primary_name}",
            "refactor": f"restructure {primary_name}",
            "chore": f"maintain {primary_name}",
        }
        subject = subject_map[commit_type]

        body = [
            f"Touched {len(paths)} file(s); +{added}/-{removed} lines.",
        ]
        if src_paths[:5]:
            body.append("Primary source changes: " + ", ".join(src_paths[:5]))
        if new_tests:
            body.append("Tests added/updated alongside source changes.")
        if breaking:
            body.append("BREAKING CHANGE: API surface or behavior changed; consult the migration notes.")

        bump = "major" if breaking else ("minor" if commit_type == "feat" else "patch")

        changelog_map = {
            "feat": "Added", "fix": "Fixed", "test": "Changed", "docs": "Changed",
            "build": "Changed", "style": "Changed", "refactor": "Changed", "chore": "Changed",
        }
        section = changelog_map[commit_type]
        entry = f"- {subject.capitalize()}" + (f" ({scope})" if scope else "") + \
                (" (**BREAKING**)" if breaking else "")

        footer = "Refs: <issue#>\nReviewed-by: <reviewer>" if not breaking else \
                 "Refs: <issue#>\nBREAKING CHANGE: <describe migration>\nReviewed-by: <reviewer>"

        return CommitPack(commit_type=commit_type, scope=scope, subject=subject, body=body,
                          breaking=breaking, semver_bump=bump, changelog_entry=entry, footer=footer)

    @staticmethod
    def format_pack(p: CommitPack) -> str:
        header = f"{p.commit_type}" + (f"({p.scope})" if p.scope else "") + \
                 ("!" if p.breaking else "") + f": {p.subject}"
        out = ["=" * 62, "COMMIT CRAFTER AGENT — COMMIT PACK", "=" * 62,
               "Suggested commit:", "  " + header]
        out += ["  " + ("  " + b) for b in p.body]
        out += ["  " + l for l in ("  " + p.footer).splitlines()]
        out += ["-" * 62,
               f"Semver bump: {p.semver_bump}",
               f"Changelog section: see below", "",
               "Changelog entry:",
               "  " + p.changelog_entry,
               "-" * 62,
               "Rule: if the diff does two unrelated things, split the commit — history is an API.",
               "=" * 62]
        return "\n".join(out)

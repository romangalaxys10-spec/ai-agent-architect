"""
Copy Editor Agent Engine.
Edits for clarity: passive voice, filler, sentence length, jargon,
readability (Flesch), with line-level suggestions and a rewrite.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Edit:
    line_no: int
    kind: str
    excerpt: str
    suggestion: str

@dataclass
class EditReport:
    word_count: int
    sentence_count: int
    avg_sentence_len: float
    flesch: float
    grade_level: float
    passive_count: int
    filler_count: int
    jargon_hits: List[str] = field(default_factory=list)
    edits: List[Edit] = field(default_factory=list)
    rewrite: str = ""
    verdict: str = ""

FILLERS = ["very", "really", "quite", "just", "basically", "actually", "literally",
           "simply", "totally", "definitely", "certainly", "in order to", "at this point in time",
           "it should be noted that", "needless to say", "for all intents and purposes"]

JARGON = ["synergy", "leverage (as a verb)", "paradigm", "holistic", "disrupt", "circle back",
          "bandwidth", "low-hanging fruit", "move the needle", "best-in-class", "world-class",
          "cutting-edge", "game-changer", "value-add", "ideate", "operationalize"]

PASSIVE_RE = re.compile(r"\b(?:is|are|was|were|be|been|being)\s+(\w+(?:ed|en))\b", re.I)
IRREGULAR_PASSIVES = {"is known", "are known", "was made", "were made", "is done", "are done",
                      "is seen", "was held", "is taken", "was given", "is written", "was built"}

def _syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee", "ye")):
        n -= 1
    return max(1, n)

class CopyEditorEngine:
    """Clarity is politeness paid to the reader in advance."""

    @classmethod
    def edit(cls, text: str) -> EditReport:
        lines = text.splitlines()
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        words = re.findall(r"[A-Za-z']+", text)
        n_words = len(words)
        n_sent = max(1, len(sentences))
        n_syll = sum(_syllables(w) for w in words)

        flesch = round(206.835 - 1.015 * (n_words / n_sent) - 84.6 * (n_syll / max(1, n_words)), 1)
        grade = round(0.39 * (n_words / n_sent) + 11.8 * (n_syll / max(1, n_words)) - 15.59, 1)

        edits: List[Edit] = []
        low_blob = text.lower()

        # passive voice per line
        passive_total = 0
        for i, line in enumerate(lines, 1):
            if not line.strip():
                continue
            for m in PASSIVE_RE.finditer(line):
                passive_total += 1
                edits.append(Edit(i, "passive", m.group(0),
                                  "name the actor: 'X did Y' instead of 'Y was done'"))
                break
            if any(p in line.lower() for p in IRREGULAR_PASSIVES):
                passive_total += 1

        # fillers
        filler_total = 0
        for i, line in enumerate(lines, 1):
            for f in FILLERS:
                if re.search(rf"\b{re.escape(f)}\b", line, re.I):
                    filler_total += 1
                    if len([e for e in edits if e.kind == "filler" and e.line_no == i]) < 2:
                        edits.append(Edit(i, "filler", f, f"delete '{f}' — the sentence is stronger without it"))

        # jargon
        jargon_hits = []
        for j in JARGON:
            core = j.split(" (")[0]
            if re.search(rf"\b{re.escape(core)}\b", low_blob):
                jargon_hits.append(j)

        # long sentences
        for s in sentences:
            wc = len(s.split())
            if wc > 32:
                edits.append(Edit(0, "long-sentence", s[:60] + "...",
                                  f"{wc} words — split at the conjunction or delete a clause"))

        # very + adjective
        for i, line in enumerate(lines, 1):
            m = re.search(r"\b(very|really|extremely)\s+(\w+)", line)
            if m:
                edits.append(Edit(i, "intensifier", m.group(0),
                                  f"replace with a stronger single word ('{m.group(2)}' has one)"))

        # rewrite: strip fillers, compress
        rewrite = text
        for f in FILLERS:
            rewrite = re.sub(rf"\b{re.escape(f)}\b\s*", "", rewrite, flags=re.I)
        rewrite = re.sub(r"\bin order to\b", "to", rewrite, flags=re.I)
        rewrite = re.sub(r"\s{2,}", " ", rewrite)
        # shorten common bureaucratic phrases
        rewrite = re.sub(r"\bat this point in time\b", "now", rewrite, flags=re.I)
        rewrite = re.sub(r"\bdue to the fact that\b", "because", rewrite, flags=re.I)
        rewrite = re.sub(r"\bin the event that\b", "if", rewrite, flags=re.I)
        rewrite = re.sub(r"\bmake use of\b", "use", rewrite, flags=re.I)

        avg_len = round(n_words / n_sent, 1)
        issues = passive_total + filler_total + len(jargon_hits) + len([e for e in edits if e.kind == "long-sentence"])
        verdict = (f"{n_words} words | avg sentence {avg_len} | Flesch {flesch} "
                   f"(grade {grade}) | passive {passive_total} | filler {filler_total} | {issues} total issues")
        return EditReport(n_words, n_sent, avg_len, flesch, grade, passive_total,
                          filler_total, jargon_hits, edits, rewrite.strip(), verdict)

    @staticmethod
    def format_report(r: EditReport) -> str:
        out = ["=" * 62, "COPY EDITOR AGENT — REPORT", "=" * 62, r.verdict, "-" * 62,
               "Readability: " + ("easy" if r.flesch >= 60 else "moderate" if r.flesch >= 40 else "difficult") +
               f" (Flesch {r.flesch}, grade {r.grade_level})"]
        if r.jargon_hits:
            out.append("Jargon found: " + ", ".join(r.jargon_hits))
        out += ["-" * 62, "Line-level edits:"]
        if r.edits:
            shown = {}
            for e in r.edits:
                key = (e.kind, e.line_no)
                if shown.get(key, 0) >= 2:
                    continue
                shown[key] = shown.get(key, 0) + 1
                loc = f"L{e.line_no}" if e.line_no else "sentence"
                out.append(f"  [{e.kind:14}] {loc}: \"{e.excerpt[:52]}\"")
                out.append(f"        -> {e.suggestion[:80]}")
        else:
            out.append("  clean — no mechanical issues found")
        out += ["-" * 62, "Rewrite (filler-stripped, phrases compressed):"]
        out += ["  " + ln for ln in r.rewrite.splitlines()[:25]]
        out += ["-" * 62,
                "Targets for professional prose: avg sentence 15-20 words, passive < 10%, zero filler.",
                "=" * 62]
        return "\n".join(out)

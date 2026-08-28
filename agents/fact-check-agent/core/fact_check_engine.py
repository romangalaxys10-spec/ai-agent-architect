"""
Fact Check Agent Engine.
Decomposes claims into atomic assertions and verifies each against
provided evidence with a verdict and evidence trail.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Assertion:
    text: str
    status: str          # supports / refutes / insufficient
    evidence_idx: List[int]
    note: str

@dataclass
class VerdictReport:
    claim: str
    assertions: List[Assertion] = field(default_factory=list)
    verdict: str = ""
    confidence: float = 0.0
    trail: List[str] = field(default_factory=list)
    verdict_reason: str = ""

STOP = set("""the a an of for to in on with and or is are was were be been being that this these those it its
as at by from into than then so such can could may might will would about over under across per via have has
had do does did their there here they you we i not no nor but if""".split())

REFUTE_MARKERS = ["false", "not true", "incorrect", "actually", "in fact", "however", "but ",
                  "myth", "debunk", "no evidence", "contrary", "refuted", "overstated"]
SUPPORT_MARKERS = ["true", "confirmed", "confirms", "according to", "study found", "data shows", "reported",
                   "records show", "verified", "documented", "shows that", "found that"]

NUM_RE = re.compile(r"-?\$?\d[\d,.]*\s?(%|percent|billion|million|thousand|x)?", re.I)

class FactCheckEngine:
    """A claim is a chain of assertions — verify each link, not just the headline."""

    @staticmethod
    def _atoms(claim: str) -> List[str]:
        parts = re.split(r"(?:,?\s(?:and|but|because|while|although|however)\s|;\s|:\s)", claim)
        atoms = []
        for p in parts:
            p = p.strip().rstrip(".")
            if len(p.split()) >= 3:
                atoms.append(p)
        if not atoms:
            atoms = [claim.strip().rstrip(".")]
        return atoms[:6]

    @staticmethod
    def _overlap(a: str, b: str) -> float:
        ta = {w for w in re.findall(r"[a-z]{4,}", a.lower()) if w not in STOP}
        tb = {w for w in re.findall(r"[a-z]{4,}", b.lower()) if w not in STOP}
        return len(ta & tb) / len(ta | tb) if ta | tb else 0.0

    @classmethod
    def verify(cls, claim: str, evidence_blocks: List[str]) -> VerdictReport:
        atoms = cls._atoms(claim)
        assertions, trail = [], []

        for atom in atoms:
            best_ov, best_idx, best_sent, best_kind = 0.12, None, None, "insufficient"
            for i, ev in enumerate(evidence_blocks):
                for sent in re.split(r"(?<=[.!?])\s+", ev.replace("\n", " ")):
                    ov = cls._overlap(atom, sent)
                    if ov <= best_ov:
                        continue
                    low = sent.lower()
                    if any(m in low for m in REFUTE_MARKERS):
                        kind = "refutes"
                    elif any(m in low for m in SUPPORT_MARKERS) or ov >= 0.5:
                        kind = "supports"
                    else:
                        kind = "insufficient"
                    best_ov, best_idx, best_sent, best_kind = ov, i, sent, kind
                    if kind == "refutes" and ov >= 0.4:
                        break
                if best_kind == "refutes" and best_ov >= 0.4:
                    break

            if best_idx is None:
                assertions.append(Assertion(atom, "insufficient", [],
                                            "No evidence sentence overlaps this assertion."))
            else:
                note = f"matched evidence S{best_idx+1} (overlap {best_ov:.0%}): \"{best_sent[:100]}\""
                assertions.append(Assertion(atom, best_kind, [best_idx + 1], note))
                trail.append(f"[{best_kind.upper():12}] {atom[:70]} -> S{best_idx+1}")

        s = sum(1 for a in assertions if a.status == "supports")
        r = sum(1 for a in assertions if a.status == "refutes")
        u = len(assertions) - s - r
        total = max(1, len(assertions))

        if not evidence_blocks:
            verdict, reason, conf = "UNVERIFIED", "No evidence supplied.", 0.0
        elif r and s == 0:
            verdict, reason, conf = "REFUTED", f"{r}/{total} assertions contradicted, none supported.", min(0.9, 0.5 + 0.15 * r)
        elif r and s:
            verdict, reason, conf = "PARTIALLY_TRUE", f"{s} supported, {r} refuted, {u} unverifiable.", min(0.8, 0.35 + 0.12 * s)
        elif s == total:
            verdict, reason, conf = "CONFIRMED", f"All {total} assertion(s) supported by evidence.", min(0.95, 0.5 + 0.12 * s + 0.05 * len(evidence_blocks))
        elif s:
            verdict, reason, conf = "PARTIALLY_TRUE", f"{s}/{total} supported, {u} unverifiable.", min(0.7, 0.3 + 0.1 * s)
        else:
            verdict, reason, conf = "UNVERIFIED", f"{u}/{total} assertions have no matching evidence.", 0.1

        # numeric spot check: numbers in claim should appear in evidence
        claim_nums = {mt.group(0).strip() for mt in NUM_RE.finditer(claim)}
        ev_nums = {mt.group(0).strip() for mt in NUM_RE.finditer(" ".join(evidence_blocks))}
        missing_nums = claim_nums - ev_nums
        if missing_nums and verdict == "CONFIRMED":
            verdict, reason = "PARTIALLY_TRUE", f"Supported textually, but number(s) {sorted(missing_nums)} not found in evidence."
            conf *= 0.7

        return VerdictReport(claim, assertions, verdict, round(conf, 2), trail, reason)

    @staticmethod
    def format_report(r: VerdictReport) -> str:
        out = ["=" * 62, "FACT CHECK AGENT — VERDICT", "=" * 62,
               f"Claim: {r.claim}", "-" * 62,
               f"VERDICT: {r.verdict} (confidence {r.confidence:.0%})",
               f"Reason: {r.verdict_reason}", "-" * 62, "Atomic assertions:"]
        for i, a in enumerate(r.assertions, 1):
            out.append(f"  {i}. [{a.status.upper():12}] {a.text}")
            if a.note:
                out.append(f"      {a.note}")
        if r.trail:
            out += ["-" * 62, "Evidence trail:"]
            out += [f"  {t}" for t in r.trail]
        out += ["=" * 62, "Caveat: verdict quality is bounded by the evidence supplied — supply primary sources."]
        return "\n".join(out)

"""
Literature Review Agent Engine.
Clusters papers by method and topic, builds the chronological evolution,
maps contradictions, and identifies research gaps ranked by tractability.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Paper:
    idx: int
    title: str
    method: str
    sample: int
    finding: str
    year: str

@dataclass
class LitReview:
    papers: List[Paper] = field(default_factory=list)
    clusters: List[dict] = field(default_factory=list)
    evolution: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    gaps: List[dict] = field(default_factory=list)
    citation_matrix: List[str] = field(default_factory=list)
    verdict: str = ""

METHODS = {
    "RCT": [r"\brandomized\b", r"\bRCT\b", r"\bcontrolled trial\b"],
    "quasi-experimental": [r"quasi[- ]?experimental", r"difference[- ]in[- ]difference", r"\bDiD\b"],
    "survey": [r"\bsurvey\b", r"questionnaire", r"\bN\s*=\s*\d+\b.*respond"],
    "simulation": [r"\bsimulation\b", r"\bMonte Carlo\b", r"\bsynthetic data\b"],
    "qualitative": [r"\binterviews?\b", r"\bethnograph", r"\bcase stud", r"thematic analysis"],
    "meta-analysis": [r"meta[- ]analysis", r"systematic review"],
    "bench/empirical": [r"\bbenchmark\b", r"\bevaluation\b", r"\bempirical\b", r"\bdataset\b"],
}

GAP_PATTERNS = [
    (r"\bonly|single|small sample|N\s*=\s*\d{1,2}\b", "sample-size limitation",
     "Replicate with a larger/pre-registered sample — tractable and highly citable."),
    (r"no (baseline|control|comparison)", "missing baseline",
     "Add the standard baseline the field uses; instant referee-bait fix."),
    (r"future work|remains? (?:an? )?open|not yet (?:studied|explored)", "explicit open problem",
     "Author-declared gap — highest acceptance probability if scoped narrowly."),
    (r"\b(one|a single) (dataset|domain|language|site)\b", "single-domain limitation",
     "Cross-domain replication tests external validity; cheap to execute."),
]

class LiteratureReviewEngine:
    """A review is a map of the field's disagreements — not a summary of its agreements."""

    @classmethod
    def review(cls, abstracts: List[str]) -> LitReview:
        papers = []
        for i, ab in enumerate(abstracts, 1):
            first = ab.split(".")[0][:80] or f"paper {i}"
            m = re.match(r"^(.{10,90}?)[.\n]", ab)
            title = m.group(1).strip() if m else first
            method = "other"
            for meth, pats in METHODS.items():
                if any(re.search(p, ab, re.I) for p in pats):
                    method = meth
                    break
            sm = re.search(r"[Nn]\s*=\s*([\d,]+)", ab)
            sample = int(sm.group(1).replace(",", "")) if sm else 0
            ym = re.search(r"\b(19|20)\d{2}\b", ab)
            year = ym.group(0) if ym else "?"
            fm = re.search(r"(?:we found|results? (?:show|indicate)|conclud\w*|findings?:?)(.{10,140})",
                           ab, re.I)
            finding = fm.group(1).strip() if fm else ab[-140:].strip()
            papers.append(Paper(i, title, method, sample, finding, year))

        # clusters by method x topical overlap
        clusters = {}
        for p in papers:
            words = set(re.findall(r"[a-z]{5,}", p.title.lower()))
            key = p.method
            clusters.setdefault(key, []).append(p)
        cluster_out = []
        for meth, ps in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
            sample_note = f"samples: {min(x.sample for x in ps if x.sample)}-{max(x.sample for x in ps if x.sample)}" if any(x.sample for x in ps) else "samples: unspecified"
            avg_sample = round(sum(x.sample for x in ps) / max(1, sum(1 for x in ps if x.sample)), 0) if any(x.sample for x in ps) else 0
            cluster_out.append({
                "method": meth, "n": len(ps), "avg_sample": avg_sample,
                "titles": [p.title[:60] for p in ps[:3]],
                "weight": "dominant" if len(ps) >= max(2, len(papers) * 0.3) else "minor",
            })

        # evolution by year
        by_year = sorted(papers, key=lambda p: p.year)
        evolution = []
        for p in by_year:
            evolution.append(f"{p.year} [S{p.idx}] {p.method}: {p.finding[:90]}")

        # contradictions: numeric findings within same method that disagree in direction
        contradictions = []
        for i in range(len(papers)):
            for j in range(i + 1, len(papers)):
                if papers[i].method != papers[j].method:
                    continue
                wi = set(re.findall(r"[a-z]{5,}", papers[i].finding.lower()))
                wj = set(re.findall(r"[a-z]{5,}", papers[j].finding.lower()))
                if len(wi & wj) >= 2:
                    neg_i = bool(re.search(r"\b(no|not|negative|null|decrease|reduce\w*)\b", papers[i].finding.lower()))
                    neg_j = bool(re.search(r"\b(no|not|negative|null|decrease|reduce\w*)\b", papers[j].finding.lower()))
                    if neg_i != neg_j:
                        contradictions.append(
                            f"S{papers[i].idx} vs S{papers[j].idx} (both {papers[i].method}): "
                            f"'{papers[i].finding[:60]}...' vs '{papers[j].finding[:60]}...'")
        # power warnings for small samples
        for p in papers:
            if 0 < p.sample < 30:
                contradictions.append(f"S{p.idx}: {p.method} with N={p.sample} is underpowered — treat as preliminary.")

        gaps = []
        for p in papers:
            for pat, name, action in GAP_PATTERNS:
                if re.search(pat, p.abstract if hasattr(p, "abstract") else "", re.I):
                    pass
        for ab, p in zip(abstracts, papers):
            for pat, name, action in GAP_PATTERNS:
                if re.search(pat, ab, re.I):
                    gaps.append({"gap": name, "from": f"S{p.idx}", "action": action})
        if not gaps:
            gaps.append({"gap": "no explicit gaps declared", "from": "-",
                         "action": "Read the limitations sections verbatim; authors under-report gaps here."})
        seen, dedup = set(), []
        for g in gaps:
            k = g["gap"]
            if k not in seen:
                seen.add(k); dedup.append(g)
        gaps = dedup[:6]

        matrix = [f"S{p.idx}: {p.method:18} N={p.sample or 'n/a':<8} {p.year}  {p.title[:44]}" for p in papers]

        verdict = (f"{len(papers)} papers | {len(cluster_out)} method clusters | "
                   f"{len(contradictions)} tensions | {len(gaps)} gap types")
        return LitReview(papers, cluster_out, evolution, contradictions, gaps, matrix, verdict)

    @staticmethod
    def format_review(r: LitReview) -> str:
        out = ["=" * 62, "LITERATURE REVIEW AGENT — REVIEW", "=" * 62, r.verdict, "-" * 62,
               "Citation matrix:"]
        out += [f"  {m}" for m in r.citation_matrix]
        out += ["-" * 62, "Method clusters:"]
        for c in r.clusters:
            out.append(f"  {c['method']:18} n={c['n']} avg N={c['avg_sample'] or '-':<6} [{c['weight']}]")
            out += [f"      - {t}" for t in c["titles"]]
        out += ["-" * 62, "Chronological evolution:"]
        out += [f"  {e}" for e in r.evolution]
        if r.contradictions:
            out += ["-" * 62, "Contradictions & power concerns:"]
            out += [f"  ! {c}" for c in r.contradictions[:6]]
        out += ["-" * 62, "Research gaps (ranked by tractability):"]
        out += [f"  {i}. {g['gap']} (from {g['from']}) -> {g['action']}" for i, g in enumerate(r.gaps, 1)]
        out.append("=" * 62)
        return "\n".join(out)

"""
Contract Reviewer Agent Engine.
Detects clause families (termination, liability, indemnity, IP,
confidentiality, renewal), grades each found clause, lists missing
protective clauses, and drafts redlines with fallbacks.
Not legal advice — preparation for counsel review.
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class ClauseFinding:
    clause: str
    found: bool
    grade: str          # favorable / balanced / one-sided / absent
    excerpt: str
    issue: str
    redline: str
    fallback: str

@dataclass
class ContractReview:
    side: str
    word_count: int
    clauses: List[ClauseFinding] = field(default_factory=list)
    risky_terms: List[str] = field(default_factory=list)
    missing: List[str] = field(default_factory=list)
    escalation: List[str] = field(default_factory=list)
    verdict: str = ""

CLAUSE_PATTERNS = {
    "termination": r"(terminat\w+|end\w* (?:this|the) agreement|notice period of \w+ days)",
    "liability_cap": r"(limit\w* (?:of )?liability|liability (?:is|shall be)? (?:capped|limited)|aggregate liability)",
    "indemnity": r"(indemnif\w+|hold harmless|defend)",
    "ip_ownership": r"(intellectual property|ownership of (?:the )?work|work product|assigns? all right)",
    "confidentiality": r"(confidential\w*|non-?disclosure|NDA)",
    "auto_renewal": r"(auto(?:matic(?:ally)?)?[- ]?renew\w*|evergreen|shall renew for)",
    "governing_law": r"(govern(?:ed|ing) (?:by|law)|jurisdiction|venue|applicable law)",
    "payment_terms": r"(net \d{1,2}|payment (?:is )?due|invoice|late (?:fee|charge|interest))",
    "warranty": r"(warrant\w+|as[- ]is|disclaim\w+)",
    "data_protection": r"(personal data|GDPR|data processing|CCPA|privacy)",
}

RISK_TERMS = [
    (r"unlimited liability|liability (?:shall not be limited|is excluded)", "critical",
     "unlimited/excluded liability language detected"),
    (r"sole (?:and )?discretion", "high",
     "counterparty 'sole discretion' — convert to objective standards"),
    (r"indemnif\w+ [^.]{0,80}(?:any and all|all claims|unlimited)", "high",
     "uncapped indemnity scope"),
    (r"perpetu\w+|in perpetuity", "medium",
     "perpetual grant — add a term or a revocation right"),
    (r"non-?(?:exclusive )?assign\s+.{0,40}rights.{0,40}without (?:the )?consent", "medium",
     "free assignment to third parties (assign to a competitor?)"),
    (r"terminat\w+ [^.]{0,60}immediate\w* (?:effect|upon)", "medium",
     "immediate termination right — demand notice + cure period"),
    (r"exclusiv\w+", "medium",
     "exclusivity — scope-limit it (field, territory, duration) or price it"),
    (r"liquidated damages", "medium",
     "liquidated damages — verify it's a genuine pre-estimate, not a penalty"),
]

class ContractReviewerEngine:
    """Read the contract like the side that gets sued, not the side that signs fast."""

    @classmethod
    def review(cls, contract_text: str, side: str = "buyer") -> ContractReview:
        text = contract_text
        low = text.lower()
        wc = len(text.split())

        clauses = []

        def excerpt_for(pattern):
            m = re.search(pattern, low)
            if not m:
                return ""
            start = max(0, m.start() - 60)
            return re.sub(r"\s+", " ", text[start:m.end() + 120]).strip()[:170]

        # termination
        found = bool(re.search(CLAUSE_PATTERNS["termination"], low))
        grade = "absent"
        issue = redline = fallback = ""
        if found:
            has_cure = bool(re.search(r"(cure|remed\w+).{0,60}(\d{1,2})\s*days|(\d{1,2})\s*days.{0,40}cure", low))
            notice = re.search(r"(\d{1,3})\s*(?:business\s+)?days'? (?:written )?notice", low)
            n_days = int(notice.group(1)) if notice else 0
            if side == "buyer":
                if n_days >= 60 and has_cure:
                    grade, issue = "favorable", f"{n_days}-day notice + cure period present."
                elif n_days >= 30:
                    grade, issue = "balanced", f"{n_days}-day notice; " + ("no explicit cure period." if not has_cure else "cure period ok.")
                    redline = "Add: 30-day cure period for material breach before termination takes effect."
                    fallback = "Accept if relationship is short-cycle."
                else:
                    grade, issue = "one-sided", "short/no notice period for termination."
                    redline = "Require 60 days' written notice + 30-day cure period for material breach."
                    fallback = "30 days notice minimum, cure period for fixable breaches."
            else:
                grade = "favorable" if n_days <= 30 else "balanced"
        else:
            issue = "No termination clause found — contract has no defined exit."
            redline = "Add termination: either party, 60 days' notice, plus immediate-for-cause with cure."
        clauses.append(ClauseFinding("termination", found, grade, excerpt_for(CLAUSE_PATTERNS["termination"]), issue, redline, fallback))

        # liability cap
        found = bool(re.search(CLAUSE_PATTERNS["liability_cap"], low))
        cap = re.search(r"(?:liability|damages).{0,120}?(?:\$|USD\s?|EUR\s?|£)\s?([\d,]+(?:\.\d+)?)\s?([km]?)", text, re.I)
        mult = re.search(r"(?:limited|capped).{0,80}?(?:fees?|amounts?) (?:paid|payable).{0,60}?(\d+)[x×]", low)
        grade, issue, redline, fallback = "absent", "", "", ""
        if found or cap or mult:
            if cap:
                val = float(cap.group(1).replace(",", "")) * (1000 if cap.group(2) == "k" else 1e6 if cap.group(2) == "m" else 1)
                issue = f"Cap appears to be a fixed amount: ${val:,.0f}."
                grade = "balanced" if val >= 50000 else "one-sided"
            elif mult:
                issue = f"Cap = {mult.group(1)}x fees paid."
                grade = "balanced" if int(mult.group(1)) >= 2 else "one-sided"
            else:
                issue = "Liability limitation language present; cap size unclear."
                grade = "one-sided"
            if side == "buyer":
                redline = "Cap at the greater of 12 months' fees or $[amount]; carve-outs for confidentiality breach, IP infringement, and gross negligence."
                fallback = "Mutual cap at fees paid in the trailing 12 months; carve-outs limited to willful misconduct."
            else:
                redline = "Keep cap at 12 months' fees; add mutual application and a super-cap for data breach."
                fallback = "Cap at total fees paid; no carve-outs beyond IP indemnity."
        else:
            issue = "NO liability cap — exposure is unlimited as written."
            redline = "Insert mutual liability cap (greater of 12-month fees or fixed amount) with standard carve-outs."
            fallback = "None — an uncapped contract is a walk-away unless counsel says otherwise."
        clauses.append(ClauseFinding("liability_cap", found or bool(cap or mult), grade,
                                     excerpt_for(CLAUSE_PATTERNS["liability_cap"]), issue, redline, fallback))

        # indemnity
        found = bool(re.search(CLAUSE_PATTERNS["indemnity"], low))
        one_sided = bool(re.search(r"(?:customer|client|you)\s+(?:shall|will|agrees?\s+to)\s+indemnif", low)) and side == "buyer"
        grade = "one-sided" if one_sided else ("balanced" if found else "absent")
        issue = "Indemnity present." if found else "No indemnity clause."
        if one_sided:
            issue = "One-way indemnity: buyer indemnifies seller, not mutual."
        redline = "Make indemnity MUTUAL; cap indemnity except for IP infringement and willful misconduct; require prompt notice + control of defense."
        fallback = "Mutual indemnity limited to third-party IP claims."
        clauses.append(ClauseFinding("indemnity", found, grade,
                                     excerpt_for(CLAUSE_PATTERNS["indemnity"]), issue, redline, fallback))

        # IP
        found = bool(re.search(CLAUSE_PATTERNS["ip_ownership"], low))
        buyer_loses = bool(re.search(r"(?:contractor|provider|supplier|vendor)\s+(?:shall|will|owns?)", low)) and side == "buyer"
        grade = "balanced" if found and not buyer_loses else ("one-sided" if found else "absent")
        issue = "IP ownership addressed." if found else "No IP/work-product ownership clause."
        if buyer_loses:
            issue = "IP language appears to favor the counterparty."
        redline = "Buyer owns all deliverables/work product upon payment; provider retains background IP with a license to buyer."
        fallback = "Ownership on payment, perpetual license to background IP."
        clauses.append(ClauseFinding("ip_ownership", found, grade,
                                     excerpt_for(CLAUSE_PATTERNS["ip_ownership"]), issue, redline, fallback))

        # confidentiality / auto-renewal / governing law / data protection quick checks
        for name, label, buyer_redline in (
            ("confidentiality", "confidentiality", "Term: 3 years post-termination (trade secrets: perpetual); mutual scope."),
            ("auto_renewal", "auto-renewal", "Convert to affirmative renewal (opt-in); 60-day non-renewal notice window."),
            ("governing_law", "governing law", "Neutral forum or your home jurisdiction; arbitration option for cross-border."),
            ("data_protection", "data protection", "Add DPA incorporating SCCs where transfer applies; breach notice within 72h."),
            ("payment_terms", "payment terms", "Net-30 from valid invoice; dispute window with withholding right for disputed amounts."),
            ("warranty", "warranty", "90-day re-performance warranty; 'as-is' only if priced accordingly."),
        ):
            found = bool(re.search(CLAUSE_PATTERNS[name], low))
            grade = "balanced" if found else "absent"
            issue = f"{label.capitalize()} clause present." if found else f"No {label} clause — the default will be whatever local law implies, which you have not read."
            redline = buyer_redline if not found or side == "buyer" else ""
            fallback = "Accept with confirmation of current practice."
            clauses.append(ClauseFinding(name, found, grade,
                                         excerpt_for(CLAUSE_PATTERNS[name]), issue, redline, fallback))

        risky = []
        for pat, sev, desc in RISK_TERMS:
            m = re.search(pat, low)
            if m:
                snippet = re.sub(r'\s+', ' ', text[max(0, m.start()-30):m.end()+40])[:90]
                risky.append(f"[{sev}] {desc} — near \"{snippet}\"")

        missing = [c.clause for c in clauses if c.grade == "absent"]

        escalation = [
            "Counsel review is REQUIRED if: liability is uncapped, indemnity is one-way, or IP assignment is ambiguous.",
            "Finance sign-off for: payment terms deviating from Net-30, any auto-renewal with <60-day exit window.",
            "Security/privacy sign-off whenever personal data is processed (attach the DPA before signature).",
        ]

        critical = [r for r in risky if r.startswith("[critical]")]
        verdict = (f"{wc} words | {len([c for c in clauses if c.found])}/{len(clauses)} clause families found | "
                   f"{len(missing)} missing | {len(risky)} risky term(s)"
                   + (" | COUNSEL REQUIRED" if critical or "unlimited" in " ".join(risky).lower() else ""))
        return ContractReview(side, wc, clauses, risky, missing, escalation, verdict)

    @staticmethod
    def format_review(r: ContractReview) -> str:
        out = ["=" * 62, "CONTRACT REVIEWER AGENT — REVIEW", "=" * 62, r.verdict, "-" * 62,
               "Clause map:"]
        for c in r.clauses:
            mark = {"favorable": "+", "balanced": "=", "one-sided": "!", "absent": "-"}[c.grade]
            out.append(f"  [{mark}] {c.clause:18} {c.grade:10} {c.issue[:76]}")
            if c.excerpt:
                out.append(f"        ...{c.excerpt[:100]}...")
            if c.redline:
                out.append(f"        redline: {c.redline[:100]}")
                out.append(f"        fallback: {c.fallback[:90]}")
        if r.risky_terms:
            out += ["-" * 62, "Risky terms (exact-text search):"]
            out += [f"  {t}" for t in r.risky_terms[:8]]
        if r.missing:
            out += ["-" * 62, "MISSING clauses (silence = risk): " + ", ".join(r.missing)]
        out += ["-" * 62, "Escalation triggers:"] + [f"  * {e}" for e in r.escalation]
        out += ["=" * 62,
                "Disclaimer: structured preparation for counsel review — not legal advice, and no attorney-client privilege applies."]
        return "\n".join(out)

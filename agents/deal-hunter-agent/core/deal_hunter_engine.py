"""
Deal Hunter Agent Engine.
Evaluates product candidates: price percentile vs reference, rating
confidence (shrunk by review count), need coverage — then BUY/WAIT/PASS.
"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class CandidateVerdict:
    name: str
    price: float
    reference: float
    discount_pct: float
    rating: float
    reviews: int
    bayesian_rating: float
    need_coverage: float
    value_score: float
    verdict: str
    target_price: float
    rationale: str

@dataclass
class DealVerdict:
    candidates: List[CandidateVerdict] = field(default_factory=list)
    ranking: List[str] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)
    verdict: str = ""

class DealHunterEngine:
    """A discount on something you don't need is 100% waste with extra steps."""

    @classmethod
    def evaluate(cls, candidates: List[dict], needs: List[str] = None) -> DealVerdict:
        needs = [n.lower().strip() for n in (needs or []) if n.strip()]
        out = []

        for c in candidates:
            name = str(c.get("name", c.get("product", "item")))
            price = float(c.get("price", 0) or 0)
            reference = float(c.get("reference_price", c.get("msrp", price)) or price)
            rating = float(c.get("rating", 0) or 0)
            reviews = int(c.get("reviews", c.get("review_count", 0)) or 0)
            features = [str(f).lower() for f in (c.get("features", []) or [])]
            stock = str(c.get("stock", "unknown")).lower()

            discount = round(100 * (1 - price / reference), 1) if reference > 0 else 0.0

            # Bayesian shrinkage toward 3.8 prior; C = 50 pseudo-reviews
            prior_mean, C = 3.8, 50
            bayes = round((prior_mean * C + rating * reviews) / (C + reviews), 2) if reviews else prior_mean

            if needs and features:
                covered = sum(1 for n in needs if any(n in f or f in n for f in features))
                coverage = round(covered / len(needs), 2)
            elif needs:
                blob = " ".join(features)
                covered = sum(1 for n in needs if n in blob)
                coverage = round(covered / len(needs), 2)
            else:
                coverage = 0.5  # neutral when no needs declared

            # value score: discount quality (capped), rating confidence, coverage
            disc_score = min(discount, 45) / 45
            rating_score = max(0.0, min(1.0, (bayes - 3.0) / 1.8))
            value = round(100 * (0.35 * disc_score + 0.30 * rating_score + 0.35 * coverage), 1)

            target = round(price * (0.85 if discount >= 30 else 0.90), 2)
            if coverage < 0.5 and needs:
                verdict = "PASS"
                rationale = (f"covers only {coverage:.0%} of your needs — the discount buys the wrong product")
            elif value >= 70 and discount >= 20:
                verdict = "BUY"
                rationale = (f"{discount:.0f}% off with trusted rating ({bayes:.1f} bayesian over {reviews} reviews) "
                             f"and {coverage:.0%} need coverage")
            elif discount >= 35 and bayes >= 4.0:
                verdict = "BUY"
                rationale = f"deep discount ({discount:.0f}%) on a well-rated item — historical-price percentile favors acting"
            elif discount < 10:
                verdict = "WAIT"
                rationale = f"only {discount:.0f}% off — within normal price noise; set an alert at {target}"
            else:
                verdict = "WAIT"
                rationale = f"moderate deal; value score {value} — a 10-15% further drop makes it compelling"

            if stock in ("low", "last items") and verdict == "WAIT":
                rationale += " (stock is low: if it sells out, the wait was the wrong call — decide risk tolerance)"

            out.append(CandidateVerdict(name, price, reference, discount, rating, reviews,
                                        bayes, coverage, value, verdict, target, rationale))

        out.sort(key=lambda c: -c.value_score)
        ranking = [f"{c.name}: {c.verdict} (value {c.value_score}) — {c.rationale}" for c in out]
        alerts = [f"{c.name}: alert when price <= {c.target}" for c in out if c.verdict == "WAIT"][:5]

        buys = sum(1 for c in out if c.verdict == "BUY")
        verdict = f"{len(out)} candidates | {buys} BUY | {len(alerts)} WAIT-with-alert | rest PASS"
        return DealVerdict(out, ranking, alerts, verdict)

    @staticmethod
    def format_verdict(v: DealVerdict) -> str:
        out = ["=" * 62, "DEAL HUNTER AGENT — VERDICT", "=" * 62, v.verdict, "-" * 62,
               f"{'item':22}{'price':>8}{'ref':>8}{'off%':>6}{'rating':>8}{'needs':>7}  verdict"]
        for c in v.candidates:
            out.append(f"{c.name[:22]:22}{c.price:>8.0f}{c.reference:>8.0f}{c.discount_pct:>6.1f}"
                       f"{c.bayesian_rating:>8.1f}{c.need_coverage:>7.0%}  {c.verdict}")
        out += ["-" * 62, "Ranked rationale:"]
        out += [f"  {i}. {r}" for i, r in enumerate(v.ranking, 1)]
        if v.alerts:
            out += ["-" * 62, "Set price alerts:"] + [f"  * {a}" for a in v.alerts]
        out += ["=" * 62, "Rule: never let a countdown timer make a decision a spreadsheet could make."]
        return "\n".join(out)

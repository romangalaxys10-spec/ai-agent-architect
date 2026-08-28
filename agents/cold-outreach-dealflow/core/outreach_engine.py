"""
Cold Outreach & Dealflow Closer Engine.
Constructs 3-step high-deliverability technical email sequences, audits spam scores, and generates Statements of Work (SOW).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import re


@dataclass
class EmailTouchpoint:
    step_number: int
    subject: str
    body: str
    deliverability_score: float  # 0.0 to 1.0


@dataclass
class DealProposal:
    client_name: str
    project_scope: str
    milestones: List[Dict[str, Any]]
    total_fee_usd: float
    sow_markdown: str


class ColdOutreachDealflow:
    """Generates high-converting technical B2B outreach sequences and client SOW proposals."""

    SPAM_WORDS = [
        "100% free", "guaranteed", "act now", "limited time",
        "make money", "risk-free", "winner", "earn cash"
    ]

    @classmethod
    def generate_sequence(cls, target_name: str, target_company: str, tech_stack: str = "Solana & Python") -> List[EmailTouchpoint]:
        first_name = target_name.split()[0]

        # Touch 1: Technical observation / free value
        sub_1 = f"Quick technical question re: {target_company}'s indexing pipeline"
        body_1 = f"""Hi {first_name},

Noticed your team is scaling infrastructure on {tech_stack}.

We recently solved a critical slot-latency dropout issue in Yellowstone Geyser streams by moving to a deterministic preflight simulation layer.

Put together a 2-page architectural teardown showing how we dropped latency to 0.04ms. Happy to send it over if you're exploring optimizations this quarter.

Best,
Architect"""

        # Touch 2: Benchmark case study
        sub_2 = f"Case study: {target_company} latency optimization"
        body_2 = f"""Hi {first_name},

Following up on my previous note. We just published our benchmark results showing a 68% reduction in RPC overhead using our autonomous agent pipeline.

Open-sourced the full implementation here: github.com/romangalaxys10-spec/ai-agent-architect

Would love to hear how {target_company} currently handles high-volatility spikes.

Best,
Architect"""

        # Touch 3: Low-friction exit
        sub_3 = f"Closing the loop / {target_company}"
        body_3 = f"""Hi {first_name},

Assuming your current {tech_stack} pipeline is dialed in right now.

If you ever run into scale bottlenecks or want an independent architecture audit down the road, feel free to reach out anytime.

Best,
Architect"""

        touches = []
        for i, (sub, b) in enumerate([(sub_1, body_1), (sub_2, body_2), (sub_3, body_3)]):
            # Calculate deliverability score (check for spam words)
            has_spam = any(w in (sub + " " + b).lower() for w in cls.SPAM_WORDS)
            score = 0.98 if not has_spam else 0.70
            touches.append(EmailTouchpoint(step_number=i+1, subject=sub, body=b, deliverability_score=score))

        return touches

    @classmethod
    def generate_sow(cls, client: str, scope: str, fee: float = 8500.0) -> DealProposal:
        sow = f"""# Statement of Work (SOW)
**Client:** {client}  
**Architect:** Autonomous Systems Labs  
**Engagement Fee:** ${fee:,.2f} USD  

---

## 1. Project Objective & Scope
{scope}

---

## 2. Deliverables & Milestones
* **Milestone 1 (Architecture Blueprint):** Decompose system DAG and define interface schemas ($2,500.00).
* **Milestone 2 (Core Engine Implementation):** Deploy deterministic pipeline with automated test fixtures ($3,500.00).
* **Milestone 3 (Verification & Delivery):** Final load testing, security secret audit, and production handoff ($2,500.00).

---

## 3. Payment Terms
Invoiced via `invoice-billing-sentinel` upon milestone sign-off. Net 14 payment terms.
"""
        return DealProposal(
            client_name=client,
            project_scope=scope,
            milestones=[
                {"name": "Architecture Blueprint", "amount": 2500.0},
                {"name": "Core Engine Implementation", "amount": 3500.0},
                {"name": "Verification & Delivery", "amount": 2500.0},
            ],
            total_fee_usd=fee,
            sow_markdown=sow,
        )

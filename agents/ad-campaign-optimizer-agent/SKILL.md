---
name: ad-campaign-optimizer-agent
description: 'Computes CTR/CPC/CPA/ROAS, flags waste, and reallocates budget with experiment plan'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# Ad Campaign Optimizer Agent

> "Computes CTR/CPC/CPA/ROAS, flags waste, and reallocates budget with experiment plan."

**Demand basis:** Ad-spend optimization agents deliver the most directly measurable marketing ROI.

## 🎯 Activation Triggers
- `optimize ad spend`
- `campaign audit`
- `ROAS analysis`
- `budget reallocation`

## ⚡ Execution Protocol
1. Compute per-campaign metrics: CTR, CPC, CPA, ROAS, and share of wasted spend.
2. Classify performance (scale / fix / pause) against breakeven thresholds.
3. Reallocate budget to marginal-ROAS winners and design one clean experiment per loser.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/ad-campaign-optimizer-agent/cli/ad_campaign.py --help`
- **Input:** CLI arguments (see `--help`); text or JSON input inline or via `--file`
- **Output:** structured report with verdict/plan + ranked next actions
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + length ceilings before processing (guardrails discipline)
- 3-currency budgets (steps/tokens/wall-clock) enforced by the master loop
- JSONL event + cost entries via the observability bus on every run
- Findings carry evidence + severity so the evaluation judge can score them

## 🔗 See Also
- Hub catalog: [`agents/AGENTS.md`](../AGENTS.md)
- Master architecture: [`README.md`](../../README.md)

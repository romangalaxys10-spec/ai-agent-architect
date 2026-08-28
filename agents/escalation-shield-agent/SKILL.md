---
name: escalation-shield-agent
description: 'Computes churn-risk from account signals and prescribes the save play before escalation'
version: 1.0.0
author: AI Agent Architect
category: 'Customer Support'
---

# Escalation Shield Agent

> "Computes churn-risk from account signals and prescribes the save play before escalation."

**Demand basis:** Churn-prediction agents are the highest-ROI CS agents per vendor case studies.

## 🎯 Activation Triggers
- `churn risk`
- `escalate account`
- `save play`
- `angry customer signals`

## ⚡ Execution Protocol
1. Ingest account signals: ticket volume trend, sentiment words, plan, tenure, open issue age.
2. Compute churn risk score with weighted evidence and tier (healthy/at-risk/critical).
3. Prescribe the save play: who calls whom, what to concede, what to fix first, follow-up cadence.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/escalation-shield-agent/cli/escalation_shield.py --help`
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

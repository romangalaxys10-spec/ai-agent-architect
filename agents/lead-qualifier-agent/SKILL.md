---
name: lead-qualifier-agent
description: 'Scores leads on BANT evidence, tiers MQL/SQL, and writes the disqualifier truth'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# Lead Qualifier Agent

> "Scores leads on BANT evidence, tiers MQL/SQL, and writes the disqualifier truth."

**Demand basis:** AI sales agent market: $3.25B in 2024 growing at 44.7% CAGR — qualification is task #1.

## 🎯 Activation Triggers
- `qualify lead`
- `BANT scoring`
- `MQL or SQL`
- `lead disqualification`

## ⚡ Execution Protocol
1. Extract BANT evidence: budget signals, authority titles, need verbs, timeline dates.
2. Score each pillar with evidence quotes and compute tier (MQL/SQL/disqualify) honestly.
3. Output next-best-action sequence and the exact disqualifiers, if any, to keep pipeline clean.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/lead-qualifier-agent/cli/lead_qualifier.py --help`
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

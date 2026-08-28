---
name: fact-check-agent
description: 'Decomposes claims into atomic assertions and verifies each against evidence'
version: 1.0.0
author: AI Agent Architect
category: 'Research & Analysis'
---

# Fact Check Agent

> "Decomposes claims into atomic assertions and verifies each against evidence."

**Demand basis:** Fact-checking agents are heavily demanded by newsrooms and enterprise comms.

## 🎯 Activation Triggers
- `fact check`
- `verify claim`
- `evidence check`
- `claim decomposition`

## ⚡ Execution Protocol
1. Split the claim into atomic, independently checkable assertions.
2. Match each assertion to evidence: supports / refutes / insufficient with quoted spans.
3. Render a verdict (CONFIRMED / REFUTED / PARTIALLY / UNVERIFIED) with confidence and trail.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/fact-check-agent/cli/fact_check.py --help`
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

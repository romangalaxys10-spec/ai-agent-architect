---
name: contract-reviewer-agent
description: 'Detects and grades clauses, flags missing terms, drafts negotiation redlines'
version: 1.0.0
author: AI Agent Architect
category: 'Education, Legal & Life'
---

# Contract Reviewer Agent

> "Detects and grades clauses, flags missing terms, drafts negotiation redlines."

**Demand basis:** Contract-review agents are the most-deployed legal AI (in-house teams first).

## 🎯 Activation Triggers
- `review contract`
- `clause audit`
- `redline draft`
- `contract risk`

## ⚡ Execution Protocol
1. Detect clause families: termination, liability caps, indemnity, IP, confidentiality, renewal, Governing law.
2. Grade each found clause (favorable/balanced/one-sided) and list missing protective clauses.
3. Draft redline language with fallback positions and escalation triggers for counsel.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/contract-reviewer-agent/cli/contract_reviewer.py --help`
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

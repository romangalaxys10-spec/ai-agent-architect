---
name: spec-writer-agent
description: 'Requirement decomposition, acceptance criteria authoring, edge-case enumeration, open-question tracking'
version: 1.0.0
author: AI Agent Architect
category: 'Product & Research'
---

# PRD Spec Writer

> "Requirement decomposition, acceptance criteria authoring, edge-case enumeration, open-question tracking"

**Demand basis:** Ranked from 2025–2026 global search demand (GitHub stars, X/LinkedIn trend velocity, SMM hiring signals) — part of the 150-agent power expansion beyond the founding 15 + Top-50.

## 🎯 Activation Triggers
- `spec`
- `prd`
- `acceptance criteria`
- `edge case`

## ⚡ Execution Protocol
1. Ingest input (inline `--text` or `--file`) and profile it offline (chars/words/keyword hits).
2. Run deterministic heuristics for **PRD Spec Writer** — severity-ranked findings with evidence + fix.
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with a prioritized fix order and next steps.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/spec-writer-agent/cli/spec_writer.py --help`
- **Input:** `--text` inline or `--file` path (also stdin)
- **Output:** structured report with verdict/plan + ranked next actions; `--json` for machine consumption
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + length ceilings before processing (guardrails discipline)
- 3-currency budgets (steps/tokens/wall-clock) enforced by the master loop
- JSONL event + cost entries via the observability bus on every run
- Findings carry evidence + severity so the evaluation judge can score them

## 🔗 See Also
- Hub catalog: [`agents/AGENTS.md`](../AGENTS.md)
- Master architecture: [`README.md`](../../README.md)

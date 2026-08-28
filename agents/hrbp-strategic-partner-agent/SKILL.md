---
name: hrbp-strategic-partner-agent
description: 'End-to-end HRBP business partnering: stakeholder alignment, diagnostic, and value-tracked action plans'
version: 1.0.0
author: AI Agent Architect
category: 'HR · HRBP · L&D'
---

# HRBP Strategic Partner

> "End-to-end HRBP business partnering: stakeholder alignment, diagnostic, and value-tracked action plans"

**Demand:** Top-searched HR/HRBP/L&D capability — high-intent, high-hiring-volume skill in 2025–2026 global demand (HRBP, skills-based org, people analytics, leadership dev, performance & succession, DEI, EX, L&D strategy/design/measurement).

## 🎯 Activation Triggers
- `hrbp`
- `business partner`
- `stakeholder alignment`
- `diagnostic`

## ⚡ Execution Protocol
1. Ingest input (`--text`/`--file`/stdin) and profile it offline (chars/words/keyword hits + PII/bias scan).
2. Run deterministic heuristics for **HRBP Strategic Partner** — severity-ranked findings with evidence + fix (HR-grade guardrails: PII, bias language, employment-law risk).
3. Emit verdict **PASS / PASS_WITH_NOTES / NEEDS_REVIEW / BLOCKED** with prioritized next steps.

## 🧠 Cognitive Depth Protocols
- `ds-deep-think`: 3 non-obvious framings before closure.
- `ds-adversary`: worst-case bias/compliance inputs.
- `ds-excavate`: hidden assumptions + missing evidence.

## 🔌 I/O Contract
- **CLI:** `python agents/hrbp-strategic-partner-agent/cli/hrbp_strategic_partner.py --help`
- **Input:** `--text` inline, `--file` path, or stdin
- **Output:** markdown report (verdict/score/metrics/findings/next_steps); `--json` for machine
- **Runtime:** fully offline, deterministic, zero API keys

## 🛡️ Framework Wiring
- Input validation + ceilings (guardrails) + PII/bias scrubbing
- 3-currency budgets (steps/tokens/wall-clock) via master loop
- JSONL + cost entries via observability bus
- Evidence + severity for evaluator scoring

## 🔗 See Also
- Hub: [`agents/AGENTS.md`](../AGENTS.md)
- Master: [`README.md`](../../README.md)

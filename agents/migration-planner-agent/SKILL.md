---
name: migration-planner-agent
description: 'Plans framework/version migrations as phased, reversible, dual-run campaigns'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Migration Planner Agent

> "Plans framework/version migrations as phased, reversible, dual-run campaigns."

**Demand basis:** Migration agents (Python 2->3, framework major bumps) are evergreen high-search topics.

## 🎯 Activation Triggers
- `plan migration`
- `upgrade framework`
- `port to new version`
- `migration risk assessment`

## ⚡ Execution Protocol
1. Inventory migration surface: pattern counts in code, config files, and API-touching code paths.
2. Build a phased plan (inventory -> shim -> dual-run -> cut over -> cleanup) with risk gates and rollback.
3. Estimate effort per phase from pattern counts and flag irreversibility points needing HITL approval.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/migration-planner-agent/cli/migration_planner.py --help`
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

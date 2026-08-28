---
name: refactor-pilot-agent
description: 'Detects code smells and flies a risk-gated, step-by-step refactoring flight plan'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Refactor Pilot Agent

> "Detects code smells and flies a risk-gated, step-by-step refactoring flight plan."

**Demand basis:** Refactoring agents rank among the most-requested IDE agent features.

## 🎯 Activation Triggers
- `refactor module`
- `code smell audit`
- `clean up code`
- `improve maintainability`

## ⚡ Execution Protocol
1. Detect smells: duplication (line-set similarity), long functions, long parameter lists, god classes, magic numbers, deep nesting.
2. Order refactorings by impact-on-maintainability over risk, with behavior-preservation guards per step.
3. Emit a flight plan: steps, tests-to-add-before-each-step, rollback points, effort estimate.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/refactor-pilot-agent/cli/refactor_pilot.py --help`
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

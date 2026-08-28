---
name: test-forge-agent
description: 'Generates runnable pytest skeletons and closes coverage gaps with branch accounting'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Test Forge Agent

> "Generates runnable pytest skeletons and closes coverage gaps with branch accounting."

**Demand basis:** Test generation is a top-3 requested coding-agent capability in developer surveys.

## 🎯 Activation Triggers
- `generate tests`
- `close coverage gap`
- `write unit tests`
- `test plan for module`

## ⚡ Execution Protocol
1. Parse the target module: functions, classes, signatures, and branch inventory (if/for/while/try/except).
2. Generate pytest test skeletons per public callable with happy-path, edge-case, and failure-case slots.
3. Score projected coverage against the requested target and list the remaining uncovered branches.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/test-forge-agent/cli/test_forge.py --help`
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

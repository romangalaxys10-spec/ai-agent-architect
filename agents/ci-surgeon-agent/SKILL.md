---
name: ci-surgeon-agent
description: 'Parses CI failure logs, isolates root cause class, and prescribes the fix playbook'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# CI Surgeon Agent

> "Parses CI failure logs, isolates root cause class, and prescribes the fix playbook."

**Demand basis:** CI-red triage is the most recurring daily pain point reported by engineering teams.

## 🎯 Activation Triggers
- `fix CI`
- `diagnose build failure`
- `pipeline is red`
- `flaky test hunt`

## ⚡ Execution Protocol
1. Scan log text for failure signatures: assertion, timeout, import, OOM, network, flake markers, segfault, permission.
2. Classify failure class and blame domain (code / infra / flake / dependency / environment).
3. Emit a fix playbook ordered by expected fix probability plus a flake-vs-real verdict.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/ci-surgeon-agent/cli/ci_surgeon.py --help`
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

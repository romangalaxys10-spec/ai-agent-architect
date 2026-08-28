---
name: bug-triage-agent
description: 'Classifies bug reports, builds repro checklists, and ranks root-cause hypotheses'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Bug Triage Agent

> "Classifies bug reports, builds repro checklists, and ranks root-cause hypotheses."

**Demand basis:** Bug triage / issue grooming is the highest-time-cost activity maintainers report.

## 🎯 Activation Triggers
- `triage bug`
- `reproduce issue`
- `root cause analysis`
- `classify defect report`

## ⚡ Execution Protocol
1. Extract structured signals from the report: environment, steps, expected vs actual, stack traces, frequency words.
2. Classify defect class (crash/data-corruption/UI/perf/security) and severity x priority matrix.
3. Produce a reproduction checklist and rank root-cause hypotheses by prior probability with disconfirming tests.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/bug-triage-agent/cli/bug_triage.py --help`
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

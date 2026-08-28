---
name: socratic-tutor-agent
description: 'Builds question ladders from easy to hard with misconception probes and hints'
version: 1.0.0
author: AI Agent Architect
category: 'Education, Legal & Life'
---

# Socratic Tutor Agent

> "Builds question ladders from easy to hard with misconception probes and hints."

**Demand basis:** Tutoring agents are the most-searched education agent (2-sigma tutoring effect).

## 🎯 Activation Triggers
- `tutor me`
- `question ladder`
- `practice set`
- `explain socratically`

## ⚡ Execution Protocol
1. Map the topic into a concept dependency ladder for the student's level.
2. Generate Socratic question ladder: recall -> apply -> analyze -> transfer, per rung.
3. Attach misconception probes, hint ladder per problem (3 hints, no answers), and worked example.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/socratic-tutor-agent/cli/socratic_tutor.py --help`
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

---
name: interview-coach-agent
description: 'Designs structured interviews: question bank, rubrics, legal guardrails, scorecards'
version: 1.0.0
author: AI Agent Architect
category: 'HR & Recruiting'
---

# Interview Coach Agent

> "Designs structured interviews: question bank, rubrics, legal guardrails, scorecards."

**Demand basis:** Structured-interview agents reduce bias and are top asks for TA teams.

## 🎯 Activation Triggers
- `design interview`
- `question bank`
- `scorecard rubric`
- `structured hiring`

## ⚡ Execution Protocol
1. Map competencies for the role/level into question types (behavioral, system, craft).
2. Generate questions with STAR follow-ups and 1-5 anchored scoring rubrics.
3. Flag illegal/bias-risk questions (EEOC patterns) and produce the interviewer scorecard.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/interview-coach-agent/cli/interview_coach.py --help`
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

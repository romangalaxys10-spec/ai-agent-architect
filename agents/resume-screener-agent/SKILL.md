---
name: resume-screener-agent
description: 'Scores resume-job fit with evidence per skill, plus bias-safe language enforcement'
version: 1.0.0
author: AI Agent Architect
category: 'HR & Recruiting'
---

# Resume Screener Agent

> "Scores resume-job fit with evidence per skill, plus bias-safe language enforcement."

**Demand basis:** Resume screening is the highest-volume recruiting agent deployment.

## 🎯 Activation Triggers
- `screen resume`
- `rank candidates`
- `job fit score`
- `shortlist`

## ⚡ Execution Protocol
1. Parse job requirements (skills, years, education, nice-to-haves) into a weighted rubric.
2. Match resume evidence per skill (exact + alias), estimate experience, and score honestly.
3. Produce fit score, ranked shortlist, per-gap interview probes, and bias-safe wording audit.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/resume-screener-agent/cli/resume_screener.py --help`
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

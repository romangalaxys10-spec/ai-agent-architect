---
name: language-coach-agent
description: 'Analyzes learner writing: level estimate, error taxonomy, drills, CEFR path'
version: 1.0.0
author: AI Agent Architect
category: 'Education, Legal & Life'
---

# Language Coach Agent

> "Analyzes learner writing: level estimate, error taxonomy, drills, CEFR path."

**Demand basis:** Language-learning agents are top-10 education app agent requests.

## 🎯 Activation Triggers
- `language feedback`
- `grade my writing`
- `CEFR level`
- `grammar drills`

## ⚡ Execution Protocol
1. Analyze the learner text: sentence variety, error patterns, vocabulary breadth, idioms.
2. Estimate CEFR level with evidence and classify errors into a fix-first taxonomy.
3. Produce 3 targeted drills, a spaced repetition queue, and model rewrites of 2 sentences.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/language-coach-agent/cli/language_coach.py --help`
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

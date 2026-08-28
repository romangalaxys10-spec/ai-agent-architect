---
name: deep-research-agent
description: 'Cross-examines sources: corroboration matrix, contradiction detection, confidence bands'
version: 1.0.0
author: AI Agent Architect
category: 'Research & Analysis'
---

# Deep Research Agent

> "Cross-examines sources: corroboration matrix, contradiction detection, confidence bands."

**Demand basis:** 'Deep Research' is the single fastest-growing agent search term since late 2024.

## 🎯 Activation Triggers
- `deep research`
- `synthesize sources`
- `research question`
- `cross-examine evidence`

## ⚡ Execution Protocol
1. Decompose the research question into atomic sub-questions.
2. Extract claims per source, then build corroboration and contradiction matrices across sources.
3. Answer each sub-question with confidence band and evidence trail; flag unverifiable claims.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/deep-research-agent/cli/deep_research.py --help`
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

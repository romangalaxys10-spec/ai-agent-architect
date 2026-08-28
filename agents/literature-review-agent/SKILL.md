---
name: literature-review-agent
description: 'Clusters papers by method and finding, maps contradictions, and finds research gaps'
version: 1.0.0
author: AI Agent Architect
category: 'Research & Analysis'
---

# Literature Review Agent

> "Clusters papers by method and finding, maps contradictions, and finds research gaps."

**Demand basis:** Academic synthesis agents are the top researcher use case after summarization.

## 🎯 Activation Triggers
- `literature review`
- `survey papers`
- `research gap`
- `paper synthesis`

## ⚡ Execution Protocol
1. Parse paper blocks: title, method words, sample size, findings sentences.
2. Cluster by method x topic; build the chronological evolution and contradiction map.
3. Identify research gaps (untested combos, missing baselines, sample bias) ranked by tractability.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/literature-review-agent/cli/literature_review.py --help`
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

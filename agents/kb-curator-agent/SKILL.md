---
name: kb-curator-agent
description: 'Audits the knowledge base for gaps, duplicates, staleness, and coverage holes'
version: 1.0.0
author: AI Agent Architect
category: 'Customer Support'
---

# KB Curator Agent

> "Audits the knowledge base for gaps, duplicates, staleness, and coverage holes."

**Demand basis:** KB deflection is the top ROI lever support leaders cite for agent adoption.

## 🎯 Activation Triggers
- `audit knowledge base`
- `find KB gaps`
- `merge duplicate articles`
- `deflection analysis`

## ⚡ Execution Protocol
1. Load article set; compute topic coverage from question keyword clusters.
2. Detect near-duplicate articles (token Jaccard) and staleness (missing updates, dead version refs).
3. Produce a curation plan: merge pairs, rewrite list, new-article queue mapped to ticket themes.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/kb-curator-agent/cli/kb_curator.py --help`
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

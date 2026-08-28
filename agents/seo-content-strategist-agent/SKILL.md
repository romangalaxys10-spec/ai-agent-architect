---
name: seo-content-strategist-agent
description: 'Designs topic clusters, search intent, outlines, and internal link plans'
version: 1.0.0
author: AI Agent Architect
category: 'Sales & Marketing'
---

# SEO Content Strategist Agent

> "Designs topic clusters, search intent, outlines, and internal link plans."

**Demand basis:** Agentic SEO workflows are the fastest-growing marketing agent use case (2025-2026).

## 🎯 Activation Triggers
- `content strategy`
- `topic cluster`
- `SEO plan`
- `pillar page design`

## ⚡ Execution Protocol
1. Classify search intent for the keyword and map the pillar + spoke cluster topology.
2. Draft title variants, outline with H2/H3 intent coverage, and internal-link graph.
3. Attach an E-E-A-T checklist and SERP-feature targets (snippet, PAA, related).

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/seo-content-strategist-agent/cli/seo_content.py --help`
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

---
name: voice-of-customer-agent
description: 'Mines feedback corpora into quantified themes, sentiment, and prioritized pain points'
version: 1.0.0
author: AI Agent Architect
category: 'Customer Support'
---

# Voice of Customer Agent

> "Mines feedback corpora into quantified themes, sentiment, and prioritized pain points."

**Demand basis:** VoC/theme-mining agents are standard in every CX stack RFP.

## 🎯 Activation Triggers
- `analyze feedback`
- `customer themes`
- `voice of customer`
- `pain point mining`

## ⚡ Execution Protocol
1. Tokenize feedback items, build keyword co-occurrence clusters, and name each theme.
2. Score sentiment per item and aggregate to per-theme net sentiment and volume share.
3. Rank pain points by (negative sentiment x frequency x revenue words) into a top-5 fix list.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/voice-of-customer-agent/cli/voice_of_customer.py --help`
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

---
name: code-review-sentinel
description: 'Zero-trust PR review: severity-ranked findings, CWE mapping, verdict gate'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# Code Review Sentinel

> "Zero-trust PR review: severity-ranked findings, CWE mapping, verdict gate."

**Demand basis:** AI coding agents are the #1 most-searched agent class (Cursor, Claude Code, Devin, Copilot).

## 🎯 Activation Triggers
- `review code`
- `review PR`
- `audit pull request`
- `code quality gate`
- `pre-merge review`

## ⚡ Execution Protocol
1. Tokenize source into functions/classes and walk every line with a rule engine (complexity, mutability, security, hygiene).
2. Rank findings blocker/major/minor/info, map each to a CWE ID and remediation snippet.
3. Emit verdict PASS / NEEDS_CHANGES plus a prioritized fix order sized by risk-to-effort ratio.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/code-review-sentinel/cli/code_review.py --help`
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

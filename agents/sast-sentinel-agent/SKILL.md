---
name: sast-sentinel-agent
description: 'OWASP Top-10 aligned static security scanner with CVSS-style severity and remediation'
version: 1.0.0
author: AI Agent Architect
category: 'Coding & Development'
---

# SAST Sentinel Agent

> "OWASP Top-10 aligned static security scanner with CVSS-style severity and remediation."

**Demand basis:** Security scanning agents are the fastest-growing coding sub-category post-regulation.

## 🎯 Activation Triggers
- `security scan`
- `SAST`
- `find vulnerabilities`
- `OWASP check`
- `audit code security`

## ⚡ Execution Protocol
1. Run taint-shaped pattern rules: injection sinks, deserialization risk, weak crypto, secret leakage, TLS bypass.
2. Map each finding to OWASP Top-10 category, severity, and a concrete remediation snippet.
3. Emit a fix-ordered security report with a compliance verdict for CI gating.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/sast-sentinel-agent/cli/sast_sentinel.py --help`
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

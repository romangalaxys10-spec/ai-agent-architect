---
name: access-review-agent
description: 'Audits access grants for least-privilege violations and dormant privilege risk'
version: 1.0.0
author: AI Agent Architect
category: 'Ops, IT & Security'
---

# Access Review Agent

> "Audits access grants for least-privilege violations and dormant privilege risk."

**Demand basis:** Access-review agents are mandated by SOC2/ISO audits — recurring demand.

## 🎯 Activation Triggers
- `access review`
- `least privilege`
- `revoke stale access`
- `SOC2 evidence`

## ⚡ Execution Protocol
1. Parse grants: user, role, resource, permission, last-used days, MFA status.
2. Detect violations: unused > 90d, wildcard perms, privilege clusters, dormant accounts.
3. Produce revocation list ranked by risk and the audit-evidence bundle summary.

## 🧠 Cognitive Depth Protocols (Depth-Skills Powered)
- `ds-deep-think`: hold premature closure until 3 non-obvious framings are mapped.
- `ds-adversary`: stress-test the output against worst-case inputs before delivery.
- `ds-excavate`: surface hidden assumptions and missing evidence behind every score.

## 🔌 I/O Contract
- **CLI:** `python agents/access-review-agent/cli/access_review.py --help`
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

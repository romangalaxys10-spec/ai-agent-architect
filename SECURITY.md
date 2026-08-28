# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 2.x     | yes       |
| 1.x     | no        |

## Reporting a vulnerability

Email the maintainer via GitHub security advisories
(**Security → Report a vulnerability** on this repo). Please do not open a
public issue for vulnerabilities. We aim to respond within 72 hours.

## Security architecture (what this framework enforces)

- **OWASP LLM Top-10 (2025) checklist** ships in `core/guardrails.py::OWASP_LLM_TOP10_CHECKLIST` and is applied as a design review gate.
- **Prompt injection**: pattern detection on input (`SafetyGuardrails.audit_input`), untrusted-content delimiting (`delimit_untrusted`), six-tier trust model (`TrustTier`).
- **PII**: masking on inputs, outputs, tool arguments, memory writes, and trace spans (redaction at the observability boundary).
- **Excessive agency**: `is_safe` / `requires_approval` / `idempotent` / `failure_policy` declared per tool; HITL gates with fail-closed defaults (no resolver configured = reject).
- **Unbounded consumption**: three-currency budgets (steps / tokens / USD) with advertised-vs-enforced ceilings; `BudgetGovernor` spend caps.
- **Memory poisoning**: quarantine filter at the semantic-memory write boundary.
- **Tool misuse**: path-traversal and SSRF heuristics at the dispatch boundary (`audit_tool_arguments`).
- **Secrets**: never in system prompts; `.env.example` documents the full surface; secret-leak patterns audited on output.

## Known limitations

- The regex injection/PII detectors are heuristic defense-in-depth layers, not a substitute for an LLM-based classifier or a dedicated firewall in hostile environments.
- The in-process MCP transport runs tools with the host process's privileges; sandbox external servers in containers before granting them destructive tools.

# Contributing to AI Agent Architect

Thank you for considering a contribution. This framework's bar is *insanely great* — every PR must keep the end-to-end contract intact.

## Development setup

```bash
git clone https://github.com/romangalaxys10-spec/ai-agent-architect.git
cd ai-agent-architect
make install          # or: pip install -e . && pip install pytest pytest-cov
make test             # full suite runs OFFLINE with zero API keys
```

## The non-negotiables

1. **Offline-first.** Every feature must be testable with the `EchoProvider` / `ScriptedProvider` — no test may require an API key or network access. If your feature calls a live API, implement it behind `LLMProvider` and test with the mock.
2. **Errors are messages.** Tool/LLM failures return `ToolExecutionResult(success=False, ...)` — never raise into the agent loop.
3. **Every capability boundary is a trust boundary.** New tools declare `is_safe`, `requires_approval`, `idempotent`, and `failure_policy`.
4. **Sub-agents are complete or they don't merge.** Each agent in `agents/` must ship: `SKILL.md` (valid frontmatter), `core/` engine, `cli/` entrypoint — and `tests/test_subagent_completeness.py` must stay green, including the run-from-any-cwd CLI check.
5. **Budgets on every loop.** Any new long-running path wires a `BudgetPortfolio` (steps/tokens/seconds) and a `LoopDetector`.

## Pull request checklist

- [ ] `make test` passes (178+ tests, offline)
- [ ] `make lint` compiles every module
- [ ] New modules have tests with >90% line coverage
- [ ] Public APIs are backward-compatible or the PR documents the break
- [ ] `SKILL.md` frontmatter still parses (`make skills`)
- [ ] No secrets, keys, or PII committed (guardrails audit the repo too)

## Adding a new sub-agent

```bash
python cli/architect.py scaffold-skill --name my-agent --description "What it does"
# then complete: core/ engine, cli/ entrypoint, and register it in agents/
```

## Commit style

Conventional commits: `feat(scope): ...`, `fix(scope): ...`, `docs: ...`, `test: ...`, `chore: ...`.

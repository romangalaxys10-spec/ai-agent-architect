# 🧠 AI Agent Architect v2.0
### *A Complete, End-to-End Production Agent Framework — From Cognitive Design to Deployed Autonomy*

[![CI](https://github.com/romangalaxys10-spec/ai-agent-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/romangalaxys10-spec/ai-agent-architect/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests: 183 offline](https://img.shields.io/badge/tests-183%20offline-brightgreen.svg)]()
[![Agents Hub: 15 Sub-Agents](https://img.shields.io/badge/Agents%20Hub-15%20Complete%20Agents-brightgreen.svg)]()
[![Zero-Key Runtime](https://img.shields.io/badge/runtime-zero%20API%20keys-success.svg)]()
[![MCP](https://img.shields.io/badge/protocol-MCP%20%2B%20A2A-blueviolet.svg)]()

> **"An AI Agent is not a chatbot with a system prompt. It is an autonomous cognitive engine built with uncompromising taste, radical focus, and resilient architecture — and it must be complete: provider, loop, tools, memory, retrieval, protocols, guardrails, HITL, budgets, evals, telemetry. Anything less is a demo."**

---

## 🌟 What This Is

**AI Agent Architect** is a production-grade agent framework, cognitive engine, and monorepo sub-agent factory. Version 2.0 closes every gap identified against the definitive agent-engineering corpus:

| Reference | What it contributed to this design |
|---|---|
| Anthropic — *Building Effective Agents* | The five workflow patterns, agent-computer interface, tool poka-yoke |
| OpenAI — Agents SDK | Handoffs, guardrails with tripwires, sessions, agents-as-tools |
| Model Context Protocol (MCP) | JSON-RPC server/client, capability negotiation, tool annotations |
| Google A2A / Linux Foundation | Agent Cards, task lifecycle, skill-based discovery |
| Microsoft — *AI Agents for Beginners* + *Zero-to-Production* | Eval tiers (smoke vs full), tool-call accuracy metrics, deployment gates |
| ed-donner — *Master AI Agentic Engineering* | Middleware stack, evaluator loop, MCP-based memory, mock-LLM testing |
| bryanyzhu — *Agentic AI System Course* | Budgets (3 currencies), loop detection, compaction, trust tiers, HITL rulesets |
| GeneArnold — *AI Agent Engineering Course* | Rubric judges, mock-agent testing, JSONL logging, escalation ladders |
| MemGPT/Letta, Manus context research | Memory tiers, KV-cache-aware context assembly, note recitation |

**Everything runs offline with zero API keys** (deterministic Echo/Scripted providers) — then swaps to OpenAI/Anthropic/GLM/local models with one line.

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AGENT RUNTIME (core/)                            │
│                                                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌───────────────────────────────┐   │
│  │ LLM LAYER    │   │ AGENT LOOP   │   │ CONTEXT ENGINEERING           │   │
│  │ providers/   │◄──┤ agent_loop   ├──►│ compaction · notes · window   │   │
│  │ router·retry │   │ ReAct+tools  │   │ stable prefixes (KV-cache)    │   │
│  │ structured   │   │ parallel ✧   │   └───────────────────────────────┘   │
│  └──────────────┘   └──────┬───────┘   ┌───────────────────────────────┐   │
│                            │           │ RELIABILITY KIT                │   │
│  ┌─────────────────────────▼─────────┐ │ budgets(3) · loop detect      │   │
│  │ TOOL REGISTRY                     │ │ idempotency · failure policy  │   │
│  │ schema validation · hooks         │ └───────────────────────────────┘   │
│  │ dry-run · annotations             │ ┌───────────────────────────────┐   │
│  └─────────────────────────┬─────────┘ │ GUARDRAILS + HITL              │   │
│                            │           │ PII · injection · trust tiers  │   │
│  ┌─────────────────────────▼────────┐  │ approve/edit/reject/respond    │   │
│  │ PROTOCOLS                        │  │ checkpoints (resume button)    │   │
│  │ MCP server/client (JSON-RPC)     │  └───────────────────────────────┘   │
│  │ A2A: cards · tasks · discovery   │  ┌───────────────────────────────┐   │
│  │ Orchestrator: 4 topologies       │  │ EVALS + OBSERVABILITY         │   │
│  └──────────────────────────────────┘  │ rubric judge · trajectory      │   │
│  ┌──────────────────────────────────┐  │ golden sets · regression       │   │
│  │ MEMORY + AGENTIC RAG             │  │ OTel spans · JSONL · cost     │   │
│  │ working/episodic/semantic/vector │  └───────────────────────────────┘   │
│  │ curation · quarantine · persist  │                                      │
│  └──────────────────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌────────────────┐        ┌────────────────┐        ┌────────────────┐
│ PLANNING       │        │ WORKFLOWS      │        │ 15 SUB-AGENTS  │
│ 4 plan shapes  │        │ 5 patterns +   │        │ agents/ hub    │
│ retry→replan→  │        │ evaluator-opt  │        │ SKILL.md+core+ │
│ human ladder   │        │ handoffs       │        │ CLI, all green │
└────────────────┘        └────────────────┘        └────────────────┘
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/romangalaxys10-spec/ai-agent-architect.git
cd ai-agent-architect
pip install -e .

# Zero keys. Zero network. The full stack just runs:
python examples/full_stack_agent.py      # agent loop + RAG + HITL + budgets + evals + OTel
python examples/multi_agent_protocols.py # workflows + handoffs + A2A + MCP

make test                                # 183 tests, offline
```

### Run a real agent loop in 12 lines

```python
from core.llm import EchoProvider                     # or OpenAICompatibleProvider()
from core.agent_loop import AgentLoop
from core.tool_registry import ToolRegistry

registry = ToolRegistry()
registry.register("add", "Add two numbers", lambda a, b: a + b,
                  parameters_schema={"type": "object",
                                     "properties": {"a": {"type": "number"},
                                                    "b": {"type": "number"}},
                                     "required": ["a", "b"]})

result = AgentLoop(provider=EchoProvider(), registry=registry).run("compute 2+3")
print(result.stop_reason, result.total_tokens, result.final_answer)
```

### Serve your tools over MCP

```python
from core.mcp import MCPServer, MCPClient

server = MCPServer(registry)          # JSON-RPC 2.0: initialize/tools/list/tools/call
client = MCPClient(server)
client.connect()
tools = client.list_tools()
result = client.call_tool("add", {"a": 2, "b": 3})
```

### Expose an agent over A2A

```python
from core.a2a_protocol import AgentCard, A2AParticipant, A2ADiscovery, AgentSkill

card = AgentCard(name="research-agent", description="Deep research",
                 url="https://agents.internal/research",
                 skills=[AgentSkill(id="r", name="research", description="web research",
                                    tags=["research"])])
discovery = A2ADiscovery()
discovery.register(A2AParticipant(card, handler=lambda task: {"sources": [...]}))
matches = discovery.find_by_skill("research")   # skill-based discovery
```

### Switch to live models

```python
from core.llm import create_provider
provider = create_provider("openai")            # reads OPENAI_API_KEY / OPENAI_BASE_URL
# or: create_provider("anthropic")
# or route cheap→flagship automatically:
from core.llm import ModelRouter, EchoProvider
router = ModelRouter(provider, small_model="gpt-4o-mini", flagship_model="gpt-4o")
```

---

## 🧠 Cognitive Depth: Powered by Depth-Skills

Traditional models suffer from **Premature Closure** and **Pattern Gravity**. This framework embeds the 19 cognitive protocols from [`depth-skills`](https://github.com/Kshitijpalsinghtomar/depth-skills) — CONDUCTOR (complexity orchestration), DEEP-THINK (tri-angle activation), ADVERSARY (self-opposition), DIVERGE (contrarian paths), EXCAVATE (assumption archaeology), TEMPORAL (Day 1 vs Year 1) — wired into the master engine lifecycle and every sub-agent.

---

## 🏭 Agents Factory: 15 Complete Sub-Agents

Every agent ships **SKILL.md + core engine + CLI + tests** (enforced by `tests/test_subagent_completeness.py`, including a run-from-any-cwd contract):

| # | Agent | Domain |
|---|-------|--------|
| 1 | 🧠 `depth-conductor-agent` | Metacognition, anti-premature-closure audits |
| 2 | 🎨 `superdesign-agent` | Anti-AI-Slop design engine (sites, decks, HUDs) |
| 3 | 🍏 `steve-jobs-agent` | Focus filter, Rule of Three, binary verdicts |
| 4 | ⚡ `solana-stream-sentinel` | Yellowstone gRPC sniffer, DLMM decoder, MEV sim |
| 5 | 🛡️ `binary-reverse-sentinel` | Mach-O/iOS security scanner, credential hunter |
| 6 | 🎯 `linkedin-intent-sniper` | B2B buying-intent analysis, outreach |
| 7 | 🛰️ `discord-community-radar` | Dev-feed scanning, gig detection |
| 8 | ✍️ `anti-slop-content-engine` | Viral X threads, LinkedIn case studies |
| 9 | 🚀 `product-launch-orchestrator` | Show HN / PH / Reddit launch campaigns |
| 10 | 📬 `cold-outreach-dealflow` | Deliverability-safe email sequences, SOWs |
| 11 | 🎯 `career-hunter-orchestrator` | Job scout, ATS resumes, cover letters, CRM |
| 12 | 🧠 `model-bridge-router` | Multi-model routing, schema translation |
| 13 | 🧾 `invoice-billing-sentinel` | Multi-currency invoicing, timesheets |
| 14 | 🏛️ `senior-architect-agent` | Cognitive DAG decomposition, anti-pattern review |
| 15 | 🏭 `skill-factory-agent` | SKILL.md scaffolding, packaging, linting |

```bash
python cli/architect.py list-agents                    # browse the hub
python agents/depth-conductor-agent/cli/conductor.py --query "architect a DEX indexer"
python agents/senior-architect-agent/cli/architect.py --requirement "build an agent" --name Sys
python agents/skill-factory-agent/cli/factory.py lint --root .   # audit every SKILL.md
```

---

## 🛡️ Production Safety Stack

- **Budgets**: three non-convertible currencies (steps / tokens / wall-clock), *advertised to the model* (it paces itself) with a hard enforced ceiling as backstop.
- **Loop detection**: repetition / stagnation / cycling via canonicalized tool-call fingerprints (volatile keys stripped) with a graduated Inform → Constrain → Escalate ladder.
- **Guardrails**: input injection patterns, PII masking (email/card/SSN/phone/keys), output secret-leak blocking, tool-argument path-traversal & SSRF heuristics, untrusted-content delimiting, six trust tiers, OWASP LLM Top-10 checklist.
- **HITL**: allow/ask/deny rulesets with conditional predicates, approve/edit/reject/respond decisions, checkpoint store for resume, audit trail, fail-closed defaults.
- **Failure policies per tool**: compensate / reconcile / refuse — irreversible actions never auto-retry.
- **Idempotency ledger**: side-effecting calls replay cached results instead of double-firing.

## 📊 Evals & Observability

```python
from core.evaluation import AgentEvaluator, LLMAsJudge, GoldenDataset, RegressionGate, pass_at_k

report = AgentEvaluator.evaluate_run(agent_name="a", goal="g", final_output=..., turns=...,
                                     latency_ms=..., total_cost_usd=...)
# rubric judge + trajectory eval + deterministic checks → PRODUCTION_READY / NEEDS_REFINEMENT / FAILED
# evals/rubrics/*.json — versioned rubrics; evals/golden/ — smoke (every deploy) vs full (nightly)
```

```python
from core.observability import TelemetryTracer, JSONLLogger, CostLedger

tracer = TelemetryTracer("run")            # OTel-compatible export + PII redaction
logger = JSONLLogger("events.jsonl")        # structured events: llm_call/tool_call/hitl/guardrail
ledger = CostLedger()                      # per-model / per-agent USD accounting
```

---

## 📦 Project Layout

```
core/
├── llm/                    # providers, model router, retry+circuit breaker, structured output
├── agent_loop.py           # THE agent loop: tools, HITL, budgets, loop detection, stop conditions
├── workflows.py            # 5 Anthropic patterns (chain/route/parallel/orch/eval-opt)
├── handoffs.py             # transfer_to_X tools, input filters, audit trail
├── planning.py             # 4 plan shapes, retry→replan→human ladder, ReAct scaffold
├── reliability.py          # 3-currency budgets, loop detector, idempotency, failure policies
├── context_engineering.py  # compaction, note recitation, 4-block window
├── memory.py               # working/episodic/semantic + vector store + curation
├── rag.py                  # agentic RAG: retrieval tools, corrective grading, citations
├── guardrails.py           # PII, injection, trust tiers, delimiting, OWASP checklist
├── hitl.py                 # interrupts, approval rulesets, checkpoints
├── evaluation.py           # rubric judge, trajectory evals, golden sets, regression, pass^k
├── observability.py        # OTel spans, JSONL events, cost ledger, metrics
├── mcp.py                  # MCP JSON-RPC server + client + stdio transport
├── a2a_protocol.py         # Agent Cards, task lifecycle, discovery, message bus
├── orchestrator.py         # hierarchical / pipeline / mesh / blackboard
├── tool_registry.py        # schemas, validation pipeline, hooks, annotations
├── depth_cognitive_engine.py · steve_jobs_lens.py · engine.py · registry.py
agents/                     # 15 complete sub-agents (SKILL.md + core + cli)
factory/                    # skill builder, prompt synthesizer
evals/                      # versioned rubrics + golden datasets
examples/                   # end-to-end walkthroughs
tests/                      # 183 tests — all offline
docs/                       # compendium, patterns, product DNA, skill factory spec
```

## 🌍 Top-50 Demand-Driven Agent Suite (2026)

The 50 most-wanted, highest-searched agent capabilities — researched from global 2025–2026 demand data
(coding agents #1 search class, support automation = largest enterprise spend, sales agents $3.25B @ 44.7% CAGR,
deep research = fastest-growing term) — now shipped as first-class sub-agents:

**Coding & Dev (10)** · code-review-sentinel, test-forge-agent, bug-triage-agent, ci-surgeon-agent, refactor-pilot-agent, doc-scribe-agent, sast-sentinel-agent, dep-guardian-agent, migration-planner-agent, commit-crafter-agent

**Customer Support (5)** · ticket-router-agent, kb-curator-agent, escalation-shield-agent, voice-of-customer-agent, sla-sentinel-agent

**Sales & Marketing (7)** · lead-qualifier-agent, outreach-personalizer-agent, meeting-brief-agent, crm-hygiene-agent, competitor-radar-agent, seo-content-strategist-agent, ad-campaign-optimizer-agent

**Research & Analysis (5)** · deep-research-agent, data-analyst-agent, fact-check-agent, market-scout-agent, literature-review-agent

**Personal Productivity (5)** · email-triage-agent, calendar-architect-agent, meeting-scribe-agent, trip-compass-agent, deal-hunter-agent

**Finance (4)** · invoice-intake-agent, expense-auditor-agent, finstat-analyst-agent, portfolio-scout-agent

**HR & Recruiting (4)** · resume-screener-agent, interview-coach-agent, onboarding-guide-agent, culture-pulse-agent

**Content & Creative (4)** · content-calendar-agent, script-writer-agent, social-media-manager-agent, copy-editor-agent

**Ops, IT & Security (3)** · cloud-cost-optimizer-agent, incident-commander-agent, access-review-agent

**Education, Legal & Life (3)** · socratic-tutor-agent, language-coach-agent, contract-reviewer-agent

Every agent: offline-deterministic engine, argparse CLI (runs from any cwd), SKILL.md contract, and
functional smoke tests. Full catalog with per-agent tables: [`agents/AGENTS.md`](agents/AGENTS.md).
Test suite: `python -m pytest tests/test_top50_agents.py` (56 tests).

```bash
# try one:
python agents/sast-sentinel-agent/cli/sast_sentinel.py --code 'cursor.execute(f"SELECT * FROM t WHERE id={uid}")'
```

## 🧪 Testing & CI

```bash
make test       # 183 tests: providers, loop, HITL, budgets, RAG, MCP, A2A, evals...
make coverage   # line coverage for core/ + factory/
make smoke      # 5-second offline sanity check
make docker     # image with baked-in offline smoke gate
```

CI runs on every push: syntax compile → offline import smoke → Python 3.10/3.11/3.12 matrix with coverage → sub-agent CLI end-to-end job → MCP stdio protocol conformance.

## 🔧 Configuration

Copy `.env.example` → `.env`. Defaults are offline-safe: `AGENT_LLM_PROVIDER=echo`. Add `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` only when you want live models.

---

## 📄 License & Governance

MIT License — see [`LICENSE`](./LICENSE). Contributions follow [`CONTRIBUTING.md`](./CONTRIBUTING.md); report vulnerabilities per [`SECURITY.md`](./SECURITY.md); history in [`CHANGELOG.md`](./CHANGELOG.md).

**Depth-Skills cognitive protocols** — inspired by [depth-skills](https://github.com/Kshitijpalsinghtomar/depth-skills). **Steve Jobs Product DNA** — see [`docs/STEVE_JOBS_PRODUCT_DNA.md`](./docs/STEVE_JOBS_PRODUCT_DNA.md).

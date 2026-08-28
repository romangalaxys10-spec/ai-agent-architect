# 🤖 Sub-Agents Hub
### *Specialized Autonomous Sub-Agents Organized Under AI Agent Architect*

All specialized sub-agents are organized in this dedicated `agents/` directory. Each sub-agent is modular, self-contained, and dynamically discoverable by the master orchestrator.

---

## 🌟 Complete Sub-Agent Catalog

| Sub-Agent | Category | Description | Primary CLI | Location |
|---|---|---|---|---|
| 🎨 **`superdesign-agent`** | Design & UI/UX | 100% Credit-Free Anti-AI-Slop design engine for responsive websites, 16:9 keynote decks, and Teenage Engineering telemetry HUDs. | `superdesign` | [`agents/superdesign-agent/`](./superdesign-agent) |
| ⚡ **`solana-stream-sentinel`** | Web3 & On-Chain | Yellowstone Geyser gRPC real-time sniffer, Meteora DLMM / Raydium pool decoder, and MEV preflight simulator. | `python cli/sentinel.py` | [`agents/solana-stream-sentinel/`](./solana-stream-sentinel) |
| 🎯 **`career-hunter-orchestrator`** | Career & Leads | Headless job scout, ATS-optimized resume generator, bespoke cover letter engine, and lead CRM. | `python cli/career.py` | [`agents/career-hunter-orchestrator/`](./career-hunter-orchestrator) |
| 🧠 **`model-bridge-router`** | LLM Gateway | Adaptive multi-model router (GLM-4.7/5.3, Claude 3.7, Local) with unified tool schema translation and cost optimizer. | `python cli/bridge.py` | [`agents/model-bridge-router/`](./model-bridge-router) |
| 🛡️ **`binary-reverse-sentinel`** | Security & Reversing | Mach-O & iOS IPA security scanner, cloud credential leak hunter, and private API endpoint extractor. | `python cli/reverser.py` | [`agents/binary-reverse-sentinel/`](./binary-reverse-sentinel) |
| 🧾 **`invoice-billing-sentinel`** | Finance & Ops | Deterministic multi-currency invoice generator, timesheet tracker, and vector financial reports. | `python cli/billing.py` | [`agents/invoice-billing-sentinel/`](./invoice-billing-sentinel) |
| 🏛️ **`senior-architect-agent`** | Systems Architecture | Cognitive DAG state-machine design, modular decomposition, and zero-trust verification. | `agent-architect` | [`agents/senior-architect-agent/`](./senior-architect-agent) |
| 🍏 **`steve-jobs-agent`** | Product Taste | Enforces *Focus (Saying NO to 1,000 things)*, *The Whole Widget*, and binary quality verdicts. | `agent-architect review` | [`agents/steve-jobs-agent/`](./steve-jobs-agent) |
| 🏭 **`skill-factory-agent`** | Skill Scaffolding | Automated builder for universal `SKILL.md` packages with verification fixtures. | `agent-architect scaffold-skill` | [`agents/skill-factory-agent/`](./skill-factory-agent) |

---

## ⚡ CLI Hub Discovery

```bash
agent-architect list-agents
```

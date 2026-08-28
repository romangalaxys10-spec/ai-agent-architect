# 🤖 Sub-Agents Hub
### *Specialized Autonomous Sub-Agents Organized Under AI Agent Architect*

All specialized sub-agents are organized in this dedicated `agents/` directory. Each sub-agent is modular, self-contained, and dynamically discoverable by the master orchestrator.

---

## 🌟 Sub-Agent Catalog

| Sub-Agent | Category | Description | Location |
|---|---|---|---|
| 🎨 **`superdesign-agent`** | Frontend & UI/UX | 100% Credit-Free Anti-AI-Slop design engine for responsive websites, 16:9 keynote decks, and Teenage Engineering telemetry HUDs. | [`agents/superdesign-agent/`](./superdesign-agent) |
| 🏛️ **`senior-architect-agent`** | Systems Engineering | Decomposes complex goals into minimal DAGs, designs cognitive state machines, and enforces zero-trust modularity. | [`agents/senior-architect-agent/`](./senior-architect-agent) |
| 🍏 **`steve-jobs-agent`** | Product & Taste | Enforces *Focus (Saying NO to 1,000 things)*, *The Whole Widget*, and binary quality verdicts (`INSANELY_GREAT` vs `TOTAL_BULLSHIT`). | [`agents/steve-jobs-agent/`](./steve-jobs-agent) |
| 🏭 **`skill-factory-agent`** | Agent Engineering | Scaffolds hardened, production-grade `SKILL.md` packages with deterministic verification fixtures and prompt synthesizers. | [`agents/skill-factory-agent/`](./skill-factory-agent) |

---

## 🚀 How to Use Sub-Agents

### 1. List all Registered Sub-Agents via CLI
```bash
agent-architect list-agents
```

### 2. Invoke Sub-Agents Programmatically
```python
from core.registry import AgentRegistry

agents = AgentRegistry.discover_agents()
for agent_id, meta in agents.items():
    print(f"[{meta.id}] {meta.name} (v{meta.version}) -> {meta.description}")
```

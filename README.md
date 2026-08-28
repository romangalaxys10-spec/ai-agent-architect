# 🧠 AI Agent Architect
### *Create Your Powerful Agents — From Scratch to Maximum*

[![CI](https://github.com/romangalaxys10-spec/ai-agent-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/romangalaxys10-spec/ai-agent-architect/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Definitive](https://img.shields.io/badge/Architecture-Production--Grade-brightgreen.svg)]()
[![Steve Jobs DNA](https://img.shields.io/badge/Design-Insanely%20Great-black.svg)]()

> **"An AI Agent is not a chatbot with a system prompt. It is an autonomous cognitive engine built with uncompromising taste, radical focus, and resilient architecture."**

---

## 🌟 Overview

**AI Agent Architect** is a comprehensive, production-grade framework, cognitive engine, and skill factory designed to architect, scaffold, test, and deploy world-class autonomous agents and multi-agent swarms.

Born at the intersection of **Senior Systems Architecture**, **Skill Factory Engineering**, and the **Steve Jobs Product Philosophy**, this framework empowers developers to build agents that possess:
- **Radical Focus:** Saying *NO* to 1,000 superfluous features.
- **The Whole Widget:** End-to-end control from perception to execution sandboxes.
- **Zero Hedging:** Deterministic cognitive loops, verified tool execution, and defensive fallback trees.

---

## 🏛️ System Architecture

```
                               ┌────────────────────────────────┐
                               │       USER GOAL / INTENT       │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                               ┌────────────────────────────────┐
                               │       PERCEPTION ENGINE        │
                               │  (Context Hydration & State)   │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
      ┌─────────────────────┐  ┌────────────────────────────────┐  ┌─────────────────────┐
      │   WORKING MEMORY    │  │      REASONING & PLANNING      │  │   SEMANTIC MEMORY   │
      │ (Transient Scratch) │◄─┼► (Minimal Path Decomposition)  │◄─┼► (Facts & Knowledge)│
      └─────────────────────┘  └───────────────┬────────────────┘  └─────────────────────┘
                                               │
                                               ▼
                               ┌────────────────────────────────┐
                               │   TOOL & MCP EXECUTION LAYER   │
                               │ (Strict Schema & Type Safety)  │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                               ┌────────────────────────────────┐
                               │   SELF-CORRECTION & VERIFY     │
                               │  (Deterministic Fallbacks)     │
                               └───────────────┬────────────────┘
                                               │
                        ┌──────────────────────┴──────────────────────┐
                        ▼                                             ▼
             [VERIFICATION PASSED]                         [ANOMALY / RETRY]
        ┌──────────────────────────────┐              ┌──────────────────────────────┐
        │     MISSION ACCOMPLISHED     │              │     FALLBACK TREE RECOVERY   │
        └──────────────────────────────┘              └──────────────────────────────┘
```

---

## ✨ Core Pillars

### 1. Cognitive Engine (`core/engine.py`)
- Perception, planning, execution, and verification states.
- Built-in audit trail and duration telemetry.
- Fail-fast toggles and automated self-correction loops.

### 2. Steve Jobs Product Mindset (`core/steve_jobs_lens.py`)
- Evaluates agent designs and system architectures against the **6 Core Mental Models**:
  1. *Focus = Saying No to 1,000 Things*
  2. *The Whole Widget (End-to-End Vertical Control)*
  3. *Connecting the Dots*
  4. *The Death Filter (Essential vs. Superficial)*
  5. *Reality Distortion Field (Pushing Boundaries)*
  6. *Technology × Liberal Arts (Craft & Invisible Beauty)*
- Delivers binary verdicts: `INSANELY_GREAT` vs. `TOTAL_BULLSHIT`.

### 3. Multi-Agent Orchestration Topologies (`core/orchestrator.py`)
- **Hierarchical:** Supervisor agent coordinates specialized domain workers.
- **Pipeline:** Deterministic sequential hand-offs ($A \to B \to C$).
- **Mesh / Blackboard:** Distributed peer-to-peer event routing.

### 4. Memory Subsystem (`core/memory.py`)
- **Working Memory:** Fast in-flight key-value store.
- **Episodic Memory:** Immutable chronological event logs.
- **Semantic Memory:** Persistent facts, rules, and vector embeddings.

### 5. Agent & Skill Factory (`factory/`)
- Automated scaffolding of universal `SKILL.md` bundles with YAML frontmatter.
- Zero-hedging system prompt synthesis.
- Failure Mode & Fallback matrix generator.

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/romangalaxys10-spec/ai-agent-architect.git
cd ai-agent-architect
pip install -e .
```

### 2. Build Your First Autonomous Agent in 10 Lines

```python
from core.engine import AgentEngine
from core.memory import HierarchicalMemory
from core.tool_registry import ToolRegistry

# Initialize Memory and Tools
memory = HierarchicalMemory()
memory.semantic.store_fact("style_guide", "Strict type hints, PEP 8")

tools = ToolRegistry()
tools.register("audit_code", "Audits source files", lambda path: f"Audited {path}: 0 defects")

# Build Agent
agent = AgentEngine(name="CodeSentinel", system_prompt="You are a strict code auditor.")

# Run Autonomous Lifecycle
result = agent.run_lifecycle("Audit authentication module")
print(result)
```

---

## 🛠️ CLI Tools

`ai-agent-architect` includes a built-in CLI for scaffolding skills and running architectural reviews:

### Scaffold a New Agent Skill
```bash
agent-architect scaffold-skill --name solana-stream-decoder --description "Real-time Solana Geyser streaming and decoding"
```

### Run a Steve Jobs Product & Architecture Review
```bash
agent-architect review \
  --name "HyperAgent" \
  --pitch "Autonomous self-correcting deployment agent with zero configuration." \
  --features "One-click deploy, Self-healing DAG, Live telemetry, Social sharing, Unused RSS feed" \
  --steps 2
```

---

## 📚 Comprehensive Guides

Explore our in-depth architectural blueprints in the [`docs/`](./docs) directory:
- [📖 The Definitive AI Agent Guide](./docs/THE_DEFINITIVE_AGENT_GUIDE.md)
- [🍏 Steve Jobs Product DNA for Agents](./docs/STEVE_JOBS_PRODUCT_DNA.md)
- [🏭 Skill Factory Specification](./docs/SKILL_FACTORY_SPEC.md)
- [🕸️ Multi-Agent Topologies & Patterns](./docs/TOPOLOGIES_AND_PATTERNS.md)

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

All test suites verify:
- Agent state-machine transitions and verification loops.
- Hierarchical memory persistence and recall.
- Steve Jobs product filter heuristics and cut-lists.
- Skill factory markdown rendering and prompt synthesis.

---

## 🤝 Contributing

Contributions are welcome! Please ensure all new features include unit tests, maintain clean type signatures, and uphold the **Rule of Three & Radical Focus**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/InsanelyGreatFeature`)
3. Commit your Changes (`git commit -m 'Add InsanelyGreatFeature'`)
4. Push to the Branch (`git push origin feature/InsanelyGreatFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

<p align="center">
  <b>Built with taste, precision, and relentless standards by the AI Agent Architect.</b>
</p>

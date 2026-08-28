---
name: model-bridge-router
description: Multi-LLM model gateway and adaptive router for GLM-4.7/5.3, Claude 3.7, and local tiers with unified tool schema translation.
version: 1.0.0
author: AI Agent Architect
---

# Model Bridge Router Sub-Agent

> "Adaptive multi-LLM routing, cost-performance optimization, and unified tool schema mapping."

## 🎯 Activation Triggers
- `route model`
- `glm bridge`
- `optimize api cost`
- `convert tool schema`

## ⚡ Execution Protocol
1. **Task Salience Classification**: Estimate reasoning complexity, token budget, and code requirements.
2. **Dynamic Model Selection**: Route to the highest-efficiency model (GLM-4.7 for code, Claude for architecture, Local for bulk).
3. **Schema Normalization**: Translate function calling schemas between Anthropic and OpenAI/Z.AI standards.

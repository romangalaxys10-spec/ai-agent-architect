# syntax=docker/dockerfile:1
# AI Agent Architect — offline-capable runtime image.
# The framework runs with ZERO API keys (EchoProvider default); live keys are
# only needed when switching to openai/anthropic providers at runtime.

FROM python:3.11-slim AS base

WORKDIR /app

# Dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Framework + agents
COPY core/ ./core/
COPY factory/ ./factory/
COPY cli/ ./cli/
COPY agents/ ./agents/
COPY skills/ ./skills/
COPY tests/ ./tests/
COPY pyproject.toml README.md LICENSE ./

# Non-root user (least privilege doctrine)
RUN useradd -m agent && chown -R agent:agent /app
USER agent

# Offline smoke gate inside the image
RUN python -c "import sys; sys.path.insert(0, '.'); from core.llm import EchoProvider; from core.agent_loop import AgentLoop; from core.tool_registry import ToolRegistry; r = ToolRegistry(); r.register('ping', 'ping', lambda: 'pong'); assert AgentLoop(provider=EchoProvider(), registry=r).run('smoke').success"

# Expose the agent-card well-known port for A2A discovery (when serving)
EXPOSE 8080

# Default: run the full offline test suite
CMD ["python", "-m", "pytest", "tests/", "-q"]

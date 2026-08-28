.PHONY: install test test-fast coverage lint cli docker agents skills clean

install:            ## Install dependencies + package (editable)
	pip install -e .
	pip install pytest pytest-cov

test:               ## Full test suite (offline, zero API keys)
	python -m pytest tests/ -v

test-fast:          ## Quiet mode
	python -m pytest tests/ -q

coverage:           ## Coverage report for core + factory
	python -m pytest tests/ --cov=core --cov=factory --cov-report=term-missing

lint:               ## Syntax-compile every module
	python -m compileall -q core factory cli agents tests

cli:                ## Run the master CLI
	python cli/architect.py

agents:             ## List the sub-agents hub
	python cli/architect.py list-agents

skills:             ## Lint every SKILL.md for completeness
	python agents/skill-factory-agent/cli/factory.py lint --root .

docker:             ## Build the offline-capable image
	docker build -t ai-agent-architect:latest .

smoke:              ## Offline agent-loop smoke (no keys)
	python -c "import sys; sys.path.insert(0,'.'); from core.llm import EchoProvider; from core.agent_loop import AgentLoop; from core.tool_registry import ToolRegistry; r=ToolRegistry(); r.register('ping','ping',lambda:'pong'); res=AgentLoop(provider=EchoProvider(),registry=r).run('smoke'); print('smoke:', 'OK' if res.success else 'FAIL')"

clean:              ## Remove caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	rm -rf .pytest_cache .coverage

help:               ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

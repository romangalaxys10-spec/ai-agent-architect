"""
End-to-End Example: Multi-Agent Systems — workflows, handoffs, A2A + MCP protocol.

Demonstrates:
  1. The five Anthropic workflow patterns (chaining/routing/parallel/orch-workers/eval-opt)
  2. Handoffs between triage and specialists
  3. A2A: Agent Cards, task lifecycle, discovery
  4. MCP: serve the tool registry over JSON-RPC, consume from a client
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.a2a_protocol import A2ADiscovery, A2AParticipant, AgentCard, AgentSkill, TaskState
from core.handoffs import Handoff, HandoffRegistry, HandoffRequest, InputFilter
from core.llm.providers import EchoProvider
from core.mcp import MCPClient, MCPServer
from core.tool_registry import ToolRegistry
from core.workflows import (
    ChainStep, EvaluatorOptimizer, EvalScore, OrchestratorWorkers,
    Parallelization, PromptChain, Route, RouterWorkflow,
)


def demo_workflows():
    print("=== 1. THE FIVE WORKFLOW PATTERNS ===")
    provider = EchoProvider()

    # Prompt chaining with a gate
    chain = PromptChain(provider, [
        ChainStep(name="extract", prompt_template="Extract facts: {input}"),
        ChainStep(name="summarize", prompt_template="Summarize: {input}", gate=lambda out: len(out) > 10),
    ])
    run = chain.run("the quarterly report shows 40% growth")
    print(f"chain: {len(run.results)} steps -> {str(run.final_output)[:60]}")

    # Routing
    router = RouterWorkflow([
        Route(name="billing", condition=lambda t: "invoice" in t.lower(), handler=lambda t: " routed to billing"),
        Route(name="tech", condition=lambda t: "error" in t.lower() or "bug" in t.lower(), handler=lambda t: " routed to tech support"),
    ], default_handler=lambda t: " routed to general queue")
    print("routing:", router.run("I have a billing invoice question").final_output)
    print("routing:", router.run("there is an error in my deployment").final_output)

    # Parallelization: sectioning + voting
    par = Parallelization(provider)
    sec = par.section("review", ["security review: check auth", "perf review: check latency", "quality review: check tests"])
    print(f"sectioning: {len(sec.results) - 1} sections fanned out")
    vote = par.vote("is this design sound? answer yes or no", n=3)
    print(f"voting: consensus={vote.results[0].output['consensus']}")

    # Orchestrator-workers
    orch = OrchestratorWorkers(provider, worker=lambda sub: f"completed: {sub}")
    run = orch.run("refactor the authentication module and update tests")
    print(f"orchestrator-workers: {len(run.results)} phases -> {str(run.final_output)[:50]}")

    # Evaluator-optimizer
    def evaluator(task, output):
        passed = "verified" in output.lower()
        return EvalScore(score=0.9 if passed else 0.3, passed=passed,
                         feedback="add verification statement" if not passed else "good")

    eo = EvaluatorOptimizer(provider, evaluator, max_iterations=3)
    run = eo.run("produce a verified report")
    print(f"evaluator-optimizer: {len(run.results)} iterations -> {str(run.final_output)[:50]}")


def demo_handoffs():
    print("\n=== 2. HANDOFFS (triage -> specialist) ===")
    reg = HandoffRegistry()
    reg.add("triage", Handoff(
        destination="billing_specialist",
        description="Transfer billing and invoice issues",
        input_type={"type": "object", "properties": {"reason": {"type": "string"}}},
        input_filter=InputFilter(drop_tool_messages=True),
        on_handoff=lambda req: print(f"  on_handoff fired: {req.from_agent} -> {req.to_agent}"),
    ))
    print("  tool for the model:", reg.tool_declarations("triage")[0]["name"])
    result = reg.execute(HandoffRequest(
        from_agent="triage", to_agent="billing_specialist",
        input_data={"reason": "duplicate_charge"},
    ))
    print("  accepted:", result.accepted, "| audit:", reg.trail[-1]["input_keys"])


def demo_a2a():
    print("\n=== 3. A2A PROTOCOL (cards, tasks, discovery) ===")
    research_card = AgentCard(
        name="research-agent", description="Deep research and source synthesis",
        url="https://agents.internal/research",
        skills=[AgentSkill(id="res", name="research", description="web research", tags=["research", "analysis"])],
        capabilities={"streaming": True, "pushNotifications": False},
    )
    coding_card = AgentCard(
        name="coding-agent", description="Writes and reviews code",
        url="https://agents.internal/coding",
        skills=[AgentSkill(id="code", name="coding", description="implements features", tags=["code"])],
    )

    discovery = A2ADiscovery()
    discovery.register(A2AParticipant(research_card, handler=lambda task: {"sources": ["a", "b"], "summary": "found 2"}))
    discovery.register(A2AParticipant(coding_card, handler=lambda task: {"diff": "+42 -7"}))

    print("  discovery 'research' ->", [p.card.name for p in discovery.find_by_skill("research")])
    participant = discovery.find_by_url("https://agents.internal/research")
    print("  agent card well-known keys:", sorted(participant.well_known().keys()))

    task = participant.submit_task("research agentic memory architectures")
    participant.execute(task)
    print("  task state:", task.state.value, "| artifacts:", len(task.artifacts))


def demo_mcp():
    print("\n=== 4. MCP PROTOCOL (serve + consume) ===")
    registry = ToolRegistry()
    registry.register("add", "Add two numbers", lambda a, b: a + b, parameters_schema={
        "type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"],
    })
    registry.register("search_docs", "Search documentation", lambda query: f"results for {query}", parameters_schema={
        "type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"],
    })

    server = MCPServer(registry)
    client = MCPClient(server)
    info = client.connect()
    print("  handshake:", info["name"], "v" + info["version"], "| protocol:", server.handle({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}})["result"]["protocolVersion"])
    tools = client.list_tools()
    print("  tools/list:", [t["name"] for t in tools])
    result = client.call_tool("add", {"a": 19, "b": 23})
    print("  tools/call add(19,23):", result["content"][0]["text"], "| isError:", result["isError"])


if __name__ == "__main__":
    demo_workflows()
    demo_handoffs()
    demo_a2a()
    demo_mcp()
    print("\nAll multi-agent protocol demos completed (offline, zero keys).")

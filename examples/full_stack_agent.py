"""
End-to-End Example: The Complete Production Agent Stack (offline, zero API keys).

Runs the REAL agent loop with:
  tools + HITL approval gates + budgets + loop detection + context engineering
  + observability (OTel spans, JSONL events, cost ledger) + evaluation
  (rubric judge + trajectory eval).

Swap EchoProvider for OpenAICompatibleProvider/AnthropicProvider in production —
nothing else changes.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent_loop import AgentLoop
from core.context_engineering import ContextEngine
from core.evaluation import AgentEvaluator, LLMAsJudge, TrajectoryEvaluator
from core.hitl import ApprovalPolicy, ApprovalRule, Decision, HumanApprovalFlow
from core.llm.providers import ScriptedProvider
from core.observability import CostLedger, JSONLLogger, TelemetryTracer
from core.rag import AgenticRAG
from core.reliability import BudgetPortfolio, LoopDetector, TerminationCriteria
from core.tool_registry import ToolRegistry


def main():
    # 1. Knowledge base (agentic RAG)
    rag = AgenticRAG()
    rag.ingest(
        "The Yellowstone Geyser plugin streams Solana account updates over gRPC. "
        "Meteora DLMM pools emit swap events which the indexer decodes. "
        "The MEV preflight simulator models sandwich attack profitability.",
        source="docs",
    )

    # 2. Tools (validated, some approval-gated)
    registry = ToolRegistry()
    search_fn, store_fn = (lambda **kw: rag.as_tool_functions()["knowledge_search"](**kw)), None
    fns = rag.as_tool_functions()
    registry.register("knowledge_search", "Search the knowledge base", fns["knowledge_search"],
                      parameters_schema=rag.tool_declarations()[0]["parameters"])
    registry.register("knowledge_store", "Persist new knowledge", fns["knowledge_store"],
                      parameters_schema=rag.tool_declarations()[1]["parameters"])
    registry.register(
        "deploy_to_prod", "Deploy the service to production (irreversible)",
        lambda service: f"deployed {service}",
        is_safe=False, requires_approval=True, idempotent=False,
    )

    # 3. HITL: approve deploys except to 'prod-canary' which is allow-listed
    flow = HumanApprovalFlow(policy=ApprovalPolicy(default_mode="allow"))
    flow.policy.add_rule(ApprovalRule(
        tool_name="deploy_to_prod", mode="ask",
        when=lambda args: args.get("service") != "prod-canary",
    ))
    flow.set_resolver(lambda intr: Decision.APPROVE)

    # 4. Observability
    tracer = TelemetryTracer("example-trace")
    ledger = CostLedger()

    # 5. The loop with every subsystem wired
    script = [
        {"content": None, "tool_calls": [{"id": "c1", "name": "knowledge_search",
                                          "arguments": '{"query": "solana geyser streaming"}'}],
         "usage": {"prompt_tokens": 210, "completion_tokens": 30}},
        {"content": None, "tool_calls": [{"id": "c2", "name": "knowledge_store",
                                          "arguments": '{"text": "Geyser requires a paid RPC endpoint", "source": "agent"}'}],
         "usage": {"prompt_tokens": 400, "completion_tokens": 25}},
        {"content": "Research complete: geyser streams account updates over gRPC [docs::chunk0]; "
                    "stored the new fact about RPC endpoints. Deploying the indexer next.",
         "usage": {"prompt_tokens": 500, "completion_tokens": 60}},
    ]
    loop = AgentLoop(
        name="research-agent",
        system_prompt="You are a precise research agent. Cite sources. Verify before answering.",
        provider=ScriptedProvider(script),
        registry=registry,
        context_engine=ContextEngine(),
        budgets=BudgetPortfolio(max_steps=10, max_tokens=50_000, max_seconds=60),
        loop_detector=LoopDetector(),
        approval_flow=flow,
        tracer=tracer,
    )
    result = loop.run("Research Solana streaming and deploy the indexer to prod-canary")

    # 6. Metering
    ledger.record("scripted", "research-agent", result.total_tokens, 0, result.total_cost_usd)

    print("=" * 70)
    print("RUN:", result.run_id, "| stop:", result.stop_reason.value, "| success:", result.success)
    print("steps:", result.steps, "| tokens:", result.total_tokens, "| cost: $%.6f" % result.total_cost_usd)
    print("budgets:", {k: v["spent"] for k, v in result.artifacts["budgets"].items()})
    print("tool health:", result.artifacts["tool_health"])
    print("final answer:", (result.final_answer or "")[:200])
    print("=" * 70)

    # 7. Evaluation: rubric judge + trajectory
    report = AgentEvaluator.evaluate_run(
        agent_name="research-agent",
        goal="Research Solana streaming and deploy the indexer",
        final_output=result.final_answer or "",
        turns=[{"tool_calls": t.tool_calls, "tool_results": t.tool_results} for t in result.turns],
        latency_ms=result.wallclock_ms,
        total_cost_usd=result.total_cost_usd,
    )
    print("GRADE:", report.overall_grade)
    print("rubric:", report.rubric_scores)
    print("trajectory:", report.trajectory_finding)
    print("=" * 70)

    # 8. OTel export + cost report
    otel = tracer.export_otel()
    print(f"OTel spans exported: {len(otel)} (first: {otel[0]['name'] if otel else 'n/a'})")
    print("cost ledger:", ledger.report())
    print("audit trail (HITL):", flow.audit_trail)
    print("\nDone. Swap ScriptedProvider -> OpenAICompatibleProvider for live models.")


if __name__ == "__main__":
    main()

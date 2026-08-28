"""Tests: evaluation v2 (rubric judge, trajectory, golden datasets, regression, pass^k) + observability v2."""
import sys, os, json, tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.evaluation import (
    LLMAsJudge, TrajectoryEvaluator, GoldenDataset, RegressionGate, pass_at_k,
    AgentEvaluator, DEFAULT_RUBRIC, Rubric,
)
from core.observability import (
    TelemetryTracer, JSONLLogger, CostLedger, MetricsRegistry, new_correlation_id,
)


class TestLLMAsJudge(unittest.TestCase):
    def test_rubric_scores_all_criteria(self):
        judge = LLMAsJudge()
        judgment = judge.evaluate("analyze the data", "Analysis of the data with source [doc1] references and tool outputs.")
        self.assertEqual(set(judgment["scores"].keys()), {"task_completion", "groundedness", "tool_call_accuracy", "conciseness"})
        self.assertGreater(judgment["weighted_score"], 0.5)

    def test_empty_output_scores_low(self):
        judge = LLMAsJudge()
        judgment = judge.evaluate("task", "")
        self.assertLessEqual(judgment["weighted_score"], 0.4)

    def test_comparison_ranks_candidates(self):
        judge = LLMAsJudge()
        result = judge.evaluate_comparison("task", ["good detailed output with sources [1]", ""])
        self.assertEqual(result["ranking"][0], 0)

    def test_custom_rubric_from_dict(self):
        rubric = Rubric.from_dict({
            "name": "custom", "version": "2.1", "scale": 5,
            "criteria": [{"name": "accuracy", "description": "is accurate", "weight": 2.0}],
        })
        judge = LLMAsJudge(rubric=rubric)
        judgment = judge.evaluate("t", "accurate output about the task topic")
        self.assertIn("accuracy", judgment["scores"])


class TestTrajectoryEvaluator(unittest.TestCase):
    def test_clean_trajectory_optimal(self):
        turns = [{"tool_calls": [{"name": "search", "arguments": '{"q": 1}'}],
                  "tool_results": [{"tool": "search", "success": True}]}]
        finding = TrajectoryEvaluator().evaluate(turns)
        self.assertEqual(finding.verdict, "OPTIMAL")

    def test_repetition_flagged(self):
        turns = [{"tool_calls": [{"name": "t", "arguments": '{"q": 1}'}], "tool_results": [{"success": True}]}
                 for _ in range(4)]
        finding = TrajectoryEvaluator().evaluate(turns)
        self.assertIn(finding.verdict, ("SUBOPTIMAL", "ACCEPTABLE"))
        self.assertTrue(finding.loop_suspected)

    def test_mass_failure_is_failure(self):
        turns = [{"tool_calls": [{"name": "t", "arguments": "{}"}], "tool_results": [{"success": False}]}
                 for _ in range(4)]
        finding = TrajectoryEvaluator().evaluate(turns)
        self.assertEqual(finding.verdict, "FAILURE")


class TestGoldenAndRegression(unittest.TestCase):
    def test_golden_dataset_roundtrip(self):
        ds = GoldenDataset.from_dict({
            "name": "smoke", "tier": "smoke",
            "cases": [{"task": "compute 2+2", "expected_contains": ["4"], "expected_tools": ["calc"]}],
        })
        self.assertEqual(ds.tier, "smoke")
        self.assertEqual(ds.cases[0].task, "compute 2+2")
        out = ds.to_dict()
        self.assertEqual(out["cases"][0]["expected_contains"], ["4"])

    def test_regression_gate_blocks_drop(self):
        gate = RegressionGate(tolerance=0.05)
        result = gate.gate(
            baseline={"groundedness": 0.9, "tool_precision": 0.8},
            candidate={"groundedness": 0.6, "tool_precision": 0.82},
        )
        self.assertFalse(result["pass"])
        self.assertIn("groundedness", result["regressions"])

    def test_regression_gate_passes_small_delta(self):
        gate = RegressionGate(tolerance=0.05)
        result = gate.gate({"score": 0.9}, {"score": 0.88})
        self.assertTrue(result["pass"])

    def test_pass_at_k_consistency(self):
        self.assertEqual(pass_at_k([True, True, True], k=3), 1.0)
        self.assertEqual(pass_at_k([True, False, True], k=3), 0.0)  # single success proves nothing


class TestEvaluatorV2Pipeline(unittest.TestCase):
    def test_evaluate_run_full_pipeline(self):
        turns = [{"tool_calls": [{"name": "search", "arguments": '{"q": 1}'}],
                  "tool_results": [{"tool": "search", "success": True}]}]
        report = AgentEvaluator.evaluate_run(
            agent_name="test", goal="find answer", final_output="The answer with source [doc1].",
            turns=turns, latency_ms=120.0, total_cost_usd=0.001,
        )
        self.assertIn(report.overall_grade, ("PRODUCTION_READY", "NEEDS_REFINEMENT"))
        self.assertIsNotNone(report.rubric_scores)
        self.assertIn("Trajectory", [m.name for m in report.metrics])

    def test_legacy_api_still_works(self):
        report = AgentEvaluator.evaluate_trajectory(
            agent_name="legacy", user_goal="g",
            execution_steps=[{"step": 1, "tool_name": "t"}],
            final_output="a" * 40, latency_ms=100.0,
        )
        self.assertEqual(report.overall_grade, "PRODUCTION_READY")


class TestObservabilityV2(unittest.TestCase):
    def test_otel_export_shape(self):
        tracer = TelemetryTracer("T")
        span = tracer.start_span("llm.call", attributes={"model": "echo", "email": "user@corp.com"})
        tracer.end_span(span, extra_attributes={"tokens": 42})
        otel = tracer.export_otel()
        self.assertEqual(otel[0]["name"], "llm.call")
        self.assertEqual(otel[0]["traceId"], tracer.trace_id)
        self.assertIn("gen_ai.system", otel[0]["attributes"])
        self.assertNotIn("user@corp.com", str(otel[0]["attributes"]))  # redacted

    def test_flameview_and_save(self):
        tracer = TelemetryTracer("T")
        s1 = tracer.start_span("outer")
        s2 = tracer.start_span("inner", parent_id=s1)
        tracer.end_span(s2)
        tracer.end_span(s1)
        rows = tracer.export_flameview()
        self.assertEqual(len(rows), 2)
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "trace.json")
            tracer.save_otel(path)
            data = json.load(open(path))
            self.assertIn("resourceSpans", data)

    def test_jsonl_logger_events(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "events.jsonl")
            logger = JSONLLogger(path=path)
            logger.log_event("llm_call", model="echo", tokens=100, latency_ms=5.0)
            logger.log_event("tool_call", tool="search", email="a@b.co")
            logger.close()
            lines = [json.loads(l) for l in open(path)]
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[0]["type"], "llm_call")
            self.assertIn("@b.co", lines[1]["email"])  # PII masked in logs

    def test_cost_ledger_aggregates(self):
        ledger = CostLedger()
        ledger.record("echo-local", "agent-a", 100, 200, 0.0)
        ledger.record("gpt-4o", "agent-b", 1000, 500, 0.01)
        report = ledger.report()
        self.assertEqual(report["total_usd"], 0.01)
        self.assertIn("gpt-4o", report["by_model"])
        self.assertIn("agent-a", report["by_agent"])

    def test_metrics_registry_exposition(self):
        m = MetricsRegistry()
        m.inc("tool_calls_total")
        m.inc("tool_calls_total")
        m.gauge("active_runs", 3.0)
        m.observe("latency_ms", 12.5)
        text = m.exposition()
        self.assertIn("tool_calls_total 2.0", text)
        self.assertIn("active_runs 3.0", text)
        self.assertIn("latency_ms_p50", text)

    def test_correlation_ids_unique(self):
        ids = {new_correlation_id() for _ in range(100)}
        self.assertEqual(len(ids), 100)


if __name__ == "__main__":
    unittest.main()

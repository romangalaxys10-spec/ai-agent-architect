"""Tests: workflow patterns (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.llm.providers import EchoProvider
from core.workflows import (
    PromptChain, ChainStep, RouterWorkflow, Route, Parallelization,
    OrchestratorWorkers, EvaluatorOptimizer, EvalScore, PATTERN_SELECTION_GUIDE,
)


class TestPromptChain(unittest.TestCase):
    def test_chain_passes_outputs_forward(self):
        chain = PromptChain(EchoProvider(), [
            ChainStep(name="draft", prompt_template="Draft: {input}"),
            ChainStep(name="polish", prompt_template="Polish: {input}"),
        ])
        run = chain.run("the spec")
        self.assertEqual(len(run.results), 2)
        self.assertEqual(run.pattern, "prompt_chaining")

    def test_gate_stops_chain_early(self):
        chain = PromptChain(EchoProvider(), [
            ChainStep(name="check", prompt_template="{input}", gate=lambda out: False,
                      gate_failure_message="quality gate failed"),
            ChainStep(name="never", prompt_template="{input}"),
        ])
        run = chain.run("x")
        self.assertEqual(len(run.results), 1)
        self.assertIn("quality gate failed", run.final_output)


class TestRouter(unittest.TestCase):
    def test_routes_by_condition(self):
        routes = [
            Route(name="math", condition=lambda t: any(c in t for c in "+-*/"), handler=lambda t: f"computed {t}"),
            Route(name="greeting", condition=lambda t: "hello" in t.lower(), handler=lambda t: "greeted"),
        ]
        router = RouterWorkflow(routes, default_handler=lambda t: "defaulted")
        self.assertEqual(router.run("2 + 2").final_output, "computed 2 + 2")
        self.assertEqual(router.run("hello there").final_output, "greeted")
        self.assertEqual(router.run("mystery").final_output, "defaulted")


class TestParallelization(unittest.TestCase):
    def test_sectioning_fans_out(self):
        par = Parallelization(EchoProvider())
        run = par.section("analyze", ["check safety of: a", "check safety of: b", "check safety of: c"])
        self.assertEqual(run.pattern, "parallelization.sectioning")
        self.assertEqual(len(run.results), 4)  # fanout + 3 sections

    def test_voting_majority_wins(self):
        par = Parallelization(EchoProvider())
        run = par.vote("is this safe?", n=3, threshold=0.5)
        # Echo is deterministic: all agree -> consensus
        self.assertTrue(run.results[0].output["consensus"])


class TestOrchestratorWorkers(unittest.TestCase):
    def test_dynamic_decomposition_and_synthesis(self):
        orch = OrchestratorWorkers(
            EchoProvider(),
            worker=lambda sub: f"done: {sub}",
        )
        run = orch.run("research and build the dashboard")
        self.assertEqual(run.pattern, "orchestrator_workers")
        self.assertGreaterEqual(len(run.results), 2)  # decompose + >=1 worker + synthesize


class TestEvaluatorOptimizer(unittest.TestCase):
    def test_refinement_loop_passes_when_good(self):
        def evaluator(task, output):
            good = "FINAL" in output
            return EvalScore(score=0.95 if good else 0.3, passed=good,
                             feedback="add FINAL marker" if not good else "ok")

        # Scripted: first output lacks marker, second has it
        from core.llm.providers import ScriptedProvider
        provider = ScriptedProvider([
            {"content": "draft without marker"},
            {"content": "polished output FINAL"},
        ])
        eo = EvaluatorOptimizer(provider, evaluator, max_iterations=3)
        run = eo.run("produce final doc")
        self.assertIn("FINAL", run.final_output)
        self.assertEqual(len(run.results), 2)

    def test_exhaustion_accepts_best(self):
        def strict(task, output):
            return EvalScore(score=0.2, passed=False, feedback="never good enough")

        eo = EvaluatorOptimizer(EchoProvider(), strict, max_iterations=2)
        run = eo.run("impossible task")
        self.assertIsNotNone(run.final_output)

    def test_exhaustion_can_ask_human(self):
        def strict(task, output):
            return EvalScore(score=0.1, passed=False, feedback="no")

        eo = EvaluatorOptimizer(EchoProvider(), strict, max_iterations=1, on_exhausted="ask_human")
        run = eo.run("impossible")
        self.assertTrue(run.final_output["needs_human_review"])


class TestSelectionGuide(unittest.TestCase):
    def test_guide_covers_all_patterns(self):
        for key in ("prompt_chaining", "routing", "orchestrator_workers", "evaluator_optimizer", "agent_loop"):
            self.assertIn(key, PATTERN_SELECTION_GUIDE)


if __name__ == "__main__":
    unittest.main()

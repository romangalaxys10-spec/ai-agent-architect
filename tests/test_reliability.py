"""Tests: reliability kit (budgets, loop detection, idempotency, failure policies)."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.reliability import (
    Budget, BudgetPortfolio, BudgetExceededError, LoopDetector,
    IdempotencyLedger, FailurePolicy, FailurePolicyEngine, TerminationCriteria,
    canonicalize_call,
)


class TestBudgets(unittest.TestCase):
    def test_three_currencies_exist(self):
        p = BudgetPortfolio(max_steps=10, max_tokens=1000, max_seconds=60)
        summary = p.summary()
        self.assertIn("steps", summary)
        self.assertIn("tokens", summary)
        self.assertIn("seconds", summary)

    def test_advertised_below_enforced(self):
        p = BudgetPortfolio(max_steps=10)
        b = p._budgets["steps"]
        self.assertLess(b.advertised, b.enforced)

    def test_budget_exceeds_raises(self):
        b = Budget("tokens", advertised=80, enforced=100)
        with self.assertRaises(BudgetExceededError):
            b.spend(101)
        self.assertTrue(b.exceeded)

    def test_advertised_prompt_fragment_tells_model(self):
        p = BudgetPortfolio(max_steps=10, max_tokens=5000, max_seconds=100)
        frag = p.advertised_prompt_fragment()
        self.assertIn("Budget", frag)
        self.assertIn("steps", frag)


class TestLoopDetector(unittest.TestCase):
    def test_repetition_detected(self):
        d = LoopDetector(repeat_threshold=3)
        for _ in range(3):
            d.observe("search", {"q": "same"})
        v = d.verdict()
        self.assertIsNotNone(v)
        self.assertIn(v["level"], ("inform", "constrain", "escalate"))

    def test_stagnation_escalates_even_with_repetition(self):
        d = LoopDetector(repeat_threshold=3, stagnation_limit=5)
        for _ in range(6):
            d.observe("search", {"q": "same"})
        v = d.verdict()
        self.assertEqual(v["level"], "escalate")

    def test_cycling_detected(self):
        d = LoopDetector()
        d.observe("a", {})
        d.observe("b", {})
        d.observe("a", {})
        d.observe("b", {})
        v = d.verdict()
        self.assertEqual(v["level"], "constrain")

    def test_canonicalization_strips_volatile_keys(self):
        f1 = canonicalize_call("t", {"q": "x", "timestamp": 1})
        f2 = canonicalize_call("t", {"q": "x", "timestamp": 999})
        self.assertEqual(f1, f2)

    def test_progress_notes_reset_stagnation(self):
        d = LoopDetector(stagnation_limit=4)
        for i in range(6):
            d.observe("t", {"n": i})  # distinct calls: no repetition/cycling
            d.note_progress()
        self.assertIsNone(d.verdict())


class TestIdempotency(unittest.TestCase):
    def test_same_call_replays_cached(self):
        ledger = IdempotencyLedger()
        k = ledger.key("send_email", {"to": "a@b.c"})
        self.assertFalse(ledger.seen(k))
        ledger.record(k, "sent:123")
        self.assertTrue(ledger.seen(k))
        self.assertEqual(ledger.cached(k), "sent:123")


class TestFailurePolicies(unittest.TestCase):
    def test_compensate_runs_inverse(self):
        engine = FailurePolicyEngine()
        compensated = []
        engine.register("charge", FailurePolicy.COMPENSATE, compensator=lambda args: compensated.append(args))
        f = engine.handle("charge", "payment gateway timeout", {"amount": 100})
        self.assertEqual(f.policy, FailurePolicy.COMPENSATE)
        self.assertEqual(compensated, [{"amount": 100}])
        self.assertIn("compensation executed", f.action_taken)

    def test_refuse_escalates_by_default(self):
        engine = FailurePolicyEngine()
        f = engine.handle("unknown_tool", "exploded", {})
        self.assertEqual(f.policy, FailurePolicy.REFUSE)
        self.assertIn("escalated", f.action_taken)

    def test_reconcile_reads_world_state(self):
        engine = FailurePolicyEngine()
        engine.register("sync", FailurePolicy.RECONCILE, reconciler=lambda: {"state": "consistent"})
        f = engine.handle("sync", "partial write", {})
        self.assertIn("reconciled", f.action_taken)


class TestTermination(unittest.TestCase):
    def test_success_predicate(self):
        t = TerminationCriteria(success_predicate=lambda: False)
        self.assertIsNone(t.evaluate())
        t2 = TerminationCriteria(success_predicate=lambda: True)
        self.assertEqual(t2.evaluate(), "success")


if __name__ == "__main__":
    unittest.main()

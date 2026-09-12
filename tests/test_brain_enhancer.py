"""Unit tests for GVS5H Brain Enhancer Engine and brain-enhancer-agent"""

import unittest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.brain_enhancer import BrainEnhancerEngine, ProblemSpec
from core.registry import AgentRegistry


class TestBrainEnhancer(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_workspace_initialization(self):
        state = BrainEnhancerEngine.initialize_workspace(self.test_dir, "Find optimal path in DAG")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "task.md")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "plan.md")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "notes.md")))
        self.assertEqual(state.task_desc, "Find optimal path in DAG")

    def test_run_sample_tests_passing(self):
        code = "import sys\nprint(int(sys.stdin.read().strip()) * 2)"
        tests = [{"input": "5\n", "expected": "10"}, {"input": "21\n", "expected": "42"}]
        res = BrainEnhancerEngine.run_sample_tests(code, tests)
        self.assertTrue(res["ran"])
        self.assertEqual(res["passed"], 2)
        self.assertIn("PASSED", res["feedback"])

    def test_run_sample_tests_failing(self):
        code = "import sys\nprint(int(sys.stdin.read().strip()) + 1)"
        tests = [{"input": "5\n", "expected": "10"}]
        res = BrainEnhancerEngine.run_sample_tests(code, tests)
        self.assertTrue(res["ran"])
        self.assertEqual(res["passed"], 0)
        self.assertIn("FAILED", res["feedback"])
        self.assertIn("switch to a DIFFERENT", res["feedback"])

    def test_prompt_synthesis_constraints(self):
        p_ideate = BrainEnhancerEngine.synthesize_gvs5h_prompt("ideation", "Hard task")
        self.assertIn("Do NOT solve the problem and do NOT write any code", p_ideate)
        self.assertIn("SEVERAL DISTINCT candidate approaches", p_ideate)

        p_manage = BrainEnhancerEngine.synthesize_gvs5h_prompt("primary_manage", "Hard task")
        self.assertIn("DIFFERENT approach", p_manage)

    def test_agent_registry_discovery(self):
        agents = AgentRegistry.discover_agents()
        self.assertIn("brain-enhancer-agent", agents)
        meta = agents["brain-enhancer-agent"]
        self.assertIn("brain-enhancer", meta.name.lower())


if __name__ == "__main__":
    unittest.main()

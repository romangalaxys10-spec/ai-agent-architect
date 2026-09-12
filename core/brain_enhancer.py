"""
GVS5H Brain Enhancer: Ledger-Based Zero-Shot Self-Orchestration Engine.
Boosts LLM reasoning, algorithmic precision, and problem-solving accuracy (+23.2% on hard benchmarks)
via fresh-context decomposition, shared filesystem ledgers, and empirical sample verification.

Based on GVS5H: "Five Qwen3.8-27B Models Match Claude Fable 5 on LiveCodeBench Hard"
"""

import os
import re
import json
import time
import hashlib
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Callable


@dataclass
class ProblemSpec:
    kind: str = "code"  # "code" or "math"
    solver_system: str = "an expert algorithmist, competitive programmer, and systems architect."
    max_iters: int = 6
    max_notes_chars: int = 4000
    timeout_seconds: int = 10


@dataclass
class LedgerState:
    workspace_path: str
    task_desc: str
    plan: str = ""
    notes: str = ""
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    current_solution: str = ""
    iteration: int = 0
    status: str = "continue"
    sample_test_verdict: str = ""


class BrainEnhancerEngine:
    """
    Implements GVS5H Ledger-Based Self-Orchestration:
    1. Primary Plan (Decomposition into concrete units of work)
    2. Ideation Worker (Pure prose, distinct algorithmic approaches, NO premature code)
    3. Primary Manage (Task curation, anti-fixation approach switching)
    4. Worker Execution (Living notes compaction, fresh solution generation)
    5. Empirical Ground-Truth Testing (Execution against test cases)
    """

    @staticmethod
    def initialize_workspace(ws_dir: str, task_text: str) -> LedgerState:
        os.makedirs(ws_dir, exist_ok=True)
        files = ["task.md", "plan.md", "notes.md", "tasks.json", "solution.py", "transcript.jsonl"]
        for f in files:
            p = os.path.join(ws_dir, f)
            if not os.path.exists(p):
                with open(p, "w", encoding="utf-8") as fp:
                    fp.write("")
        
        with open(os.path.join(ws_dir, "task.md"), "w", encoding="utf-8") as fp:
            fp.write(task_text)
            
        return LedgerState(workspace_path=ws_dir, task_desc=task_text)

    @classmethod
    def run_sample_tests(cls, code_str: str, test_cases: List[Dict[str, str]], timeout: int = 10) -> Dict[str, Any]:
        """Runs candidate python code against sample test cases to provide ground truth feedback."""
        if not code_str.strip() or not test_cases:
            return {"ran": False, "passed": 0, "total": 0, "feedback": ""}

        passed = 0
        first_fail = None

        for idx, tc in enumerate(test_cases):
            inp = tc.get("input", "")
            expected = tc.get("expected", "").strip()
            try:
                proc = subprocess.run(
                    [sys.executable, "-c", code_str],
                    input=inp,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                got = proc.stdout.strip()
                if proc.returncode != 0 and not got:
                    got = f"<runtime error: {proc.stderr[:200]}>"
            except subprocess.TimeoutExpired:
                got = "<timed out (>10s)>"
            except Exception as e:
                got = f"<execution error: {e}>"

            if got == expected:
                passed += 1
            elif first_fail is None:
                first_fail = {
                    "test_index": idx + 1,
                    "input": inp[:300],
                    "expected": expected[:200],
                    "got": got[:200]
                }

        total = len(test_cases)
        if passed == total:
            feedback = f"[SAMPLE TESTS: PASSED all {total} public test cases -- solution is empirically verified.]"
        else:
            ff = first_fail or {}
            feedback = (
                f"[SAMPLE TESTS: FAILED -- passed {passed}/{total}. The solution is WRONG. "
                f"Failing case #{ff.get('test_index')}: input={ff.get('input')!r} "
                f"expected={ff.get('expected')!r} got={ff.get('got')!r}. "
                f"Fix the bug or switch to a DIFFERENT algorithmic approach.]"
            )

        return {
            "ran": True,
            "passed": passed,
            "total": total,
            "fail": first_fail,
            "feedback": feedback
        }

    @classmethod
    def synthesize_gvs5h_prompt(cls, role: str, task: str, plan: str = "", notes: str = "", current_work: str = "", last_summary: str = "") -> str:
        """Constructs GVS5H cognitive prompts enforcing zero-shot self-orchestration and anti-fixation."""
        if role == "primary_plan":
            return (
                "You are the PRIMARY orchestrator of a team of expert computer scientists and algorithmists.\n"
                "Given the problem, produce a short overarching plan and a task list of concrete units of work.\n"
                "Respond with EXACTLY:\n"
                "### PLAN\n<3-6 sentence strategy>\n"
                "### TASKS\n<3-6 bullet tasks, each a concrete unit of work>"
            )
        elif role == "ideation":
            return (
                "You are the FIRST WORKER. Do NOT solve the problem and do NOT write any code.\n"
                "Identify the core difficulty, then list SEVERAL DISTINCT candidate approaches "
                "(genuinely different algorithms / data structures / reductions, not variations of one idea), "
                "and note pitfalls for each in prose only. Absolutely no code blocks.\n"
                "Respond with EXACTLY:\n"
                "### NOTES\n<your analysis of core bottleneck and invariants>\n"
                "### NEXT\n<bullet list of distinct approaches to try next>"
            )
        elif role == "primary_manage":
            return (
                "You are the PRIMARY manager. You OWN the task list and decide when the problem is solved.\n"
                "- If the LATEST WORKER RESULT includes a failing test verdict, you MUST set STATUS 'continue'.\n"
                "- IMPORTANT: If the current solution keeps failing, do NOT polish the stuck idea. Switch to a DIFFERENT approach.\n"
                "Respond with EXACTLY:\n"
                "### STATUS\n<done|continue>\n"
                "### NEXT\n<exact text of the ONE task to do next>\n"
                "### TASKS\n<curated task list>"
            )
        elif role == "worker":
            return (
                "You are a WORKER subagent. Build on current work and notes where useful.\n"
                "If your task is to try a different approach, write a FRESH solution instead of patching the stuck one.\n"
                "Respond with EXACTLY:\n"
                "### CODE\n```python\n<full updated self-contained program>\n```\n"
                "### NOTES\n<compacted bullet notes under 800 words replacing old notes>\n"
                "### NEXT\n<bullet list of remaining checks>\n"
                "### STATUS\n<solved|continue>"
            )
        return ""

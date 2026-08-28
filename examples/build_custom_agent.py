import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
Example: Building a Custom Autonomous Code Reviewer Agent from Scratch.
"""

from core.engine import AgentEngine, ExecutionStep
from core.memory import HierarchicalMemory
from core.tool_registry import ToolRegistry


def run_code_review():
    print("🚀 Initializing Custom Code Reviewer Agent...")
    
    # 1. Setup Memory
    memory = HierarchicalMemory()
    memory.semantic.store_fact("python_style", "PEP 8 compliant, type hints required, zero unused imports")
    
    # 2. Setup Tools
    tools = ToolRegistry()
    tools.register("inspect_syntax", "Checks AST syntax", lambda code: f"AST valid for {len(code)} bytes")
    tools.register("lint_code", "Lints Python code", lambda code: "0 errors, 0 warnings")
    
    # 3. Initialize Agent Engine
    agent = AgentEngine(
        name="NexusCodeReviewer",
        system_prompt="You are a strict, uncompromising code review agent. Identify bugs, security leaks, and style violations.",
        fail_fast=True
    )
    
    # 4. Run Lifecycle
    goal = "Audit authentication middleware module"
    result = agent.run_lifecycle(goal, executor=lambda step: f"Completed {step.action} using {step.tool_name}")
    
    print("\n✅ Execution Result:")
    print(f"Agent: {result['agent']}")
    print(f"Goal: {result['goal']}")
    print(f"State: {result['state']}")
    print(f"Total Time: {result['total_time_ms']:.2f} ms")


if __name__ == "__main__":
    run_code_review()

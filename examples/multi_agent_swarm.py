import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
Example: Multi-Agent Hierarchical Team (Supervisor + Specialized Workers).
"""

from core.orchestrator import MultiAgentOrchestrator, OrchestrationTopology


def run_swarm():
    print("🐝 Initializing Multi-Agent Orchestrator (Hierarchical Topology)...")
    
    orchestrator = MultiAgentOrchestrator(topology=OrchestrationTopology.HIERARCHICAL)
    
    # Register agents
    orchestrator.register_agent(
        name="LeadArchitect",
        role="supervisor",
        skills=["system_design", "task_delegation"]
    )
    
    orchestrator.register_agent(
        name="SecOpsSpecialist",
        role="security_auditor",
        skills=["vulnerability_scan", "secret_detection"],
        handler=lambda payload: {"status": "clean", "threat_score": 0.0, "checked_files": payload.get("files", [])}
    )
    
    orchestrator.register_agent(
        name="PerformanceOptimizer",
        role="perf_engineer",
        skills=["profiling", "caching"],
        handler=lambda payload: {"status": "optimized", "speedup_estimate": "3.4x"}
    )
    
    # Run Orchestrator
    goal = "Deploy high-frequency trading smart contract"
    payload = {"files": ["main.rs", "state.rs", "vault.rs"]}
    
    response = orchestrator.run(goal, payload)
    print("\n📊 Swarm Execution Summary:")
    print(f"Supervisor Goal: {response['supervisor_goal']}")
    print(f"Worker Output: {response['worker_results']}")


if __name__ == "__main__":
    run_swarm()

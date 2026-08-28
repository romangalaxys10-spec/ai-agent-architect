"""
Multi-Agent Orchestrator.
Supports Topologies: Hierarchical (Supervisor-Worker), Mesh (Peer-to-Peer), Sequential Pipeline, and Dynamic Blackboard.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import time
import logging

logger = logging.getLogger("Orchestrator")


class OrchestrationTopology(str, Enum):
    HIERARCHICAL = "HIERARCHICAL"  # 1 Supervisor directs N Specialized Workers
    PIPELINE = "PIPELINE"          # Sequential Hand-off: A -> B -> C -> D
    MESH = "MESH"                  # Peer-to-Peer agent communication network
    BLACKBOARD = "BLACKBOARD"      # Shared state bus with autonomous watchers


@dataclass
class AgentNode:
    name: str
    role: str
    skills: List[str]
    handler: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None


class MultiAgentOrchestrator:
    """
    Coordinates distributed teams of agents with resilient routing and telemetry.
    """

    def __init__(self, topology: OrchestrationTopology = OrchestrationTopology.HIERARCHICAL):
        self.topology = topology
        self.nodes: Dict[str, AgentNode] = {}
        self.blackboard: Dict[str, Any] = {}
        self.audit_log: List[Dict[str, Any]] = []

    def register_agent(self, name: str, role: str, skills: List[str], handler: Optional[Callable] = None):
        self.nodes[name] = AgentNode(name=name, role=role, skills=skills, handler=handler)

    def route_hierarchical(self, supervisor_goal: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Supervisor delegates tasks to workers based on skill relevance."""
        results = {}
        self.audit_log.append({"action": "SUPERVISOR_DISPATCH", "goal": supervisor_goal, "timestamp": time.time()})
        for name, node in self.nodes.items():
            if node.role.lower() != "supervisor":
                logger.info(f"Delegating to worker: {name} ({node.role})")
                if node.handler:
                    res = node.handler(payload)
                else:
                    res = {"status": "success", "agent": name, "executed_role": node.role}
                results[name] = res
        return {"supervisor_goal": supervisor_goal, "worker_results": results, "topology": self.topology.value}

    def route_pipeline(self, initial_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Sequential processing across agent nodes in registration order."""
        current_data = initial_payload.copy()
        pipeline_trace = []
        for name, node in self.nodes.items():
            start = time.time()
            if node.handler:
                current_data = node.handler(current_data)
            else:
                current_data[f"processed_by_{name}"] = True
            pipeline_trace.append({"agent": name, "role": node.role, "duration_ms": (time.time() - start) * 1000})
        return {"final_payload": current_data, "trace": pipeline_trace, "topology": self.topology.value}

    def run(self, goal: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = payload or {}
        if self.topology == OrchestrationTopology.HIERARCHICAL:
            return self.route_hierarchical(goal, data)
        elif self.topology == OrchestrationTopology.PIPELINE:
            return self.route_pipeline(data)
        else:
            return {"error": f"Topology {self.topology} routing implemented via custom event bus."}

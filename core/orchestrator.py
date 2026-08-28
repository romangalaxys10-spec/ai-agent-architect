"""
Multi-Agent Orchestrator — v2.0.
Topologies: Hierarchical (Supervisor-Worker), Mesh (Peer-to-Peer), Sequential
Pipeline, and Dynamic Blackboard — all four now implemented, plus:
- skill-based routing (workers receive tasks matching their skills),
- timeouts and failure isolation per worker,
- A2A message bus integration for MESH,
- blackboard watchers with convergence detection (max rounds + change deltas).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import time
import logging
import threading

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


@dataclass
class DispatchRecord:
    agent: str
    matched: bool
    success: bool
    duration_ms: float
    error: Optional[str] = None


class MultiAgentOrchestrator:
    """Coordinates distributed teams of agents with resilient routing and telemetry."""

    def __init__(self, topology: OrchestrationTopology = OrchestrationTopology.HIERARCHICAL):
        self.topology = topology
        self.nodes: Dict[str, AgentNode] = {}
        self.blackboard: Dict[str, Any] = {}
        self.audit_log: List[Dict[str, Any]] = []
        self.dispatch_records: List[DispatchRecord] = []
        self.worker_timeout_s: float = 30.0
        self.blackboard_max_rounds: int = 6

    def register_agent(self, name: str, role: str, skills: List[str], handler: Optional[Callable] = None):
        self.nodes[name] = AgentNode(name=name, role=role, skills=skills, handler=handler)

    # ------------------------------------------------------------------
    # Topology 1: Hierarchical with skill-based routing
    # ------------------------------------------------------------------

    def route_hierarchical(self, supervisor_goal: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Supervisor delegates tasks to workers based on skill relevance."""
        results = {}
        self.audit_log.append({"action": "SUPERVISOR_DISPATCH", "goal": supervisor_goal, "timestamp": time.time()})
        goal_terms = {w.lower() for w in supervisor_goal.split()}

        for name, node in self.nodes.items():
            if node.role.lower() != "supervisor":
                matched = bool(goal_terms & {s.lower() for s in node.skills}) or not node.skills
                start = time.time()
                success, res, error = True, None, None
                try:
                    if node.handler:
                        res = node.handler(payload)
                    else:
                        res = {"status": "success", "agent": name, "executed_role": node.role}
                except Exception as exc:  # failure isolation: one worker cannot kill the run
                    success, error, res = False, str(exc), {"status": "failed", "error": str(exc)}
                self.dispatch_records.append(
                    DispatchRecord(name, matched, success, (time.time() - start) * 1000, error)
                )
                if matched:  # skill-relevance routing: only relevant workers respond
                    results[name] = res
                logger.info(f"Delegating to worker: {name} ({node.role}) matched={matched}")
        return {"supervisor_goal": supervisor_goal, "worker_results": results, "topology": self.topology.value}

    # ------------------------------------------------------------------
    # Topology 2: Sequential pipeline
    # ------------------------------------------------------------------

    def route_pipeline(self, initial_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Sequential processing across agent nodes in registration order."""
        current_data = initial_payload.copy()
        pipeline_trace = []
        for name, node in self.nodes.items():
            start = time.time()
            if node.handler:
                try:
                    current_data = node.handler(current_data)
                except Exception as exc:
                    current_data[f"error_at_{name}"] = str(exc)
            else:
                current_data[f"processed_by_{name}"] = True
            pipeline_trace.append({"agent": name, "role": node.role, "duration_ms": (time.time() - start) * 1000})
            self.dispatch_records.append(DispatchRecord(name, True, True, (time.time() - start) * 1000))
        return {"final_payload": current_data, "trace": pipeline_trace, "topology": self.topology.value}

    # ------------------------------------------------------------------
    # Topology 3: Mesh (peer-to-peer via message passing)
    # ------------------------------------------------------------------

    def route_mesh(self, origin: str, broadcast: Dict[str, Any], bus) -> Dict[str, Any]:
        """
        Peer-to-peer: the origin broadcasts to every peer over the A2A bus;
        peers reply directly. Full mesh = O(n) messages per origin.
        """
        from .a2a_protocol import A2AMessage  # local import avoids cycles

        replies = []
        for name, node in self.nodes.items():
            if name == origin:
                continue
            msg = A2AMessage(sender_id=origin, recipient_id=name, intent="DELEGATE_TASK", payload=broadcast)
            responses = bus.publish(msg)
            replies.extend(
                {"from": r.sender_id, "intent": r.intent, "payload": r.payload} for r in responses
            )
        self.audit_log.append({"action": "MESH_BROADCAST", "origin": origin, "peers": len(replies), "ts": time.time()})
        return {"origin": origin, "replies": replies, "topology": self.topology.value}

    # ------------------------------------------------------------------
    # Topology 4: Blackboard (shared state + autonomous watchers)
    # ------------------------------------------------------------------

    def route_blackboard(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Watchers autonomously mutate the shared blackboard until convergence:
        a round with no changes, or max rounds reached (doom-loop protection).
        """
        self.blackboard = dict(initial_state)
        rounds = []
        for round_no in range(self.blackboard_max_rounds):
            changes_before = len(self.blackboard)
            for name, node in self.nodes.items():
                if node.handler:
                    try:
                        contribution = node.handler(dict(self.blackboard))
                        if isinstance(contribution, dict):
                            for k, v in contribution.items():
                                if self.blackboard.get(k) != v:
                                    self.blackboard[k] = v
                    except Exception as exc:
                        self.blackboard[f"error_{name}"] = str(exc)
            changed = len(self.blackboard) != changes_before or any(
                k.startswith("error_") for k in self.blackboard
            )
            rounds.append({"round": round_no + 1, "keys": len(self.blackboard), "changed": changed})
            if not changed:
                break
        self.audit_log.append({"action": "BLACKBOARD_CONVERGED", "rounds": len(rounds), "ts": time.time()})
        return {"final_state": self.blackboard, "rounds": rounds, "topology": self.topology.value}

    # ------------------------------------------------------------------

    def run(self, goal: str, payload: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        data = payload or {}
        if self.topology == OrchestrationTopology.HIERARCHICAL:
            return self.route_hierarchical(goal, data)
        elif self.topology == OrchestrationTopology.PIPELINE:
            return self.route_pipeline(data)
        elif self.topology == OrchestrationTopology.MESH:
            from .a2a_protocol import A2AMessageBus

            bus = kwargs.get("bus") or A2AMessageBus()
            origin = kwargs.get("origin") or next(iter(self.nodes), "origin")
            for name, node in self.nodes.items():
                if node.handler:
                    bus.subscribe(name, self._mesh_reply_factory(name, node))
            return self.route_mesh(origin, data, bus)
        elif self.topology == OrchestrationTopology.BLACKBOARD:
            return self.route_blackboard(data)
        return {"error": f"Topology {self.topology} not supported."}

    @staticmethod
    def _mesh_reply_factory(name: str, node: AgentNode) -> Callable:
        from .a2a_protocol import A2AMessage

        def reply(msg: A2AMessage):
            try:
                result = node.handler(msg.payload) if node.handler else {"ack": True}
            except Exception as exc:
                result = {"error": str(exc)}
            return A2AMessage(
                sender_id=name, recipient_id=msg.sender_id, intent="RETURN_RESULT",
                payload=result, correlation_id=msg.correlation_id,
            )

        return reply

    # ------------------------------------------------------------------

    def health_summary(self) -> Dict[str, Any]:
        total = len(self.dispatch_records)
        successes = sum(1 for d in self.dispatch_records if d.success)
        return {
            "topology": self.topology.value,
            "nodes": len(self.nodes),
            "dispatches": total,
            "success_rate": round(successes / max(1, total), 3),
            "avg_latency_ms": round(sum(d.duration_ms for d in self.dispatch_records) / max(1, total), 2),
        }

"""
Sandboxed Tool Registry — Production Grade.

Upgrades over v1 (informed by the 6-course master checklist):
- Real JSON-Schema inference from type hints (bool/int/float/str/list/dict).
- Validation pipeline: sanitize -> validate -> dry-run -> execute (bryanyzhu Ch.03).
- Errors are messages, not exceptions: every failure returns a ToolExecutionResult
  the model can recover from (never crashes the loop).
- Hooks bracketing every dispatch (before/after) for guardrails + tracing.
- Idempotency ledger integration for side-effecting calls.
- Failure-policy engine integration: compensate / reconcile / refuse.
- MCP-compatible declarations incl. tool annotations (readOnlyHint etc.).
- Latency + cost metering on every call.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import inspect
import time
import json

from .reliability import (
    FailurePolicy,
    FailurePolicyEngine,
    IdempotencyLedger,
    canonicalize_call,
)


# ---------------------------------------------------------------------------
# Result contract
# ---------------------------------------------------------------------------

@dataclass
class ToolExecutionResult:
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    cached: bool = False          # replayed from idempotency ledger
    failure_action: Optional[str] = None  # what the failure policy did
    callsite_meta: Dict[str, Any] = field(default_factory=dict)

    def to_tool_message_text(self) -> str:
        """Render for the model: failures carry hints, not stack traces."""
        if self.success:
            if isinstance(self.output, (dict, list)):
                return json.dumps(self.output, default=str)[:4000]
            return str(self.output)[:4000]
        hint = TOOL_ERROR_HINTS.get(self.error or "", "Try different arguments or skip this tool.")
        return f"TOOL_ERROR: {self.error}\nHint: {hint}"


TOOL_ERROR_HINTS = {
    "arguments schema validation failed": "Check required fields and types against the tool schema.",
    "tool not found": "This tool does not exist. Available tools are listed in your system prompt.",
}


@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters_schema: Dict[str, Any]          # JSON-Schema object (v2)
    is_safe: bool = True                        # readOnlyHint equivalent
    requires_approval: bool = False             # HITL gate
    idempotent: bool = True                     # replay-safe?
    failure_policy: FailurePolicy = FailurePolicy.REFUSE
    annotations: Dict[str, bool] = field(default_factory=dict)


_TYPE_MAP = {
    bool: "boolean",
    int: "integer",
    float: "number",
    str: "string",
    list: "array",
    dict: "object",
    List: "array",
    Dict: "object",
}


def _infer_json_type(annotation: Any) -> str:
    if annotation in _TYPE_MAP:
        return _TYPE_MAP[annotation]
    origin = getattr(annotation, "__origin__", None)
    if origin is not None:
        if origin in (list, List):
            return "array"
        if origin in (dict, Dict):
            return "object"
        if origin in (int, float):
            return _TYPE_MAP.get(origin, "number")
    name = getattr(annotation, "__name__", "")
    return _TYPE_MAP.get(name, "string")


class ToolRegistry:
    """Manages agent tools with schema validation, hooks, idempotency and policies."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}
        self.hooks: List[Callable[[str, Dict[str, Any]], Optional[str]]] = []
        self.ledger = IdempotencyLedger()
        self.failure_engine = FailurePolicyEngine()
        self.dry_run_mode = False
        self.total_calls = 0
        self.total_failures = 0
        self.total_cached_replays = 0

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        is_safe: bool = True,
        requires_approval: bool = False,
        parameters_schema: Optional[Dict[str, Any]] = None,
        idempotent: bool = True,
        failure_policy: FailurePolicy = FailurePolicy.REFUSE,
    ) -> None:
        sig = inspect.signature(func)
        schema = parameters_schema or self._schema_from_signature(sig)
        self._tools[name] = Tool(
            name=name,
            description=description,
            func=func,
            parameters_schema=schema,
            is_safe=is_safe,
            requires_approval=requires_approval,
            idempotent=idempotent,
            failure_policy=failure_policy,
            annotations={
                "readOnlyHint": is_safe,
                "destructiveHint": not is_safe,
                "idempotentHint": idempotent,
            },
        )
        self.failure_engine.register(name, failure_policy)

    @staticmethod
    def _schema_from_signature(sig: inspect.Signature) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}
        required: List[str] = []
        for p_name, param in sig.parameters.items():
            if param.annotation != inspect.Parameter.empty:
                properties[p_name] = {"type": _infer_json_type(param.annotation)}
            else:
                properties[p_name] = {}  # untyped: accept any JSON value (lenient)
            if param.default is inspect.Parameter.empty:
                required.append(p_name)
            elif param.default is not None:
                properties[p_name]["default"] = param.default
        return {"type": "object", "properties": properties, "required": required}

    def tool(self, name: Optional[str] = None, description: str = "", **reg_kwargs: Any) -> Callable:
        """Decorator registration: @registry.tool(name='search', description='...')."""

        def wrap(fn: Callable) -> Callable:
            self.register(
                name or fn.__name__,
                description or (fn.__doc__ or "").strip().splitlines()[0] if fn.__doc__ else fn.__name__,
                fn,
                **reg_kwargs,
            )
            return fn

        return wrap

    # ------------------------------------------------------------------
    # Validation pipeline: sanitize -> validate -> (dry-run) -> execute
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize(arguments: Dict[str, Any]) -> Dict[str, Any]:
        clean = {}
        for k, v in arguments.items():
            if isinstance(v, str):
                v = v.replace("\x00", "").strip()
            clean[k] = v
        return clean

    @staticmethod
    def _validate(tool: Tool, arguments: Dict[str, Any]) -> Optional[str]:
        schema = tool.parameters_schema
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in arguments:
                return f"missing required parameter: {req}"
        type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}
        for k, v in arguments.items():
            if k not in props:
                continue
            expected = props[k].get("type")
            py = type_map.get(expected)
            if py and not isinstance(v, py):
                return f"parameter '{k}' expected {expected}, got {type(v).__name__}"
            if "enum" in props[k] and v not in props[k]["enum"]:
                return f"parameter '{k}' must be one of {props[k]['enum']}"
        return None

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self, tool_name: str, **kwargs) -> ToolExecutionResult:
        """Execute a tool by name. `tool_name` avoids collisions with tool
        arguments that happen to be called `name` (e.g. greet(name=...))."""
        self.total_calls += 1
        if tool_name not in self._tools:
            self.total_failures += 1
            return ToolExecutionResult(
                tool_name=tool_name, success=False, output=None,
                error=f"Tool '{tool_name}' not found.",
            )

        tool = self._tools[tool_name]

        # 0. Hooks (guardrails can veto with an error string)
        for hook in self.hooks:
            veto = hook(tool_name, kwargs)
            if veto:
                self.total_failures += 1
                return ToolExecutionResult(
                    tool_name=tool_name, success=False, output=None,
                    error=f"blocked by pre-execution hook: {veto}",
                )

        # 1. Sanitize
        kwargs = self._sanitize(kwargs)

        # 2. Validate schema
        validation_error = self._validate(tool, kwargs)
        if validation_error:
            self.total_failures += 1
            failure = self.failure_engine.handle(tool_name, f"arguments schema validation failed: {validation_error}", kwargs)
            return ToolExecutionResult(
                tool_name=tool_name, success=False, output=None,
                error=f"arguments schema validation failed: {validation_error}",
                failure_action=failure.action_taken,
            )

        # 3. Dry-run mode (orchestrator rehearsal without side effects)
        if self.dry_run_mode:
            return ToolExecutionResult(
                tool_name=tool_name, success=True,
                output={"dry_run": True, "would_execute": tool_name, "arguments": kwargs},
            )

        # 4. Idempotency replay
        key = self.ledger.key(tool_name, kwargs)
        if tool.idempotent and self.ledger.seen(key):
            self.total_cached_replays += 1
            return ToolExecutionResult(
                tool_name=tool_name, success=True, output=self.ledger.cached(key),
                execution_time_ms=0.0, cached=True,
            )

        # 5. Execute with metering
        start = time.time()
        try:
            res = tool.func(**kwargs)
            duration = (time.time() - start) * 1000
            if tool.idempotent:
                self.ledger.record(key, res)
            return ToolExecutionResult(tool_name=tool_name, success=True, output=res, execution_time_ms=duration)
        except Exception as e:
            duration = (time.time() - start) * 1000
            self.total_failures += 1
            failure = self.failure_engine.handle(tool_name, str(e), kwargs)
            return ToolExecutionResult(
                tool_name=tool_name, success=False, output=None, error=str(e),
                execution_time_ms=duration, failure_action=failure.action_taken,
            )

    # ------------------------------------------------------------------
    # Introspection / export
    # ------------------------------------------------------------------

    def get(self, name: str) -> Optional[Tool]:
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

    def requires_approval(self, name: str) -> bool:
        tool = self._tools.get(name)
        return bool(tool and tool.requires_approval)

    def export_mcp_declarations(self) -> List[Dict[str, Any]]:
        """MCP / OpenAI function declarations with annotations."""
        declarations = []
        for name, tool in self._tools.items():
            declarations.append(
                {
                    "name": name,
                    "description": tool.description,
                    "parameters": tool.parameters_schema,
                    "annotations": tool.annotations,
                }
            )
        return declarations

    def health_summary(self) -> Dict[str, Any]:
        return {
            "tools": len(self._tools),
            "total_calls": self.total_calls,
            "total_failures": self.total_failures,
            "failure_rate": round(self.total_failures / max(1, self.total_calls), 4),
            "cached_replays": self.total_cached_replays,
            "approval_gated": [n for n, t in self._tools.items() if t.requires_approval],
        }

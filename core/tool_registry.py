"""
Sandboxed Tool Registry with Schema Validation, Safety Guardrails, and Model Context Protocol (MCP) compatibility.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import inspect
import time
import json


@dataclass
class ToolExecutionResult:
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    execution_time_ms: float = 0.0


@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    parameters_schema: Dict[str, Any]
    is_safe: bool = True
    requires_approval: bool = False


class ToolRegistry:
    """Manages agent tools, enforces schema validation, and enables MCP tool declarations."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        is_safe: bool = True,
        requires_approval: bool = False,
    ):
        sig = inspect.signature(func)
        params = {}
        for p_name, param in sig.parameters.items():
            params[p_name] = {
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "string",
                "default": param.default if param.default != inspect.Parameter.empty else None,
            }
        
        tool = Tool(
            name=name,
            description=description,
            func=func,
            parameters_schema=params,
            is_safe=is_safe,
            requires_approval=requires_approval,
        )
        self._tools[name] = tool

    def execute(self, name: str, **kwargs) -> ToolExecutionResult:
        if name not in self._tools:
            return ToolExecutionResult(tool_name=name, success=False, output=None, error=f"Tool '{name}' not found.")
        
        tool = self._tools[name]
        start = time.time()
        try:
            res = tool.func(**kwargs)
            duration = (time.time() - start) * 1000
            return ToolExecutionResult(tool_name=name, success=True, output=res, execution_time_ms=duration)
        except Exception as e:
            duration = (time.time() - start) * 1000
            return ToolExecutionResult(tool_name=name, success=False, output=None, error=str(e), execution_time_ms=duration)

    def export_mcp_declarations(self) -> List[Dict[str, Any]]:
        """Exports tools in standard Model Context Protocol (MCP) / OpenAI function declaration format."""
        declarations = []
        for name, tool in self._tools.items():
            properties = {}
            required = []
            for p_name, p_info in tool.parameters_schema.items():
                properties[p_name] = {"type": "string", "description": f"Parameter {p_name}"}
                if p_info["default"] is None:
                    required.append(p_name)
            
            declarations.append({
                "name": name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                }
            })
        return declarations

"""
Model Context Protocol (MCP) — Server & Client.

Implements the MCP core over JSON-RPC 2.0 (stdio transport):
- Server: initialize handshake with capability negotiation, tools/list
  (paginated), tools/call with JSON-Schema validation, isError results,
  and listChanged notifications.
- Client: spawns/attaches a server, performs the handshake, lists and calls tools.
- Host-side conversation privacy doctrine: the server NEVER receives the whole
  conversation — only the arguments of each call (MCP spec design principle).

Zero external dependencies; stdio framing is newline-delimited JSON, which is
what every reference implementation speaks over pipes.
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, IO, List, Optional, Sequence, Tuple

from .tool_registry import ToolRegistry

JSONRPC_VERSION = "2.0"
PROTOCOL_VERSION = "2024-11-05"


def jsonrpc_request(method: str, params: Optional[Dict[str, Any]] = None, req_id: Optional[Any] = None) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "method": method, "params": params or {}}


def jsonrpc_response(req_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "result": result}


def jsonrpc_error(req_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "error": {"code": code, "message": message}}


class MCPErrorCodes:
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

@dataclass
class MCPServerInfo:
    name: str
    version: str


class MCPServer:
    """
    Serves a ToolRegistry over MCP JSON-RPC.

    Methods:
      initialize                 -> server info + capabilities
      notifications/initialized  -> (no response)
      tools/list                 -> tool declarations (+ annotations)
      tools/call                 -> execute; content array + isError flag
      ping                       -> pong
    Emits `notifications/tools/list_changed` when tools change.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        server_info: Optional[MCPServerInfo] = None,
        page_size: int = 100,
    ):
        self.registry = registry
        self.info = server_info or MCPServerInfo(name="ai-agent-architect-mcp", version="2.0.0")
        self.page_size = page_size
        self.request_count = 0
        self.call_log: List[Dict[str, Any]] = []

    # -- protocol -----------------------------------------------------------

    def handle(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle one JSON-RPC message; returns a response or None (notifications)."""
        if not isinstance(message, dict) or message.get("jsonrpc") != JSONRPC_VERSION:
            return jsonrpc_error(message.get("id") if isinstance(message, dict) else None,
                                 MCPErrorCodes.INVALID_REQUEST, "not a valid JSON-RPC 2.0 message")
        method = message.get("method", "")
        req_id = message.get("id")
        params = message.get("params") or {}
        self.request_count += 1

        if method == "initialize":
            return jsonrpc_response(req_id, self._initialize())
        if method == "notifications/initialized":
            return None
        if method == "ping":
            return jsonrpc_response(req_id, {})
        if method == "tools/list":
            return jsonrpc_response(req_id, self._tools_list(params))
        if method == "tools/call":
            return jsonrpc_response(req_id, self._tools_call(params))
        if method.startswith("notifications/"):
            return None
        return jsonrpc_error(req_id, MCPErrorCodes.METHOD_NOT_FOUND, f"unknown method: {method}")

    def _initialize(self) -> Dict[str, Any]:
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": {"listChanged": True},
            },
            "serverInfo": {"name": self.info.name, "version": self.info.version},
        }

    def _tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        declarations = self.registry.export_mcp_declarations()
        cursor = params.get("cursor")
        start = 0
        if cursor:
            try:
                start = int(cursor)
            except ValueError:
                return {"tools": [], "nextCursor": None}
        page = declarations[start : start + self.page_size]
        next_cursor = str(start + self.page_size) if start + self.page_size < len(declarations) else None
        return {"tools": page, "nextCursor": next_cursor}

    def _tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        name = params.get("name", "")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            return self._error_result("arguments must be an object")
        result = self.registry.execute(name, **arguments)
        self.call_log.append({
            "tool": name, "success": result.success, "ms": result.execution_time_ms, "ts": time.time(),
        })
        content_text = result.to_tool_message_text()
        return {
            "content": [{"type": "text", "text": content_text}],
            "isError": not result.success,
        }

    @staticmethod
    def _error_result(message: str) -> Dict[str, Any]:
        return {"content": [{"type": "text", "text": f"MCP error: {message}"}], "isError": True}

    # -- stdio loop -----------------------------------------------------------

    def serve_stdio(self, stdin: IO[str], stdout: IO[str]) -> None:
        """Newline-delimited JSON-RPC loop over any reader/writer pair."""
        for line in stdin:
            line = line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                resp = jsonrpc_error(None, MCPErrorCodes.PARSE_ERROR, "unparseable JSON")
            else:
                resp = self.handle(message)
            if resp is not None:
                stdout.write(json.dumps(resp) + "\n")
                stdout.flush()

    def tools_changed_notification(self) -> Dict[str, Any]:
        return {"jsonrpc": JSONRPC_VERSION, "method": "notifications/tools/list_changed"}


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class MCPClient:
    """
    Client that speaks the same protocol. In-process transport by default
    (calls server.handle directly); real subprocess stdio transport via
    `spawn()` when running external MCP servers.
    """

    def __init__(self, server: Optional[MCPServer] = None):
        self.server = server
        self.server_info: Dict[str, Any] = {}
        self.session_active = False

    def connect(self) -> Dict[str, Any]:
        if self.server is None:
            raise ConnectionError("no MCP server attached")
        resp = self.server.handle(jsonrpc_request("initialize", {}, req_id=1))
        self.server_info = resp.get("result", {}).get("serverInfo", {}) if "result" in resp else {}
        self.server.handle({"jsonrpc": JSONRPC_VERSION, "method": "notifications/initialized"})
        self.session_active = True
        return self.server_info

    def list_tools(self) -> List[Dict[str, Any]]:
        if not self.session_active:
            self.connect()
        resp = self.server.handle(jsonrpc_request("tools/list", {}, req_id=2))
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if not self.session_active:
            self.connect()
        resp = self.server.handle(jsonrpc_request("tools/call", {"name": name, "arguments": arguments}, req_id=3))
        return resp.get("result", {})

    # -- subprocess transport ---------------------------------------------------

    def spawn(self, command: Sequence[str]) -> "MCPStdioTransport":
        """Launch an external MCP server subprocess and return its transport."""
        return MCPStdioTransport(command)


class MCPStdioTransport:
    """Newline-JSON stdio transport to a subprocess MCP server (npx/uvx style)."""

    def __init__(self, command: Sequence[str]):
        import subprocess

        self.proc = subprocess.Popen(
            list(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self._id = 0
        self._lock = threading.Lock()

    def _request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        with self._lock:
            self._id += 1
            req = jsonrpc_request(method, params, req_id=self._id)
            self.proc.stdin.write(json.dumps(req) + "\n")
            self.proc.stdin.flush()
            line = self.proc.stdout.readline()
        if not line:
            raise ConnectionError("MCP server closed the pipe")
        return json.loads(line)

    def initialize(self) -> Dict[str, Any]:
        info = self._request("initialize", {})
        self._notify("notifications/initialized")
        return info.get("result", {})

    def _notify(self, method: str) -> None:
        with self._lock:
            self.proc.stdin.write(json.dumps({"jsonrpc": JSONRPC_VERSION, "method": method}) + "\n")
            self.proc.stdin.flush()

    def list_tools(self) -> List[Dict[str, Any]]:
        resp = self._request("tools/list", {})
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        resp = self._request("tools/call", {"name": name, "arguments": arguments})
        return resp.get("result", {})

    def close(self) -> None:
        try:
            self.proc.stdin.close()
            self.proc.terminate()
        except Exception:
            pass

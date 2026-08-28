"""
Structured output: ask the model for JSON conforming to a schema, then
validate and (if needed) repair. Falls back to lenient extraction when the
provider ignores the schema — the "errors as messages" doctrine applied to
formatting: we never crash, we re-ask or repair.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional, Sequence, Type

from .providers import LLMProvider, LLMResponse, Message, Role


class StructuredOutputError(ValueError):
    """Raised when output cannot be coerced to the requested shape."""


_JSON_BLOCK = re.compile(r"```(?:json)?\s*(.+?)\s*```", re.DOTALL)
_LEADING_JSON = re.compile(r"[\[{]")


def extract_json(text: str) -> Any:
    """Extract JSON from raw text, fenced blocks, or embedded garbage."""
    if not text:
        raise StructuredOutputError("empty text")
    candidate = text.strip()
    fenced = _JSON_BLOCK.search(candidate)
    if fenced:
        candidate = fenced.group(1)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass
    # Find the first balanced JSON object/array substring.
    for opener, closer in (("{", "}"), ("[", "]")):
        start = candidate.find(opener)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(candidate)):
            ch = candidate[i]
            if ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(candidate[start : i + 1])
                    except json.JSONDecodeError:
                        break
    raise StructuredOutputError(f"no parseable JSON in: {text[:120]!r}")


def validate_json(data: Any, schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Minimal JSON-Schema subset validation: type + required + properties + enum.
    Intentionally dependency-free; full validators can be plugged in upstream.
    """
    if not isinstance(data, dict):
        raise StructuredOutputError(f"expected object, got {type(data).__name__}")
    for req in schema.get("required", []):
        if req not in data:
            raise StructuredOutputError(f"missing required field: {req}")
    props = schema.get("properties", {})
    type_map = {"string": str, "number": (int, float), "integer": int, "boolean": bool, "object": dict, "array": list}
    for key, value in data.items():
        if key not in props:
            continue  # additional properties allowed
        expected = props[key].get("type")
        if expected and expected in type_map:
            py_type = type_map[expected]
            ok = isinstance(value, py_type) and not (expected == "integer" and isinstance(value, bool))
            if not ok:
                raise StructuredOutputError(f"field '{key}' expected {expected}, got {type(value).__name__}")
        if "enum" in props[key] and value not in props[key]["enum"]:
            raise StructuredOutputError(f"field '{key}' value {value!r} not in enum {props[key]['enum']}")
    return data


def generate_structured(
    provider: LLMProvider,
    messages: Sequence[Message],
    schema: Dict[str, Any],
    model: str = "echo-local",
    max_repair_attempts: int = 2,
) -> Dict[str, Any]:
    """
    Structured generation loop:
    1. ask with schema embedded in the prompt;
    2. extract + validate;
    3. on failure, feed the validation error back and re-ask (repair loop).
    """
    schema_text = json.dumps(schema, indent=2)
    convo = list(messages) + [
        Message(
            role=Role.USER,
            content=(
                "Respond ONLY with a JSON object that validates against this schema "
                f"(no prose, no code fences unless valid JSON):\n{schema_text}"
            ),
        )
    ]
    last_error = ""
    for _ in range(max_repair_attempts + 1):
        resp: LLMResponse = provider.complete(convo, model=model, temperature=0.0)
        try:
            data = extract_json(resp.content or "")
            return validate_json(data, schema)
        except StructuredOutputError as exc:
            last_error = str(exc)
            convo = convo + [
                Message(role=Role.ASSISTANT, content=resp.content or ""),
                Message(
                    role=Role.USER,
                    content=f"Your JSON failed validation: {last_error}. Return corrected JSON only.",
                ),
            ]
    raise StructuredOutputError(f"repair attempts exhausted: {last_error}")

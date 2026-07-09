"""
Tool execution engine.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from typing import Any

from ..tools.registry import TOOL_IMPLS


@dataclass(slots=True)
class ToolExecutionResult:
    """
    Result of executing a tool.
    """

    tool_name: str
    success: bool
    output: str
    tool_call_id: str | None = None


class ToolExecutor:
    """
    Executes tool calls.

    This class has NO knowledge of the UI.
    It simply executes tools and returns results.
    """

    def execute(
        self,
        tool_call: dict[str, Any],
    ) -> ToolExecutionResult:

        function = tool_call.get("function", {})

        tool_name = function.get("name", "")

        raw_arguments = function.get("arguments", {})

        tool_call_id = tool_call.get("id")

        arguments = self._parse_arguments(raw_arguments)

        tool = TOOL_IMPLS.get(tool_name)

        if tool is None:

            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                output=f"Unknown tool: {tool_name}",
                tool_call_id=tool_call_id,
            )

        try:

            result = tool(arguments)

            return ToolExecutionResult(
                tool_name=tool_name,
                success=True,
                output=str(result),
                tool_call_id=tool_call_id,
            )

        except Exception as exc:

            return ToolExecutionResult(
                tool_name=tool_name,
                success=False,
                output=str(exc),
                tool_call_id=tool_call_id,
            )

    def execute_all(
        self,
        tool_calls: list[dict[str, Any]],
    ) -> list[ToolExecutionResult]:

        results: list[ToolExecutionResult] = []

        for tool_call in tool_calls:
            results.append(self.execute(tool_call))

        return results

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _parse_arguments(
        self,
        raw: Any,
    ) -> dict[str, Any]:

        if isinstance(raw, dict):
            return raw

        if raw is None:
            return {}

        if isinstance(raw, str):

            try:
                return json.loads(raw)

            except Exception:
                pass

            try:
                return ast.literal_eval(raw)

            except Exception:
                pass

        return {}
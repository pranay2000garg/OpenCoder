"""
Tool execution engine.

The ToolExecutor is responsible for:

- Looking up tool implementations
- Executing tools
- Handling exceptions
- Returning normalized tool results

The Agent should never execute tools directly.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from typing import Any

from ..tools.registry import TOOL_IMPLS


@dataclass
class ToolExecutionResult:
    """
    Normalized result returned by a tool execution.
    """

    tool_name: str
    output: str
    success: bool
    tool_call_id: str | None = None


class ToolExecutor:
    """
    Executes tool calls emitted by the language model.
    """

    def execute(self, tool_call: dict[str, Any]) -> ToolExecutionResult:
        """
        Execute a single tool call.
        """

        function = tool_call.get("function", {})

        tool_name = function.get("name")

        raw_args = function.get("arguments", {})

        tool_call_id = tool_call.get("id")

        arguments = self._parse_arguments(raw_args)

        tool = TOOL_IMPLS.get(tool_name)

        if tool is None:
            return ToolExecutionResult(
                tool_name=tool_name,
                output=f"ERROR: Unknown tool '{tool_name}'.",
                success=False,
                tool_call_id=tool_call_id,
            )

        try:

            result = tool(arguments)

            return ToolExecutionResult(
                tool_name=tool_name,
                output=str(result),
                success=True,
                tool_call_id=tool_call_id,
            )

        except Exception as exc:

            return ToolExecutionResult(
                tool_name=tool_name,
                output=f"ERROR: {exc}",
                success=False,
                tool_call_id=tool_call_id,
            )

    def execute_all(
        self,
        tool_calls: list[dict[str, Any]],
    ) -> list[ToolExecutionResult]:
        """
        Execute every tool call in order.
        """

        results = []

        for call in tool_calls:
            results.append(self.execute(call))

        return results

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _parse_arguments(
        self,
        raw: Any,
    ) -> dict[str, Any]:
        """
        Ollama models sometimes return arguments as:

        - dict
        - JSON string
        - Python literal string

        Normalize everything into a dictionary.
        """

        if isinstance(raw, dict):
            return raw

        if raw is None:
            return {}

        if isinstance(raw, str):

            try:
                return json.loads(raw)

            except Exception:

                try:
                    return ast.literal_eval(raw)

                except Exception:
                    return {}

        return {}
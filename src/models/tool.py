from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolCall:
    """
    Represents a tool invocation requested by the language model.
    """

    name: str

    arguments: dict[str, Any] = field(default_factory=dict)

    tool_call_id: str | None = None

    @classmethod
    def from_ollama(cls, call: dict[str, Any]) -> "ToolCall":

        function = call.get("function", {})

        return cls(
            name=function.get("name", ""),
            arguments=function.get("arguments", {}),
            tool_call_id=call.get("id"),
        )

    def to_ollama(self) -> dict[str, Any]:

        data = {
            "function": {
                "name": self.name,
                "arguments": self.arguments,
            }
        }

        if self.tool_call_id:
            data["id"] = self.tool_call_id

        return data


@dataclass(slots=True)
class ToolExecutionResult:
    """
    Result of a tool execution.
    """

    tool_name: str

    output: str

    success: bool

    tool_call_id: str | None = None
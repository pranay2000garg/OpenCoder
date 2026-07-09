from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass(slots=True)
class Message:
    """
    Represents a chat message exchanged with the LLM.
    """

    role: Role
    content: str

    name: str | None = None

    tool_call_id: str | None = None

    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:

        data = {
            "role": self.role.value,
            "content": self.content,
        }

        if self.name:
            data["name"] = self.name

        if self.tool_call_id:
            data["tool_call_id"] = self.tool_call_id

        if self.tool_calls:
            data["tool_calls"] = self.tool_calls

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Message":

        return cls(
            role=Role(data["role"]),
            content=data.get("content", ""),
            name=data.get("name"),
            tool_call_id=data.get("tool_call_id"),
            tool_calls=data.get("tool_calls", []),
        )
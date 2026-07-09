from __future__ import annotations

from dataclasses import dataclass, field

from .tool import ToolCall


@dataclass(slots=True)
class ParsedResponse:
    """
    Normalized response returned by the ResponseParser.
    """

    content: str

    tool_calls: list[ToolCall] = field(default_factory=list)
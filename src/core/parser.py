"""
Response parser.

Responsible for converting raw model responses into a normalized
ParsedResponse object.

Supports:
1. Native Ollama tool_calls
2. JSON tool calls wrapped in ```json blocks
3. Raw JSON tool calls
"""

from __future__ import annotations

import json
import re

from ..models.response import ParsedResponse
from ..models.tool import ToolCall


class ResponseParser:
    """
    Parses model responses and extracts tool calls.
    """

    def parse(self, message: dict) -> ParsedResponse:
        """
        Parse a raw model message.

        Parameters
        ----------
        message:
            Raw assistant message returned by Ollama.

        Returns
        -------
        ParsedResponse
        """

        content = message.get("content", "") or ""

        # Native Ollama tool calling
        native_tool_calls = message.get("tool_calls") or []

        if native_tool_calls:
            return ParsedResponse(
                content=content,
                tool_calls=[
                    ToolCall.from_ollama(call)
                    for call in native_tool_calls
                ],
            )

        tool_calls: list[ToolCall] = []

        tool_calls.extend(self._extract_markdown_json(content))
        tool_calls.extend(self._extract_raw_json(content))

        cleaned = self._remove_json_blocks(content)

        return ParsedResponse(
            content=cleaned.strip(),
            tool_calls=tool_calls,
        )

    # ---------------------------------------------------------
    # JSON Extraction
    # ---------------------------------------------------------

    def _extract_markdown_json(self, text: str) -> list[ToolCall]:

        recovered: list[ToolCall] = []

        blocks = re.findall(
            r"```json\s*(.*?)```",
            text,
            flags=re.DOTALL,
        )

        for block in blocks:

            try:

                obj = json.loads(block)

                call = self._build_tool_call(obj)

                if call:
                    recovered.append(call)

            except Exception:
                continue

        return recovered

    def _extract_raw_json(self, text: str) -> list[ToolCall]:

        recovered: list[ToolCall] = []

        raw = self._first_json(text)

        if raw is None:
            return recovered

        try:

            obj = json.loads(raw)

            call = self._build_tool_call(obj)

            if call:
                recovered.append(call)

        except Exception:
            pass

        return recovered

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _build_tool_call(self, obj: dict) -> ToolCall | None:

        if not isinstance(obj, dict):
            return None

        if "name" not in obj:
            return None

        if "arguments" not in obj:
            return None

        return ToolCall(
            name=obj["name"],
            arguments=obj["arguments"],
        )

    def _remove_json_blocks(self, text: str) -> str:

        return re.sub(
            r"```json\s*.*?```",
            "",
            text,
            flags=re.DOTALL,
        )

    def _first_json(self, text: str) -> str | None:
        """
        Return the first balanced JSON object found in text.
        """

        start = text.find("{")

        if start == -1:
            return None

        depth = 0

        for index in range(start, len(text)):

            char = text[index]

            if char == "{":
                depth += 1

            elif char == "}":

                depth -= 1

                if depth == 0:
                    return text[start : index + 1]

        return None
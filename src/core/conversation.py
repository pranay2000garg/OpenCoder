"""
Conversation manager.

Responsible for maintaining the conversation exchanged with
the language model.
"""

from __future__ import annotations

from copy import deepcopy

from ..models.message import Message, Role


class Conversation:
    """
    Stores the complete conversation.

    The agent should interact with this class instead of
    manipulating message lists directly.
    """

    def __init__(self, system_prompt: str):
        self._system_prompt = system_prompt
        self.reset()

    # ---------------------------------------------------------
    # Conversation Management
    # ---------------------------------------------------------

    def reset(self) -> None:
        """Reset the conversation."""

        self._messages: list[Message] = [
            Message(
                role=Role.SYSTEM,
                content=self._system_prompt,
            )
        ]

    # ---------------------------------------------------------
    # Add Messages
    # ---------------------------------------------------------

    def add_user(self, content: str) -> None:

        self._messages.append(
            Message(
                role=Role.USER,
                content=content,
            )
        )

    def add_assistant(
        self,
        content: str,
        tool_calls: list | None = None,
    ) -> None:

        self._messages.append(
            Message(
                role=Role.ASSISTANT,
                content=content,
                tool_calls=tool_calls or [],
            )
        )

    def add_tool(
        self,
        *,
        name: str,
        result: str,
        tool_call_id: str | None = None,
    ) -> None:

        self._messages.append(
            Message(
                role=Role.TOOL,
                name=name,
                content=result,
                tool_call_id=tool_call_id,
            )
        )

    # ---------------------------------------------------------
    # Accessors
    # ---------------------------------------------------------

    def export(self) -> list[dict]:
        """
        Export the conversation in the format expected by
        Ollama.
        """

        return [
            message.to_dict()
            for message in self._messages
        ]

    def messages(self) -> list[Message]:
        """
        Return a copy of the conversation.
        """

        return deepcopy(self._messages)

    def last(self) -> Message | None:

        if not self._messages:
            return None

        return self._messages[-1]

    def count(self) -> int:
        return len(self._messages)

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def append(self, message: Message) -> None:
        """
        Append a message directly.

        Useful for future imports or replay.
        """

        self._messages.append(message)
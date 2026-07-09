"""
Tool contract.
"""

from __future__ import annotations

from typing import Any, Protocol


class Tool(Protocol):
    """
    Every tool implements this interface.
    """

    def __call__(
        self,
        arguments: dict[str, Any],
    ) -> str:
        """
        Execute the tool.

        Returns a string that will be sent back
        to the language model.
        """
        ...
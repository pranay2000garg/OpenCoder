"""
Frame painter.

Responsible for translating DrawOperations into terminal
commands.

The painter knows:

    DrawOperation
            ↓
        Terminal

It knows nothing about Frames, Widgets, Layouts,
Animations, or the Agent.
"""

from __future__ import annotations

from .diff import DrawOperation
from .terminal import Terminal


class Painter:
    """
    Paint DrawOperations onto the terminal.
    """

    def __init__(
        self,
        terminal: Terminal,
    ) -> None:

        self._terminal = terminal

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def paint(
        self,
        operations: list[DrawOperation],
    ) -> None:
        """
        Execute a list of draw operations.
        """

        if not operations:
            return

        for operation in operations:

            self._paint(operation)

        self._terminal.flush()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _paint(
        self,
        operation: DrawOperation,
    ) -> None:

        self._terminal.move(
            operation.x,
            operation.y,
        )

        self._terminal.write(
            operation.text,
        )
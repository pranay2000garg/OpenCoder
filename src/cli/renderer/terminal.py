"""
Low-level terminal backend.

This module is the ONLY place in the renderer that directly
interacts with the terminal using ANSI escape sequences.

Responsibilities
----------------
- Cursor movement
- Screen clearing
- Cursor visibility
- Writing text
- Flushing output
- Reading terminal size

Nothing in this module knows about Frames, Widgets, Layouts,
or the Renderer.
"""

from __future__ import annotations

import shutil
import sys


class Terminal:
    """
    Low-level terminal backend.
    """

    CSI = "\033["

    # ---------------------------------------------------------
    # Cursor
    # ---------------------------------------------------------

    def hide_cursor(self) -> None:
        self._write(f"{self.CSI}?25l")

    def show_cursor(self) -> None:
        self._write(f"{self.CSI}?25h")

    def move(self, x: int, y: int) -> None:
        """
        Move cursor.

        Coordinates are zero-based.
        ANSI escape sequences are one-based.
        """

        self._write(
            f"{self.CSI}{y + 1};{x + 1}H"
        )

    def save_cursor(self) -> None:
        self._write(f"{self.CSI}s")

    def restore_cursor(self) -> None:
        self._write(f"{self.CSI}u")

    # ---------------------------------------------------------
    # Screen
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Clear entire screen.
        """

        self._write(f"{self.CSI}2J")
        self.move(0, 0)

    def clear_line(self) -> None:
        """
        Clear current line.
        """

        self._write(f"{self.CSI}2K")

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    def write(self, text: str) -> None:
        """
        Write raw text.
        """

        self._write(text)

    def flush(self) -> None:
        sys.stdout.flush()

    # ---------------------------------------------------------
    # Terminal Info
    # ---------------------------------------------------------

    def size(self) -> tuple[int, int]:
        """
        Returns

        (width, height)
        """

        size = shutil.get_terminal_size(
            fallback=(80, 24)
        )

        return (
            size.columns,
            size.lines,
        )

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _write(
        self,
        text: str,
    ) -> None:

        sys.stdout.write(text)

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self):

        self.hide_cursor()

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):

        self.show_cursor()

        self.flush()
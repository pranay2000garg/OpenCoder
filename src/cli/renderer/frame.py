"""
Virtual terminal frame.

A Frame represents the complete terminal screen in memory.

Nothing in this class knows about ANSI escape sequences,
cursor movement, stdout, widgets, or layouts.

The renderer will later compare two Frame objects and paint
only the differences.
"""

from __future__ import annotations

from copy import deepcopy


class Frame:
    """
    Virtual terminal screen.
    """

    def __init__(
        self,
        width: int,
        height: int,
        fill: str = " ",
    ) -> None:

        if width <= 0:
            raise ValueError("width must be > 0")

        if height <= 0:
            raise ValueError("height must be > 0")

        if len(fill) != 1:
            raise ValueError("fill must be a single character")

        self.width = width
        self.height = height
        self.fill = fill

        self._rows: list[list[str]] = [
            [fill for _ in range(width)]
            for _ in range(height)
        ]

    # ---------------------------------------------------------
    # Frame Operations
    # ---------------------------------------------------------

    def clear(self) -> None:
        """
        Reset the frame.
        """

        for row in self._rows:
            row[:] = [self.fill] * self.width

    def resize(
        self,
        width: int,
        height: int,
    ) -> None:
        """
        Resize while preserving content.
        """

        if width <= 0:
            raise ValueError("width must be > 0")

        if height <= 0:
            raise ValueError("height must be > 0")

        new_rows = [
            [self.fill] * width
            for _ in range(height)
        ]

        copy_height = min(self.height, height)
        copy_width = min(self.width, width)

        for y in range(copy_height):
            for x in range(copy_width):
                new_rows[y][x] = self._rows[y][x]

        self.width = width
        self.height = height
        self._rows = new_rows

    # ---------------------------------------------------------
    # Writing
    # ---------------------------------------------------------

    def set(
        self,
        x: int,
        y: int,
        char: str,
    ) -> None:
        """
        Write one character.
        """

        if len(char) != 1:
            raise ValueError("char must be one character")

        if not self.in_bounds(x, y):
            return

        self._rows[y][x] = char

    def write(
        self,
        x: int,
        y: int,
        text: str,
    ) -> None:
        """
        Write text beginning at (x, y).
        """

        if y < 0 or y >= self.height:
            return

        if x >= self.width:
            return

        if x < 0:
            text = text[-x:]
            x = 0

        for index, ch in enumerate(text):

            xx = x + index

            if xx >= self.width:
                break

            self._rows[y][xx] = ch

    # ---------------------------------------------------------
    # Reading
    # ---------------------------------------------------------

    def get(
        self,
        x: int,
        y: int,
    ) -> str:

        if not self.in_bounds(x, y):
            raise IndexError("coordinates out of bounds")

        return self._rows[y][x]

    def line(
        self,
        y: int,
    ) -> str:

        if y < 0 or y >= self.height:
            raise IndexError("line out of bounds")

        return "".join(self._rows[y])

    def lines(self) -> list[str]:

        return [
            "".join(row)
            for row in self._rows
        ]

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def in_bounds(
        self,
        x: int,
        y: int,
    ) -> bool:

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def copy(self) -> "Frame":

        frame = Frame(
            self.width,
            self.height,
            self.fill,
        )

        frame._rows = deepcopy(self._rows)

        return frame

    # ---------------------------------------------------------
    # Magic Methods
    # ---------------------------------------------------------

    def __iter__(self):

        return iter(self.lines())

    def __eq__(
        self,
        other: object,
    ) -> bool:

        if not isinstance(other, Frame):
            return False

        return (
            self.width == other.width
            and self.height == other.height
            and self._rows == other._rows
        )

    def __repr__(self) -> str:

        return (
            f"Frame("
            f"width={self.width}, "
            f"height={self.height})"
        )
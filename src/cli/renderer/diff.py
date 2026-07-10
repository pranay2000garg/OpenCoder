"""
Frame diff engine.

Computes the minimal set of operations required to transform one
Frame into another.

The renderer will later translate these operations into terminal
cursor movements and writes.
"""

from __future__ import annotations

from dataclasses import dataclass

from .frame import Frame


# ==========================================================
# Operations
# ==========================================================


@dataclass(frozen=True, slots=True)
class DrawOperation:
    """
    Draw text beginning at (x, y).
    """

    x: int
    y: int
    text: str


# ==========================================================
# Diff Engine
# ==========================================================


class FrameDiffer:
    """
    Compare two frames.

    Produces only the regions that changed.
    """

    def diff(
        self,
        previous: Frame,
        current: Frame,
    ) -> list[DrawOperation]:

        if (
            previous.width != current.width
            or previous.height != current.height
        ):
            raise ValueError(
                "Frame dimensions do not match."
            )

        operations: list[DrawOperation] = []

        for y in range(current.height):

            old = previous.line(y)
            new = current.line(y)

            if old == new:
                continue

            operations.extend(
                self._diff_line(
                    y,
                    old,
                    new,
                )
            )

        return operations

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _diff_line(
        self,
        y: int,
        old: str,
        new: str,
    ) -> list[DrawOperation]:

        operations: list[DrawOperation] = []

        width = len(new)

        x = 0

        while x < width:

            if old[x] == new[x]:
                x += 1
                continue

            start = x

            while (
                x < width
                and old[x] != new[x]
            ):
                x += 1

            operations.append(
                DrawOperation(
                    x=start,
                    y=y,
                    text=new[start:x],
                )
            )

        return operations
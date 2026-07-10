"""
Frame buffer.

Maintains the previous and current frame used by the renderer.

The renderer builds the current frame, compares it with the previous
frame, renders the differences, then swaps them.

Nothing in this module knows about terminals, ANSI escape sequences,
or widgets.
"""

from __future__ import annotations

from .frame import Frame


class FrameBuffer:
    """
    Double-buffered screen.

    previous
        The last rendered frame.

    current
        The frame currently being built.
    """

    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:

        self._previous = Frame(width, height)
        self._current = Frame(width, height)

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def previous(self) -> Frame:
        return self._previous

    @property
    def current(self) -> Frame:
        return self._current

    @property
    def width(self) -> int:
        return self._current.width

    @property
    def height(self) -> int:
        return self._current.height

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def begin_frame(self) -> Frame:
        """
        Start building a new frame.

        Clears the current frame and returns it.
        """

        self._current.clear()

        return self._current

    def end_frame(self) -> None:
        """
        Finish rendering.

        Current becomes previous.
        """

        self.swap()

    def swap(self) -> None:
        """
        Swap buffers.

        Instead of copying memory, we simply swap references.
        """

        self._previous, self._current = (
            self._current,
            self._previous,
        )

    # ---------------------------------------------------------
    # Resize
    # ---------------------------------------------------------

    def resize(
        self,
        width: int,
        height: int,
    ) -> None:
        """
        Resize both buffers.
        """

        self._previous.resize(width, height)
        self._current.resize(width, height)

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def invalidate(self) -> None:
        """
        Force the next render to redraw everything.
        """

        self._previous.clear()

    def copy_previous(self) -> Frame:
        """
        Return a copy of the previous frame.
        """

        return self._previous.copy()

    def copy_current(self) -> Frame:
        """
        Return a copy of the current frame.
        """

        return self._current.copy()

    def __repr__(self) -> str:

        return (
            f"FrameBuffer("
            f"{self.width}x{self.height})"
        )
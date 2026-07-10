"""
Rendering engine.

Coordinates the complete rendering pipeline.

Frame
    ↓
FrameBuffer
    ↓
FrameDiffer
    ↓
Painter
    ↓
Terminal
"""

from __future__ import annotations

from .frame import Frame
from .framebuffer import FrameBuffer
from .diff import FrameDiffer
from .terminal import Terminal
from .painter import Painter


class Renderer:
    """
    Main rendering engine.
    """

    def __init__(self) -> None:

        self._terminal = Terminal()

        width, height = self._terminal.size()

        self._buffer = FrameBuffer(
            width,
            height,
        )

        self._differ = FrameDiffer()

        self._painter = Painter(
            self._terminal,
        )

    # ---------------------------------------------------------
    # Frame Lifecycle
    # ---------------------------------------------------------

    def begin_frame(self) -> Frame:
        """
        Begin constructing a new frame.
        """

        return self._buffer.begin_frame()

    def render(self) -> None:
        """
        Render the current frame.
        """

        operations = self._differ.diff(
            self._buffer.previous,
            self._buffer.current,
        )

        self._painter.paint(
            operations,
        )

        self._buffer.end_frame()

    # ---------------------------------------------------------
    # Screen Management
    # ---------------------------------------------------------

    def resize(self) -> None:
        """
        Resize the renderer to the current terminal.
        """

        width, height = self._terminal.size()

        self._buffer.resize(
            width,
            height,
        )

    def invalidate(self) -> None:
        """
        Force a complete redraw.
        """

        self._buffer.invalidate()

    def clear(self) -> None:
        """
        Clear the physical terminal.
        """

        self._terminal.clear()

        self.invalidate()

    # ---------------------------------------------------------
    # Cursor
    # ---------------------------------------------------------

    def hide_cursor(self) -> None:
        self._terminal.hide_cursor()

    def show_cursor(self) -> None:
        self._terminal.show_cursor()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def width(self) -> int:
        return self._buffer.width

    @property
    def height(self) -> int:
        return self._buffer.height

    @property
    def frame(self) -> Frame:
        """
        Current frame.

        Mostly useful for debugging.
        """

        return self._buffer.current

    # ---------------------------------------------------------
    # Context Manager
    # ---------------------------------------------------------

    def __enter__(self):

        self.hide_cursor()

        return self

    def __exit__(self, exc_type, exc, tb):

        self.show_cursor()

        self._terminal.move(
            0,
            self.height,
        )

        self._terminal.flush()
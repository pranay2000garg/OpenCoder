"""
Spinner animation.

The spinner does NOT print anything.

It simply returns the next animation frame whenever
the renderer asks for it.
"""

from __future__ import annotations

import itertools


class Spinner:
    """
    Terminal spinner animation.
    """

    FRAMES = (
        "⠋",
        "⠙",
        "⠹",
        "⠸",
        "⠼",
        "⠴",
        "⠦",
        "⠧",
        "⠇",
        "⠏",
    )

    def __init__(self) -> None:

        self._frames = itertools.cycle(self.FRAMES)

    def next_frame(self) -> str:
        """
        Return the next spinner frame.
        """

        return next(self._frames)

    def reset(self) -> None:
        """
        Restart the spinner animation.
        """

        self._frames = itertools.cycle(self.FRAMES)
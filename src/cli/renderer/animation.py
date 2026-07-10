"""
Animation engine.

Provides a lightweight animation clock used by the renderer.

Animations never draw directly.

Instead they update state, and the renderer paints the next frame.
"""

from __future__ import annotations

import time
from typing import Protocol


# ==========================================================
# Animation Interface
# ==========================================================


class Animation(Protocol):
    """
    Base animation contract.
    """

    @property
    def finished(self) -> bool:
        ...

    def update(
        self,
        dt: float,
    ) -> None:
        ...


# ==========================================================
# Animation Clock
# ==========================================================


class AnimationClock:
    """
    Updates all active animations.
    """

    def __init__(self) -> None:

        self._animations: list[Animation] = []

        self._last_tick = time.perf_counter()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def add(
        self,
        animation: Animation,
    ) -> None:

        self._animations.append(animation)

    def clear(self) -> None:

        self._animations.clear()

    def tick(self) -> None:
        """
        Advance every animation.
        """

        now = time.perf_counter()

        dt = now - self._last_tick

        self._last_tick = now

        alive: list[Animation] = []

        for animation in self._animations:

            animation.update(dt)

            if not animation.finished:
                alive.append(animation)

        self._animations = alive

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def has_animations(self) -> bool:

        return bool(self._animations)

    @property
    def count(self) -> int:

        return len(self._animations)
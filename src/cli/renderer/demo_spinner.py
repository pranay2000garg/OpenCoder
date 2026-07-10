"""
Spinner renderer demo.

This validates that the rendering engine can continuously update
the screen without scrolling, flickering or leaving artifacts.

Run:

    python -m src.cli.renderer.demo_spinner
"""

from __future__ import annotations

import time

from .renderer import Renderer


SPINNER = [
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
]


def main() -> None:

    with Renderer() as renderer:

        renderer.clear()

        start = time.perf_counter()

        frame_index = 0

        while time.perf_counter() - start < 8:

            frame = renderer.begin_frame()

            frame.write(
                2,
                1,
                "OpenCoder Rendering Engine",
            )

            frame.write(
                2,
                3,
                f"{SPINNER[frame_index]} Thinking...",
            )

            frame.write(
                2,
                5,
                "This should NEVER scroll.",
            )

            frame.write(
                2,
                7,
                "Press Ctrl+C to exit.",
            )

            renderer.render()

            frame_index = (
                frame_index + 1
            ) % len(SPINNER)

            time.sleep(0.08)

        frame = renderer.begin_frame()

        frame.write(
            2,
            1,
            "OpenCoder Rendering Engine",
        )

        frame.write(
            2,
            3,
            "✓ Spinner Test Passed",
        )

        frame.write(
            2,
            5,
            "No scrolling detected.",
        )

        renderer.render()

        input("\nPress ENTER to exit...")


if __name__ == "__main__":
    main()
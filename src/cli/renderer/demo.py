"""
Renderer demo.

Used to validate the rendering engine before integrating it into
OpenCoder.

Run:

    python -m src.cli.renderer.demo
"""

from __future__ import annotations

import time

from .renderer import Renderer


def main() -> None:

    with Renderer() as renderer:

        renderer.clear()

        messages = [
            "Thinking...",
            "Searching project...",
            "Reading README.md...",
            "Editing renderer.py...",
            "Running tests...",
            "Done!",
        ]

        for message in messages:

            frame = renderer.begin_frame()

            frame.write(2, 1, "OpenCoder Renderer Demo")

            frame.write(2, 3, message)

            frame.write(2, 5, "you >")

            renderer.render()

            time.sleep(1)

        time.sleep(2)


if __name__ == "__main__":
    main()
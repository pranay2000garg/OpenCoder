"""
OpenCoder entry point.
"""

from __future__ import annotations

import argparse
import os

from .cli.app import CLIApplication


DEFAULT_MODEL = "qwen2.5-coder:7b"
DEFAULT_SERVER = "http://localhost:11434"


def clear_terminal() -> None:
    """
    Clear the terminal screen.
    """

    os.system("cls" if os.name == "nt" else "clear")


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="ocode",
        description="OpenCoder CLI",
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Model name",
    )

    parser.add_argument(
        "--server",
        default=DEFAULT_SERVER,
        help="Ollama server URL",
    )

    parser.add_argument(
        "--no-tools",
        action="store_true",
        help="Disable tool usage",
    )

    return parser


def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    clear_terminal()

    app = CLIApplication(
        model=args.model,
        base_url=args.server,
        use_tools=not args.no_tools,
    )

    app.run()


if __name__ == "__main__":
    main()
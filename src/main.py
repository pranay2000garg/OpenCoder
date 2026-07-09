"""
OpenCoder entry point.
"""

from __future__ import annotations

import argparse

from .cli.app import CLIApplication


DEFAULT_MODEL = "qwen2.5-coder:7b"
DEFAULT_HOST = "http://localhost:11434"


def build_parser() -> argparse.ArgumentParser:
    """
    Create the command line argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="ocode",
        description="OpenCoder - Local AI Coding Assistant",
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Ollama model to use.",
    )

    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="Ollama server URL.",
    )

    parser.add_argument(
        "--chat",
        action="store_true",
        help="Disable tool usage.",
    )

    parser.add_argument(
        "--yolo",
        action="store_true",
        help="Automatically approve tool actions.",
    )

    return parser


def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    if args.yolo:
        from .tools.approval import approval

        approval.set_auto_approve(True)

    app = CLIApplication(
        model=args.model,
        base_url=args.host,
        use_tools=not args.chat,
    )

    app.run()


if __name__ == "__main__":
    main()
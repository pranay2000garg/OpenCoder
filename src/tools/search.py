"""
Recursive code search tool.
"""

from __future__ import annotations

import re
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    ".pytest_cache",
}


def search_code(arguments: dict) -> str:
    """
    Search recursively for a regex pattern.

    Expected arguments:

    {
        "pattern": "...",
        "path": "."      # optional
    }
    """

    pattern = arguments["pattern"]
    root = Path(arguments.get("path", "."))

    if not root.exists():
        return f"ERROR: '{root}' does not exist."

    try:
        regex = re.compile(pattern)
    except re.error as exc:
        return f"ERROR: Invalid regex: {exc}"

    results: list[str] = []

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        if any(part in IGNORED_DIRECTORIES for part in file.parts):
            continue

        try:
            text = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception:
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):

            if regex.search(line):

                results.append(
                    f"{file}:{line_number}: {line}"
                )

    if not results:
        return "No matches found."

    return "\n".join(results)
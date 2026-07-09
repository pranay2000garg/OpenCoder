"""
Filesystem tools exposed to the LLM.
"""

from __future__ import annotations

import difflib
from pathlib import Path

from .approval import ConsoleApproval


approval = ConsoleApproval()


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _diff(old: str, new: str, filename: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(True),
            new.splitlines(True),
            fromfile=f"{filename} (before)",
            tofile=f"{filename} (after)",
        )
    )


# ---------------------------------------------------------
# read_file
# ---------------------------------------------------------


def read_file(arguments: dict) -> str:
    path = Path(arguments["path"])

    if not path.exists():
        return f"ERROR: '{path}' does not exist."

    if not path.is_file():
        return f"ERROR: '{path}' is not a file."

    text = _read_text(path)

    lines = []

    for index, line in enumerate(text.splitlines(), start=1):
        lines.append(f"{index:4} | {line}")

    return "\n".join(lines)


# ---------------------------------------------------------
# list_dir
# ---------------------------------------------------------


def list_dir(arguments: dict) -> str:
    path = Path(arguments.get("path", "."))

    if not path.exists():
        return f"ERROR: '{path}' does not exist."

    entries = sorted(path.iterdir())

    if not entries:
        return "(empty)"

    output = []

    for entry in entries:

        prefix = "[D]" if entry.is_dir() else "[F]"

        output.append(f"{prefix} {entry.name}")

    return "\n".join(output)


# ---------------------------------------------------------
# write_file
# ---------------------------------------------------------


def write_file(arguments: dict) -> str:
    path = Path(arguments["path"])
    content = arguments["content"]

    old = ""

    if path.exists():
        old = _read_text(path)

    diff = _diff(old, content, str(path))

    print()
    print(diff)

    approved = approval.approve(
        f"Create/Overwrite {path}",
        diff,
    )

    if not approved:
        return "DENIED: user rejected file write."

    _write_text(path, content)

    return f"OK: wrote {len(content)} bytes to '{path}'."


# ---------------------------------------------------------
# edit_file
# ---------------------------------------------------------


def edit_file(arguments: dict) -> str:
    path = Path(arguments["path"])

    if not path.exists():
        return f"ERROR: '{path}' does not exist."

    old_str = arguments["old_str"]
    new_str = arguments["new_str"]

    original = _read_text(path)

    occurrences = original.count(old_str)

    if occurrences == 0:
        return "ERROR: old_str not found."

    if occurrences > 1:
        return "ERROR: old_str is not unique."

    updated = original.replace(
        old_str,
        new_str,
        1,
    )

    diff = _diff(
        original,
        updated,
        str(path),
    )

    print()
    print(diff)

    approved = approval.approve(
        f"Edit {path}",
        diff,
    )

    if not approved:
        return "DENIED: user rejected file edit."

    _write_text(path, updated)

    return f"OK: updated '{path}'."
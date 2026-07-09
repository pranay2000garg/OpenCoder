"""
Shell execution tool.

Provides the run_bash tool used by the language model.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .approval import approval


def run_bash(arguments: dict) -> str:
    """
    Execute a shell command.

    Expected arguments:
        {
            "command": "...",
            "cwd": "...",      # optional
            "timeout": 120     # optional
        }
    """

    command = arguments["command"]
    cwd = arguments.get("cwd")
    timeout = arguments.get("timeout", 120)

    preview = f"Command : {command}\n"

    if cwd:
        preview += f"Working Directory : {cwd}\n"

    preview += f"Timeout : {timeout}s"

    approved = approval.approve(
        "Run Shell Command",
        preview,
    )

    if not approved:
        return "DENIED: user rejected command."

    try:

        result = subprocess.run(
            command,
            shell=True,
            cwd=Path(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    except subprocess.TimeoutExpired:
        return f"ERROR: command timed out after {timeout} seconds."

    except Exception as exc:
        return f"ERROR: {exc}"

    output = []

    output.append(f"Exit Code: {result.returncode}")

    if result.stdout.strip():
        output.append("")
        output.append("STDOUT")
        output.append("-" * 60)
        output.append(result.stdout.rstrip())

    if result.stderr.strip():
        output.append("")
        output.append("STDERR")
        output.append("-" * 60)
        output.append(result.stderr.rstrip())

    return "\n".join(output)
"""
Tool registry.

Contains:

- TOOL_SCHEMAS: JSON schemas sent to the language model.
- TOOL_IMPLS: Mapping from tool name to Python implementation.
"""

from __future__ import annotations

from .filesystem import (
    edit_file,
    list_dir,
    read_file,
    write_file,
)
from .search import search_code
from .shell import run_bash

# ----------------------------------------------------------------------
# Tool Schemas
# ----------------------------------------------------------------------

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a text file with line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file."
                    }
                },
                "required": ["path"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and directories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path. Defaults to current directory."
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                    },
                    "content": {
                        "type": "string",
                    },
                },
                "required": [
                    "path",
                    "content",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace an exact unique block of text in a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                    },
                    "old_str": {
                        "type": "string",
                    },
                    "new_str": {
                        "type": "string",
                    },
                },
                "required": [
                    "path",
                    "old_str",
                    "new_str",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_bash",
            "description": "Execute a shell command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                    },
                    "cwd": {
                        "type": "string",
                    },
                    "timeout": {
                        "type": "integer",
                    },
                },
                "required": [
                    "command",
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search recursively for a regex pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                    },
                    "path": {
                        "type": "string",
                    },
                },
                "required": [
                    "pattern",
                ],
            },
        },
    },
]

# ----------------------------------------------------------------------
# Tool Implementations
# ----------------------------------------------------------------------

TOOL_IMPLS = {
    "read_file": read_file,
    "list_dir": list_dir,
    "write_file": write_file,
    "edit_file": edit_file,
    "run_bash": run_bash,
    "search_code": search_code,
}
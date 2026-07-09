"""
UI Events.

The Agent emits events.
The Renderer consumes them.

Events are immutable.
"""

from __future__ import annotations

from dataclasses import dataclass


# ==========================================================
# Base Event
# ==========================================================

class UIEvent:
    """Base class for all UI events."""


# ==========================================================
# Thinking
# ==========================================================

@dataclass(frozen=True, slots=True)
class ThinkingStarted(UIEvent):
    message: str = "Thinking..."


@dataclass(frozen=True, slots=True)
class ThinkingFinished(UIEvent):
    pass


# ==========================================================
# Assistant Output
# ==========================================================

@dataclass(frozen=True, slots=True)
class AssistantChunk(UIEvent):
    text: str


@dataclass(frozen=True, slots=True)
class AssistantFinished(UIEvent):
    pass


# ==========================================================
# Tool Events
# ==========================================================

@dataclass(frozen=True, slots=True)
class ToolStarted(UIEvent):
    tool: str
    description: str


@dataclass(frozen=True, slots=True)
class ToolFinished(UIEvent):
    tool: str
    description: str
    success: bool


# ==========================================================
# Approval
# ==========================================================

@dataclass(frozen=True, slots=True)
class ApprovalRequested(UIEvent):
    title: str


@dataclass(frozen=True, slots=True)
class ApprovalFinished(UIEvent):
    approved: bool


# ==========================================================
# Errors
# ==========================================================

@dataclass(frozen=True, slots=True)
class ErrorOccurred(UIEvent):
    message: str
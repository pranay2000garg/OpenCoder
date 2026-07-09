"""
Approval contract.
"""

from __future__ import annotations

from typing import Protocol


class ApprovalProvider(Protocol):
    """
    Responsible for asking the user whether
    an action should be executed.
    """

    def approve(
        self,
        title: str,
        preview: str,
    ) -> bool:
        """
        Return True if approved.
        """
        ...
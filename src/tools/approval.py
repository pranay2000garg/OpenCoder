"""
Approval utilities.

Every potentially destructive operation (file writes, shell commands,
etc.) should go through this module before execution.
"""

from __future__ import annotations

from ..contracts.approval import ApprovalProvider


class ConsoleApproval(ApprovalProvider):
    """
    Console-based approval provider.
    """

    def __init__(self, auto_approve: bool = False) -> None:
        self._auto_approve = auto_approve

    @property
    def auto_approve(self) -> bool:
        return self._auto_approve

    def set_auto_approve(self, enabled: bool) -> None:
        self._auto_approve = enabled

    def approve(
        self,
        title: str,
        preview: str,
    ) -> bool:
        """
        Ask the user for approval.

        Returns
        -------
        bool
            True if approved.
        """

        if self._auto_approve:
            return True

        print()
        print("-" * 72)
        print(title)
        print("-" * 72)
        print(preview.rstrip())
        print()

        while True:

            choice = input("Approve? [y/N]: ").strip().lower()

            if choice in ("y", "yes"):
                return True

            if choice in ("", "n", "no"):
                return False

            print("Please enter 'y' or 'n'.")


approval = ConsoleApproval()
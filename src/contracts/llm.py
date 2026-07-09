"""
LLM Provider contract.
"""

from __future__ import annotations

from typing import Any, Protocol


class LLMProvider(Protocol):
    """
    Contract implemented by every LLM provider.
    """

    @property
    def model(self) -> str:
        ...

    @property
    def base_url(self) -> str:
        ...

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        stream: bool = False,
    ) -> dict[str, Any]:
        """
        Send a chat request.
        """
        ...

    def switch_model(self, model: str) -> None:
        """
        Switch the active model.
        """
        ...

    def list_models(self) -> list[dict[str, Any]]:
        """
        Return installed models.
        """
        ...

    def version(self) -> dict[str, Any]:
        """
        Return provider version.
        """
        ...
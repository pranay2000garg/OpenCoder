"""
Ollama client.

Responsible for communicating with the Ollama HTTP API.

No other module should use requests directly.
"""

from __future__ import annotations

from typing import Any

import requests

from ..contracts.llm import LLMProvider


class OllamaError(Exception):
    """Base exception for Ollama."""


class OllamaConnectionError(OllamaError):
    """Raised when Ollama cannot be reached."""


class ModelNotFoundError(OllamaError):
    """Raised when the requested model is unavailable."""


class OllamaClient(LLMProvider):
    """
    Simple wrapper around the Ollama REST API.
    """

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
    ) -> None:

        self._model = model
        self._base_url = base_url.rstrip("/")

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def model(self) -> str:
        return self._model

    @property
    def base_url(self) -> str:
        return self._base_url

    # ---------------------------------------------------------
    # Chat
    # ---------------------------------------------------------

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        stream: bool = False,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "stream": stream,
        }

        if tools:
            payload["tools"] = tools

        return self._post(
            "/api/chat",
            payload,
        )

    # ---------------------------------------------------------
    # Models
    # ---------------------------------------------------------

    def list_models(self) -> list[dict[str, Any]]:

        response = self._get("/api/tags")

        return response.get("models", [])

    def switch_model(self, model: str) -> None:

        self._model = model

    def version(self) -> dict[str, Any]:

        return self._get("/api/version")

    # ---------------------------------------------------------
    # HTTP Helpers
    # ---------------------------------------------------------

    def _get(
        self,
        endpoint: str,
    ) -> dict[str, Any]:

        url = f"{self._base_url}{endpoint}"

        try:

            response = requests.get(
                url,
                timeout=30,
            )

        except requests.exceptions.ConnectionError as exc:

            raise OllamaConnectionError(
                f"Unable to connect to Ollama at {self._base_url}"
            ) from exc

        response.raise_for_status()

        return response.json()

    def _post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        url = f"{self._base_url}{endpoint}"

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=600,
            )

        except requests.exceptions.ConnectionError as exc:

            raise OllamaConnectionError(
                f"Unable to connect to Ollama at {self._base_url}"
            ) from exc

        if response.status_code == 404:

            raise ModelNotFoundError(
                f"Model '{self._model}' was not found.\n"
                f"Run:\n\n"
                f"ollama pull {self._model}"
            )

        response.raise_for_status()

        return response.json()
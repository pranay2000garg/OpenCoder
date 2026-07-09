"""
Main agent implementation.

The Agent orchestrates:

User
    ↓
Conversation
    ↓
LLM Provider
    ↓
Response Parser
    ↓
Tool Executor
    ↓
Conversation
"""

from __future__ import annotations

from .conversation import Conversation
from .ollama import OllamaClient
from .parser import ResponseParser
from .prompts import SYSTEM_PROMPT
from .tool_executor import ToolExecutor
from ..tools.registry import TOOL_SCHEMAS


class Agent:
    """
    Main orchestration class.
    """

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
        use_tools: bool = True,
    ) -> None:

        self.use_tools = use_tools

        self.client = OllamaClient(
            model=model,
            base_url=base_url,
        )

        self.conversation = Conversation(SYSTEM_PROMPT)

        self.parser = ResponseParser()

        self.tool_executor = ToolExecutor()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def model(self) -> str:
        return self.client.model

    @property
    def base_url(self) -> str:
        return self.client.base_url

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the conversation.
        """
        self.conversation.reset()

    def switch_model(self, model: str) -> None:
        """
        Switch the active model.
        """
        self.client.switch_model(model)

    def chat(self, prompt: str) -> str:
        """
        Execute one complete interaction.
        """

        self.conversation.add_user(prompt)

        while True:

            response = self.client.chat(
                messages=self.conversation.export(),
                tools=TOOL_SCHEMAS if self.use_tools else None,
            )

            message = response["message"]

            parsed = self.parser.parse(message)

            self.conversation.add_assistant(
                parsed.content,
                [
                    call.to_ollama()
                    for call in parsed.tool_calls
                ],
            )

            if not parsed.tool_calls:
                return parsed.content

            results = self.tool_executor.execute_all(
                [
                    call.to_ollama()
                    for call in parsed.tool_calls
                ]
            )

            for result in results:

                self.conversation.add_tool(
                    name=result.tool_name,
                    result=result.output,
                    tool_call_id=result.tool_call_id,
                )
"""
Main agent implementation.
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

    @property
    def model(self) -> str:
        return self.client.model

    @property
    def base_url(self) -> str:
        return self.client.base_url

    def reset(self) -> None:
        self.conversation.reset()

    def switch_model(self, model: str) -> None:
        self.client.switch_model(model)

    # ---------------------------------------------------------
    # Existing API
    # ---------------------------------------------------------

    def chat(self, prompt: str) -> str:

        response = []

        for chunk in self.chat_stream(prompt):
            response.append(chunk)

        return "".join(response)

    # ---------------------------------------------------------
    # Streaming API
    # ---------------------------------------------------------

    def chat_stream(self, prompt: str):

        self.conversation.add_user(prompt)

        while True:

            stream = self.client.chat_stream(
                messages=self.conversation.export(),
                tools=TOOL_SCHEMAS if self.use_tools else None,
            )

            assistant_message = {
                "role": "assistant",
                "content": "",
                "tool_calls": [],
            }

            for chunk in stream:

                message = chunk.get("message", {})

                # Collect streamed text
                text = message.get("content", "")

                if text:
                    assistant_message["content"] += text
                    yield text

                # Ollama sends tool calls only in the final chunk
                if "tool_calls" in message:
                    assistant_message["tool_calls"] = message["tool_calls"]

                if chunk.get("done"):
                    break

            parsed = self.parser.parse(assistant_message)

            self.conversation.add_assistant(
                parsed.content,
                [
                    call.to_ollama()
                    for call in parsed.tool_calls
                ],
            )

            if not parsed.tool_calls:
                return

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
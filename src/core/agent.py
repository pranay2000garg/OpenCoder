"""
Main agent implementation.
"""

from __future__ import annotations

from collections.abc import Generator

from .conversation import Conversation
from .ollama import OllamaClient
from .parser import ResponseParser
from .prompts import SYSTEM_PROMPT
from .tool_executor import ToolExecutor
from ..models.tool import ToolCall
from ..models.response import ParsedResponse

from ..cli.events import (
    AssistantChunk,
    AssistantFinished,
    ErrorOccurred,
    ThinkingFinished,
    ThinkingStarted,
    ToolFinished,
    ToolStarted,
    UIEvent,
)

from ..tools.registry import TOOL_SCHEMAS


class Agent:
    """
    Main orchestration class.

    Responsibilities
    ----------------
    - Maintain conversation
    - Stream responses from Ollama
    - Execute tool calls
    - Emit UI events
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

        self.conversation = Conversation(
            SYSTEM_PROMPT,
        )

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
        self.conversation.reset()

    def switch_model(
        self,
        model: str,
    ) -> None:
        self.client.switch_model(model)

    # ---------------------------------------------------------
    # Chat
    # ---------------------------------------------------------

    def chat_events(
        self,
        prompt: str,
    ) -> Generator[UIEvent, None, None]:
        """
        Main event-driven chat loop.
        """

        self.conversation.add_user(prompt)

        while True:

            yield ThinkingStarted()

            try:

                parsed = yield from self._chat_once()

            # except Exception as exc:
            #     yield ThinkingFinished()
            #     yield ErrorOccurred(str(exc))
            #     return
            
            except Exception as exc:

                import traceback

                traceback.print_exc()

                yield ThinkingFinished()

                yield ErrorOccurred(str(exc))

                return

            if parsed is None:
                return

            if not parsed.tool_calls:

                yield AssistantFinished()
                return

            yield from self._execute_tool_calls(
                parsed.tool_calls,
            )
    
    # ---------------------------------------------------------
    # Internal Chat
    # ---------------------------------------------------------

    def _chat_once(
        self,
    ) -> Generator[UIEvent, None, ParsedResponse]:
        """
        Execute a single request against the model.

        Returns
        -------
        ParsedResponse
        """

        stream = self.client.chat_stream(
            messages=self.conversation.export(),
            tools=TOOL_SCHEMAS if self.use_tools else None,
        )

        assistant_message = {
            "role": "assistant",
            "content": "",
            "tool_calls": [],
        }

        thinking = True

        for chunk in stream:

            message = chunk.get("message", {})

            text = message.get("content", "")

            if text:

                if thinking:

                    thinking = False

                    yield ThinkingFinished()

                assistant_message["content"] += text

                yield AssistantChunk(text)

            tool_calls = message.get("tool_calls")

            if tool_calls:

                assistant_message["tool_calls"] = tool_calls

            if chunk.get("done"):
                break

        parsed = self.parser.parse(
            assistant_message
        )

        self.conversation.add_assistant(
            parsed.content,
            [
                call.to_ollama()
                for call in parsed.tool_calls
            ],
        )

        return parsed
    
        # ---------------------------------------------------------
    # Tool Execution
    # ---------------------------------------------------------
    
    def _execute_tool_calls(
        self,
        tool_calls: list[ToolCall],
    ) -> Generator[UIEvent, None, None]:
        """
        Execute every requested tool one by one.
        """

        for call in tool_calls:

            description = self._tool_description(call)

            yield ToolStarted(
                tool=call.name,
                description=description,
            )

            result = self.tool_executor.execute(
                call.to_ollama()
            )

            self.conversation.add_tool(
                name=result.tool_name,
                result=result.output,
                tool_call_id=result.tool_call_id,
            )

            yield ToolFinished(
                tool=result.tool_name,
                description=description,
                success=result.success,
            )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _tool_description(
        self,
        call: ToolCall,
    ) -> str:

        name = call.name

        args = call.arguments

        if name == "write_file":
            return f"Creating {args.get('path', '')}"

        if name == "edit_file":
            return f"Editing {args.get('path', '')}"

        if name == "read_file":
            return f"Reading {args.get('path', '')}"

        if name == "list_dir":
            return f"Scanning {args.get('path', '.')}"

        if name == "search_code":
            return "Searching project"

        if name == "run_bash":
            return f"Running {args.get('command', '')}"

        return f"Running {name}"
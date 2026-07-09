"""
Main REPL application.
"""

from __future__ import annotations

from ..core.agent import Agent
from .commands import CommandHandler
from .ui import (
    prompt,
    render_home,
    print_error,
)


class CLIApplication:
    """
    Interactive CLI application.
    """

    def __init__(
        self,
        model: str,
        base_url: str,
        use_tools: bool = True,
    ) -> None:

        self.agent = Agent(
            model=model,
            base_url=base_url,
            use_tools=use_tools,
        )

        self.commands = CommandHandler(self.agent)

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------

    def run(self) -> None:

        render_home(self.agent)

        while True:

            try:

                user_input = prompt().strip()

            except (EOFError, KeyboardInterrupt):

                print()
                print("Goodbye!")
                break

            if not user_input:
                continue

            try:

                if user_input.startswith("/"):

                    handled = self.commands.execute(user_input)

                    if handled:
                        continue

                print()
                print("ocode › ", end="", flush=True)

                for chunk in self.agent.chat_stream(user_input):
                    print(chunk, end="", flush=True)

                print()
                print()

            except SystemExit:
                raise

            except Exception as exc:

                print_error(str(exc))
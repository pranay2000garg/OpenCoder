"""
Main CLI application.
"""

from __future__ import annotations

from ..core.agent import Agent
from .commands import CommandHandler
from .renderer.renderer import Renderer
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

        self.renderer = Renderer()

        self.commands = CommandHandler(
            self.agent,
        )

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

            # -----------------------------------------
            # Commands
            # -----------------------------------------

            if user_input.startswith("/"):

                handled = self.commands.execute(
                    user_input
                )

                if handled:
                    continue

            # -----------------------------------------
            # Chat
            # -----------------------------------------

            self.renderer.start()

            try:

                for event in self.agent.chat_events(
                    user_input
                ):

                    self.renderer.dispatch(event)

            except Exception as exc:

                print_error(str(exc))

            finally:

                self.renderer.stop()
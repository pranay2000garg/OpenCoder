"""
Slash command handler.
"""

from __future__ import annotations

from .ui import render_home, print_success, print_warning


class CommandHandler:
    """
    Handles slash commands entered by the user.
    """

    def __init__(self, agent):
        self.agent = agent

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def execute(self, command: str) -> bool:
        """
        Execute a slash command.

        Returns True if the command was handled,
        otherwise False.
        """

        command = command.strip()

        if not command.startswith("/"):
            return False

        parts = command.split(maxsplit=1)

        name = parts[0].lower()

        argument = ""

        if len(parts) > 1:
            argument = parts[1].strip()

        # -----------------------------------------------------
        # Help
        # -----------------------------------------------------

        if name == "/help":

            print(
                """
Available Commands

/help               Show this help message
/model <name>       Switch model
/reset              Reset conversation
/clear              Clear screen
/tools              Toggle tool usage
/yolo               Toggle auto approval
/exit               Exit OpenCoder
"""
            )

            return True

        # -----------------------------------------------------
        # Model
        # -----------------------------------------------------

        if name == "/model":

            if not argument:
                print_warning("Usage: /model <model-name>")
                return True

            self.agent.switch_model(argument)

            render_home(
                self.agent,
                f"Switched to model: {argument}",
            )

            return True

        # -----------------------------------------------------
        # Reset
        # -----------------------------------------------------

        if name == "/reset":

            self.agent.reset()

            render_home(
                self.agent,
                "Conversation reset.",
            )

            return True

        # -----------------------------------------------------
        # Clear
        # -----------------------------------------------------

        if name == "/clear":

            render_home(self.agent)

            return True

        # -----------------------------------------------------
        # Tools
        # -----------------------------------------------------

        if name == "/tools":

            self.agent.use_tools = not self.agent.use_tools

            render_home(
                self.agent,
                "Tools Enabled"
                if self.agent.use_tools
                else "Tools Disabled",
            )

            return True

        # -----------------------------------------------------
        # YOLO
        # -----------------------------------------------------

        if name == "/yolo":

            from ..tools.approval import approval

            approval.set_auto_approve(
                not approval.auto_approve
            )

            render_home(
                self.agent,
                "Auto Approval Enabled"
                if approval.auto_approve
                else "Auto Approval Disabled",
            )

            return True

        # -----------------------------------------------------
        # Exit
        # -----------------------------------------------------

        if name in ("/exit", "/quit"):

            raise SystemExit(0)

        # -----------------------------------------------------
        # Unknown
        # -----------------------------------------------------

        print_warning(f"Unknown command: {name}")

        return True
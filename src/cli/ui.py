"""
Terminal UI utilities.
"""

from __future__ import annotations

import os

RESET = "\033[0m"
BOLD = "\033[1m"

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
DIM = "\033[2m"


BANNER = rf"""
  ____   ____ ___  ____   ______
 / __ \ / ___/ __ \/ __ \ / ____/
/ /_/ // /  / / / / / / // __/
/ ____// /__/ /_/ / /_/ // /___
/_/     \____\____/_____//_____/

           {BOLD}OpenCoder{RESET}
"""


def clear_screen() -> None:
    """
    Clear the terminal.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(agent) -> None:
    """
    Print the application banner.
    """

    print(BANNER)

    print(f"{DIM}Model : {agent.model}{RESET}")
    print(f"{DIM}Server: {agent.base_url}{RESET}")
    print(
        f"{DIM}Mode  : {'Tools Enabled' if agent.use_tools else 'Chat Only'}{RESET}"
    )


def render_home(agent, message: str | None = None) -> None:
    """
    Render the home screen.
    """

    clear_screen()

    print_banner(agent)

    print()

    if message:
        print(f"{GREEN}✓ {message}{RESET}")
        print()

    print(
        f"{DIM}Type your request, or /help for commands. Ctrl+D to exit.{RESET}"
    )

    print()


def print_assistant(text: str) -> None:
    """
    Print assistant output.
    """

    print()

    print(f"{CYAN}ocode{RESET} {text}")

    print()


def print_error(text: str) -> None:
    print(f"{RED}{text}{RESET}")


def print_warning(text: str) -> None:
    print(f"{YELLOW}{text}{RESET}")


def print_success(text: str) -> None:
    print(f"{GREEN}{text}{RESET}")


def prompt() -> str:
    """
    Read user input.
    """

    return input(f"{BOLD}you › {RESET}")
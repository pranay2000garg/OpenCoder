"""
Terminal renderer.

The renderer is the ONLY component allowed to write to stdout.
Everything else emits UI events.
"""

from __future__ import annotations

import sys
import threading
import time

from .events import UIEvent
from .spinner import Spinner


class Renderer:
    """
    Event-driven terminal renderer.
    """

    SPINNER_INTERVAL = 0.08

    def __init__(self) -> None:

        self.spinner = Spinner()

        self._running = False

        self._spinner_thread: threading.Thread | None = None

        self._render_lock = threading.Lock()

        self._spinner_active = False

        self._spinner_message = ""

        self._streaming = False

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def start(self) -> None:

        if self._running:
            return

        self._running = True

        self._spinner_thread = threading.Thread(
            target=self._spinner_loop,
            daemon=True,
        )

        self._spinner_thread.start()

    def stop(self) -> None:

        self._running = False

        if self._spinner_thread:
            self._spinner_thread.join()

        with self._render_lock:
            self._clear_line()

    # ---------------------------------------------------------
    # Dispatcher
    # ---------------------------------------------------------

    def dispatch(
        self,
        event: UIEvent,
    ) -> None:
        """
        Dispatch an event to its handler.

        Example:

            ThinkingStarted
                ↓
            _on_thinkingstarted()
        """

        handler_name = (
            "_on_" + event.__class__.__name__.lower()
        )

        handler = getattr(
            self,
            handler_name,
            None,
        )

        if handler is None:
            return

        handler(event)

    # ---------------------------------------------------------
    # Spinner Thread
    # ---------------------------------------------------------

    def _spinner_loop(self) -> None:

        while self._running:

            if self._spinner_active:

                self._refresh_spinner()

            time.sleep(self.SPINNER_INTERVAL)

        # ---------------------------------------------------------
    # Thinking Events
    # ---------------------------------------------------------

    def _on_thinkingstarted(
        self,
        event,
    ) -> None:

        self._spinner_message = event.message

        self._spinner_active = True

    def _on_thinkingfinished(
        self,
        event,
    ) -> None:

        self._spinner_active = False

        with self._render_lock:

            self._clear_line()

    # ---------------------------------------------------------
    # Assistant Events
    # ---------------------------------------------------------

    def _on_assistantchunk(
        self,
        event,
    ) -> None:

        with self._render_lock:

            if self._spinner_active:

                self._spinner_active = False

                self._clear_line()

            if not self._streaming:

                sys.stdout.write("ocode › ")

                self._streaming = True

            sys.stdout.write(event.text)

            sys.stdout.flush()

    def _on_assistantfinished(
        self,
        event,
    ) -> None:

        with self._render_lock:

            if self._streaming:

                sys.stdout.write("\n\n")

                sys.stdout.flush()

            self._streaming = False

        # ---------------------------------------------------------
    # Thinking Events
    # ---------------------------------------------------------

    def _on_thinkingstarted(
        self,
        event,
    ) -> None:

        self._spinner_message = event.message

        self._spinner_active = True

    def _on_thinkingfinished(
        self,
        event,
    ) -> None:

        self._spinner_active = False

        with self._render_lock:

            self._clear_line()

    # ---------------------------------------------------------
    # Assistant Events
    # ---------------------------------------------------------

    def _on_assistantchunk(
        self,
        event,
    ) -> None:

        with self._render_lock:

            if self._spinner_active:

                self._spinner_active = False

                self._clear_line()

            if not self._streaming:

                sys.stdout.write("ocode › ")

                self._streaming = True

            sys.stdout.write(event.text)

            sys.stdout.flush()

    def _on_assistantfinished(
        self,
        event,
    ) -> None:

        with self._render_lock:

            if self._streaming:

                sys.stdout.write("\n\n")

                sys.stdout.flush()

            self._streaming = False

        # ---------------------------------------------------------
    # Rendering Helpers
    # ---------------------------------------------------------

    def _refresh_spinner(self) -> None:

        with self._render_lock:

            if not self._spinner_active:
                return

            frame = self.spinner.next_frame()

            self._clear_line()

            self._write(
                f"{frame} {self._spinner_message}"
            )

    def _write(
        self,
        text: str,
        flush: bool = True,
    ) -> None:
        """
        Write text to stdout.

        This is the ONLY place that directly writes to stdout.
        """

        sys.stdout.write(text)

        if flush:
            sys.stdout.flush()

    def _clear_line(self) -> None:
        """
        Clear the current terminal line.
        """

        self._write("\r", flush=False)

        self._write(" " * 200, flush=False)

        self._write("\r")

    def _newline(
        self,
        count: int = 1,
    ) -> None:

        self._write("\n" * count)

    def _success(
        self,
        message: str,
    ) -> None:

        self._write(f"✓ {message}\n")

    def _error(
        self,
        message: str,
    ) -> None:

        self._write(f"✗ {message}\n")

    
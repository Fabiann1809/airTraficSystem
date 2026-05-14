import tkinter as tk

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    COLOR_WHITE, COLOR_GRAY,
    FONT_SMALL,
)

_BG_STATUS = "#1A252F"


class StatusBar(tk.Frame):
    """Bottom status bar that always shows the most recent log event."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(parent, bg=_BG_STATUS, height=24)
        self._orchestrator = orchestrator
        self.pack_propagate(False)

        tk.Label(
            self,
            text="Estado: ",
            bg=_BG_STATUS,
            fg=COLOR_GRAY,
            font=FONT_SMALL,
        ).pack(side="left", padx=(8, 0))

        self._label = tk.Label(
            self,
            text="Sistema iniciado",
            bg=_BG_STATUS,
            fg=COLOR_WHITE,
            font=FONT_SMALL,
            anchor="w",
        )
        self._label.pack(side="left", fill="x", expand=True, padx=(0, 8))

    def refresh(self) -> None:
        """Updates the label with the last entry from the event log."""
        log = self._orchestrator.get_system_status()["log"]
        if log:
            last = log[-1]
            self._label.config(text=f"[{last['timestamp']}] {last['message']}")

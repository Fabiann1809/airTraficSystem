import tkinter as tk

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    COLOR_GREEN, COLOR_RED, COLOR_WHITE, COLOR_GRAY, COLOR_YELLOW,
    FONT_SMALL,
)

_BG_STATUS = "#1A252F"


class StatusBar(tk.Frame):
    """Bottom status bar showing the last log event and live system stats."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(parent, bg=_BG_STATUS, height=26)
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

        # Live stats on the right side
        tk.Label(self, text="|", bg=_BG_STATUS, fg=COLOR_GRAY, font=FONT_SMALL).pack(side="right", padx=4)

        self._incidents_stat = tk.Label(
            self, text="Emerg: 0",
            bg=_BG_STATUS, fg=COLOR_GRAY, font=FONT_SMALL,
        )
        self._incidents_stat.pack(side="right", padx=(0, 6))

        tk.Label(self, text="|", bg=_BG_STATUS, fg=COLOR_GRAY, font=FONT_SMALL).pack(side="right", padx=4)

        self._queue_stat = tk.Label(
            self, text="Cola: 0",
            bg=_BG_STATUS, fg=COLOR_GRAY, font=FONT_SMALL,
        )
        self._queue_stat.pack(side="right", padx=(0, 6))

        tk.Label(self, text="|", bg=_BG_STATUS, fg=COLOR_GRAY, font=FONT_SMALL).pack(side="right", padx=4)

        self._runway_stat = tk.Label(
            self, text="Pistas: 4/4",
            bg=_BG_STATUS, fg=COLOR_GREEN, font=FONT_SMALL,
        )
        self._runway_stat.pack(side="right", padx=(0, 6))

    def refresh(self) -> None:
        """Updates the last-event label and all live stat counters."""
        status = self._orchestrator.get_system_status()

        log = status["log"]
        if log:
            last = log[-1]
            self._label.config(text=f"[{last['timestamp']}] {last['message']}")

        free = sum(1 for r in status["runways"] if r["status"] == "Libre")
        queue = status["queue_size"]
        incidents = status["incidents_count"]

        self._runway_stat.config(
            text=f"Pistas: {free}/4",
            fg=COLOR_GREEN if free > 0 else COLOR_RED,
        )
        self._queue_stat.config(
            text=f"Cola: {queue}",
            fg=COLOR_YELLOW if queue > 0 else COLOR_GRAY,
        )
        self._incidents_stat.config(
            text=f"Emerg: {incidents}",
            fg=COLOR_RED if incidents > 0 else COLOR_GRAY,
        )

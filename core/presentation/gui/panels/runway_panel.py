import tkinter as tk
from tkinter import messagebox, simpledialog

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    BG_DARK, BG_PANEL, BG_CARD,
    COLOR_GREEN, COLOR_RED, COLOR_WHITE, COLOR_CYAN,
    FONT_TITLE, FONT_BODY,
)


class RunwayPanel(tk.LabelFrame):
    """Panel that visualizes the state of the 4 runways as colored cards."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(
            parent,
            text="Pistas de Aterrizaje",
            bg=BG_PANEL,
            fg=COLOR_CYAN,
            font=FONT_TITLE,
            padx=6,
            pady=6,
            relief="groove",
            bd=1,
        )
        self._orchestrator = orchestrator
        self._runway_labels: list[tk.Label] = []

        for i in range(4):
            lbl = tk.Label(
                self,
                text=f"Pista {i + 1}: LIBRE",
                bg=COLOR_GREEN,
                fg=BG_DARK,
                font=FONT_BODY,
                relief="flat",
                anchor="w",
                padx=8,
                pady=5,
            )
            lbl.pack(fill="x", pady=2)
            self._runway_labels.append(lbl)

        tk.Button(
            self,
            text="Liberar pista",
            bg=BG_CARD,
            fg=COLOR_WHITE,
            font=FONT_BODY,
            relief="flat",
            cursor="hand2",
            activebackground="#4A6080",
            activeforeground=COLOR_WHITE,
            command=self._release_runway,
        ).pack(fill="x", pady=(6, 0))

    def _release_runway(self) -> None:
        num = simpledialog.askinteger(
            "Liberar pista",
            "Número de pista (1-4):",
            minvalue=1,
            maxvalue=4,
            parent=self,
        )
        if num is not None:
            try:
                self._orchestrator.release_runway(num - 1)
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=self)
        self.master.master.refresh_all()

    def refresh(self) -> None:
        """Updates each runway label color and text from the current system state."""
        for info in self._orchestrator.get_system_status()["runways"]:
            i = info["index"]
            if info["status"] == "Libre":
                self._runway_labels[i].config(
                    bg=COLOR_GREEN,
                    fg=BG_DARK,
                    text=f"Pista {i + 1}:  LIBRE",
                )
            else:
                flight_id = info["aircraft"].split(" | ")[0] if info["aircraft"] else ""
                self._runway_labels[i].config(
                    bg=COLOR_RED,
                    fg=COLOR_WHITE,
                    text=f"Pista {i + 1}:  {flight_id}  [OCUPADA]",
                )

import tkinter as tk

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    BG_PANEL, BG_CARD,
    COLOR_CYAN, COLOR_WHITE,
    FONT_TITLE, FONT_BODY,
)


class RadarPanel(tk.LabelFrame):
    """Panel showing the active radar quadrant with forward/backward navigation."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(
            parent,
            text="Radar - Cuadrante Activo",
            bg=BG_PANEL,
            fg=COLOR_CYAN,
            font=FONT_TITLE,
            padx=6,
            pady=6,
            relief="groove",
            bd=1,
        )
        self._orchestrator = orchestrator

        self._sector_label = tk.Label(
            self,
            text="---",
            bg=BG_PANEL,
            fg=COLOR_CYAN,
            font=("Consolas", 22, "bold"),
            pady=12,
        )
        self._sector_label.pack(fill="x")

        self._detail_label = tk.Label(
            self,
            text="",
            bg=BG_PANEL,
            fg=COLOR_WHITE,
            font=FONT_BODY,
        )
        self._detail_label.pack(fill="x", pady=(0, 6))

        btn_frame = tk.Frame(self, bg=BG_PANEL)
        btn_frame.pack(fill="x")

        for text, cmd in [("← Anterior", self._scan_previous), ("Siguiente →", self._scan_next)]:
            tk.Button(
                btn_frame,
                text=text,
                bg=BG_CARD,
                fg=COLOR_WHITE,
                font=FONT_BODY,
                relief="flat",
                cursor="hand2",
                activebackground="#4A6080",
                activeforeground=COLOR_WHITE,
                command=cmd,
            ).pack(side="left", fill="x", expand=True, padx=2)

    def _scan_next(self) -> None:
        self._orchestrator.cycle_radar_forward()
        self.master.master.refresh_all()

    def _scan_previous(self) -> None:
        self._orchestrator.cycle_radar_backward()
        self.master.master.refresh_all()

    def refresh(self) -> None:
        """Updates the sector display from the current active sector."""
        sector_str = self._orchestrator.get_system_status()["active_sector"]
        if sector_str:
            # Format: "Cuadrante Norte (Q-001) | Aeronaves: 0"
            parts = sector_str.split(" ")
            name = parts[1] if len(parts) > 1 else "---"
            self._sector_label.config(text=name)
            self._detail_label.config(text=sector_str)
        else:
            self._sector_label.config(text="---")
            self._detail_label.config(text="")

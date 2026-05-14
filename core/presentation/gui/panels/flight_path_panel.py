import tkinter as tk
from tkinter import messagebox, simpledialog

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    BG_DARK, BG_PANEL, BG_CARD,
    COLOR_CYAN, COLOR_WHITE, COLOR_YELLOW, COLOR_GRAY,
    FONT_TITLE, FONT_BODY,
)


class FlightPathPanel(tk.LabelFrame):
    """Panel that visualizes the doubly linked waypoint list with bidirectional navigation."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(
            parent,
            text="Plan de Vuelo (Lista Doble)",
            bg=BG_PANEL,
            fg=COLOR_CYAN,
            font=FONT_TITLE,
            padx=6,
            pady=6,
            relief="groove",
            bd=1,
        )
        self._orchestrator = orchestrator

        lb_frame = tk.Frame(self, bg=BG_CARD)
        lb_frame.pack(fill="both", expand=True, pady=(0, 6))

        self._listbox = tk.Listbox(
            lb_frame,
            bg=BG_CARD,
            fg=COLOR_WHITE,
            font=FONT_BODY,
            relief="flat",
            selectbackground=COLOR_CYAN,
            selectforeground=BG_DARK,
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
            height=6,
        )
        scrollbar = tk.Scrollbar(
            lb_frame, orient="vertical",
            command=self._listbox.yview,
            bg=BG_PANEL, troughcolor=BG_CARD,
        )
        self._listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._listbox.pack(side="left", fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=BG_PANEL)
        btn_frame.pack(fill="x")

        nav_frame = tk.Frame(btn_frame, bg=BG_PANEL)
        nav_frame.pack(fill="x", pady=(0, 2))

        for text, cmd in [("← Anterior", self._navigate_backward), ("Siguiente →", self._navigate_forward)]:
            tk.Button(
                nav_frame,
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

        action_frame = tk.Frame(btn_frame, bg=BG_PANEL)
        action_frame.pack(fill="x", pady=(2, 0))

        tk.Button(
            action_frame,
            text="Agregar waypoint",
            bg=BG_CARD,
            fg=COLOR_YELLOW,
            font=FONT_BODY,
            relief="flat",
            cursor="hand2",
            activebackground="#4A6080",
            activeforeground=COLOR_WHITE,
            command=self._add_waypoint,
        ).pack(side="left", fill="x", expand=True, padx=(2, 1))

        tk.Button(
            action_frame,
            text="⟲ Reiniciar",
            bg=BG_CARD,
            fg=COLOR_GRAY,
            font=FONT_BODY,
            relief="flat",
            cursor="hand2",
            activebackground="#4A6080",
            activeforeground=COLOR_WHITE,
            command=self._reset_navigation,
        ).pack(side="left", fill="x", expand=True, padx=(1, 2))

    def _navigate_forward(self) -> None:
        try:
            self._orchestrator.navigate_waypoint_forward()
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e), parent=self)
        self.master.master.refresh_all()

    def _navigate_backward(self) -> None:
        try:
            self._orchestrator.navigate_waypoint_backward()
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e), parent=self)
        self.master.master.refresh_all()

    def _reset_navigation(self) -> None:
        self._orchestrator.reset_waypoint_navigation()
        self.master.master.refresh_all()

    def _add_waypoint(self) -> None:
        coords = simpledialog.askstring(
            "Agregar waypoint",
            "Ingrese las coordenadas del waypoint:",
            parent=self,
        )
        if coords and coords.strip():
            self._orchestrator.add_waypoint(coords.strip())
            self.master.master.refresh_all()

    def refresh(self) -> None:
        """Rebuilds the listbox, highlighting the current waypoint in cyan."""
        status = self._orchestrator.get_system_status()
        waypoints = status["waypoints"]
        current = status["current_waypoint"]

        self._listbox.delete(0, tk.END)
        for i, wp in enumerate(waypoints):
            self._listbox.insert(tk.END, f"  {wp}")
            if wp == current:
                self._listbox.itemconfig(i, fg=BG_DARK, bg=COLOR_CYAN)
            else:
                self._listbox.itemconfig(i, fg=COLOR_WHITE, bg=BG_CARD)

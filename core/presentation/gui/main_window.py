import tkinter as tk

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import BG_DARK
from core.presentation.gui.panels.runway_panel import RunwayPanel
from core.presentation.gui.panels.radar_panel import RadarPanel
from core.presentation.gui.panels.queue_panel import QueuePanel
from core.presentation.gui.panels.emergency_panel import EmergencyPanel
from core.presentation.gui.panels.flight_path_panel import FlightPathPanel
from core.presentation.gui.panels.log_panel import LogPanel
from core.presentation.gui.widgets.status_bar import StatusBar


class MainWindow(tk.Tk):
    """Root window that assembles all panels into a 3-column layout."""

    def __init__(self, orchestrator: ATCOrchestrator) -> None:
        super().__init__()
        self._orchestrator = orchestrator

        self.title("Sistema ATC - Control de Tráfico Aéreo")
        self.minsize(1100, 650)
        self.geometry("1260x730")
        self.configure(bg=BG_DARK)

        # Main grid: row 0 = panels, row 1 = status bar
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        # ── Column frames ──────────────────────────────────────────────
        left_col = tk.Frame(self, bg=BG_DARK)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=8)

        center_col = tk.Frame(self, bg=BG_DARK)
        center_col.grid(row=0, column=1, sticky="nsew", padx=4, pady=8)

        right_col = tk.Frame(self, bg=BG_DARK)
        right_col.grid(row=0, column=2, sticky="nsew", padx=(4, 8), pady=8)

        # ── Left column: runways (fixed) + radar (expands) ─────────────
        self._runway_panel = RunwayPanel(left_col, orchestrator)
        self._runway_panel.pack(fill="x", pady=(0, 4))

        self._radar_panel = RadarPanel(left_col, orchestrator)
        self._radar_panel.pack(fill="both", expand=True)

        # ── Center column: queue (expands) + emergencies (expands) ─────
        self._queue_panel = QueuePanel(center_col, orchestrator)
        self._queue_panel.pack(fill="both", expand=True, pady=(0, 4))

        self._emergency_panel = EmergencyPanel(center_col, orchestrator)
        self._emergency_panel.pack(fill="both", expand=True)

        # ── Right column: flight path + log ────────────────────────────
        self._flight_path_panel = FlightPathPanel(right_col, orchestrator)
        self._flight_path_panel.pack(fill="both", expand=True, pady=(0, 4))

        self._log_panel = LogPanel(right_col, orchestrator)
        self._log_panel.pack(fill="both", expand=True)

        # ── Status bar (spans all 3 columns) ───────────────────────────
        self._status_bar = StatusBar(self, orchestrator)
        self._status_bar.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.refresh_all()

    def refresh_all(self) -> None:
        """Calls refresh() on every panel and the status bar."""
        self._runway_panel.refresh()
        self._radar_panel.refresh()
        self._queue_panel.refresh()
        self._emergency_panel.refresh()
        self._flight_path_panel.refresh()
        self._log_panel.refresh()
        self._status_bar.refresh()

    def get_orchestrator(self) -> ATCOrchestrator:
        """Returns the shared orchestrator instance."""
        return self._orchestrator

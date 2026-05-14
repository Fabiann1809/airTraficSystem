import tkinter as tk

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    BG_PANEL, BG_CARD,
    COLOR_RED, COLOR_WHITE, COLOR_CYAN, COLOR_GRAY,
    FONT_TITLE, FONT_SMALL,
)


class LogPanel(tk.LabelFrame):
    """Panel that displays the chronological event log with incremental updates."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(
            parent,
            text="Log de Eventos",
            bg=BG_PANEL,
            fg=COLOR_CYAN,
            font=FONT_TITLE,
            padx=6,
            pady=6,
            relief="groove",
            bd=1,
        )
        self._orchestrator = orchestrator
        self._displayed_count: int = 0

        text_frame = tk.Frame(self, bg=BG_CARD)
        text_frame.pack(fill="both", expand=True, pady=(0, 6))

        self._text = tk.Text(
            text_frame,
            bg=BG_CARD,
            fg=COLOR_WHITE,
            font=FONT_SMALL,
            relief="flat",
            state=tk.DISABLED,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
        )
        scrollbar = tk.Scrollbar(
            text_frame, orient="vertical",
            command=self._text.yview,
            bg=BG_PANEL, troughcolor=BG_CARD,
        )
        self._text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._text.pack(side="left", fill="both", expand=True)

        self._text.tag_config("emergency", foreground=COLOR_RED)
        self._text.tag_config("normal", foreground=COLOR_WHITE)
        self._text.tag_config("timestamp", foreground=COLOR_GRAY)

        tk.Button(
            self,
            text="Limpiar log",
            bg=BG_CARD,
            fg=COLOR_GRAY,
            font=FONT_SMALL,
            relief="flat",
            cursor="hand2",
            activebackground="#4A6080",
            activeforeground=COLOR_WHITE,
            command=self._clear_display,
        ).pack(fill="x")

    def _clear_display(self) -> None:
        """Clears the visual log display; resets the counter to avoid re-showing old entries."""
        self._text.configure(state=tk.NORMAL)
        self._text.delete("1.0", tk.END)
        self._text.configure(state=tk.DISABLED)
        self._displayed_count = self._orchestrator.get_system_status()["log_size"]

    def refresh(self) -> None:
        """Appends only new log entries to the Text widget since the last refresh."""
        log = self._orchestrator.get_system_status()["log"]
        current_size = len(log)

        self._text.configure(state=tk.NORMAL)

        if current_size < self._displayed_count:
            self._text.delete("1.0", tk.END)
            self._displayed_count = 0

        for entry in log[self._displayed_count:]:
            ts = f"[{entry['timestamp']}] "
            msg = entry["message"] + "\n"
            self._text.insert(tk.END, ts, "timestamp")
            tag = "emergency" if "EMERGENCIA" in entry["message"] else "normal"
            self._text.insert(tk.END, msg, tag)

        self._text.configure(state=tk.DISABLED)
        if current_size > self._displayed_count:
            self._text.see(tk.END)
        self._displayed_count = current_size

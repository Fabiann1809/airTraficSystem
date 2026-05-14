import tkinter as tk
from tkinter import messagebox

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    BG_DARK, BG_PANEL, BG_CARD,
    COLOR_GREEN, COLOR_WHITE, COLOR_YELLOW, COLOR_CYAN, COLOR_GRAY,
    FONT_TITLE, FONT_BODY, FONT_SMALL,
)


class QueuePanel(tk.LabelFrame):
    """Panel that displays the FIFO landing queue and provides enqueue/dequeue controls."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(
            parent,
            text="Cola de Espera (FIFO)",
            bg=BG_PANEL,
            fg=COLOR_CYAN,
            font=FONT_TITLE,
            padx=6,
            pady=6,
            relief="groove",
            bd=1,
        )
        self._orchestrator = orchestrator

        self._count_label = tk.Label(
            self,
            text="0 aviones en cola",
            bg=BG_PANEL,
            fg=COLOR_YELLOW,
            font=FONT_SMALL,
            anchor="w",
        )
        self._count_label.pack(fill="x", pady=(0, 4))

        lb_frame = tk.Frame(self, bg=BG_CARD, relief="flat")
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

        for text, cmd in [("Agregar avión", self._add_aircraft), ("Aterrizar siguiente", self._land_next)]:
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

    def _add_aircraft(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Agregar Avión")
        dialog.configure(bg=BG_DARK)
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        fields: dict[str, tk.Entry] = {}
        labels = [
            ("Flight ID:", "flight_id"),
            ("Origen:", "origin"),
            ("Destino:", "destination"),
            ("Nivel de combustible (0-100):", "fuel_level"),
        ]
        for label_text, key in labels:
            row = tk.Frame(dialog, bg=BG_DARK)
            row.pack(fill="x", padx=14, pady=4)
            tk.Label(
                row, text=label_text, bg=BG_DARK, fg=COLOR_WHITE,
                font=FONT_BODY, width=28, anchor="w",
            ).pack(side="left")
            entry = tk.Entry(
                row, bg=BG_CARD, fg=COLOR_WHITE, font=FONT_BODY,
                insertbackground=COLOR_WHITE, relief="flat",
                highlightthickness=1, highlightcolor=COLOR_CYAN,
                highlightbackground=BG_PANEL,
            )
            entry.pack(side="left", fill="x", expand=True)
            fields[key] = entry

        def _confirm() -> None:
            try:
                flight_id = fields["flight_id"].get().strip()
                origin = fields["origin"].get().strip()
                destination = fields["destination"].get().strip()
                if not flight_id or not origin or not destination:
                    messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=dialog)
                    return
                fuel_level = int(fields["fuel_level"].get().strip())
                self._orchestrator.add_aircraft_to_queue(flight_id, origin, destination, fuel_level)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        tk.Button(
            dialog, text="Confirmar",
            bg=COLOR_GREEN, fg=BG_DARK, font=FONT_BODY,
            relief="flat", cursor="hand2",
            activebackground="#27AE60", activeforeground=BG_DARK,
            command=_confirm,
        ).pack(pady=10)

        dialog.wait_window()
        self.master.master.refresh_all()

    def _land_next(self) -> None:
        try:
            aircraft, runway = self._orchestrator.land_next_aircraft()
            messagebox.showinfo(
                "Aterrizaje autorizado",
                f"Avión {aircraft.flight_id} autorizado\npara aterrizar en pista {runway + 1}.",
                parent=self,
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)
        self.master.master.refresh_all()

    def refresh(self) -> None:
        """Rebuilds the listbox and updates the counter label."""
        status = self._orchestrator.get_system_status()
        count = status["queue_size"]
        self._count_label.config(
            text=f"{count} avión(es) en cola",
            fg=COLOR_YELLOW if count > 0 else COLOR_GRAY,
        )
        self._listbox.delete(0, tk.END)
        for aircraft_str in status["queue"]:
            self._listbox.insert(tk.END, f"  {aircraft_str}")
            idx = self._listbox.size() - 1
            color = COLOR_YELLOW if "emergency" in aircraft_str else COLOR_WHITE
            self._listbox.itemconfig(idx, fg=color)

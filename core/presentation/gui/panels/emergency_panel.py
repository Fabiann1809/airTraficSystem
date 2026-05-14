import tkinter as tk
from tkinter import messagebox

from core.application.atc_orchestrator import ATCOrchestrator
from core.presentation.gui.theme import (
    BG_DARK, BG_PANEL, BG_CARD,
    COLOR_RED, COLOR_WHITE, COLOR_YELLOW, COLOR_CYAN, COLOR_GRAY,
    FONT_TITLE, FONT_BODY, FONT_SMALL,
)


class EmergencyPanel(tk.LabelFrame):
    """Panel that displays the LIFO emergency incident stack with report/resolve controls."""

    def __init__(self, parent: tk.Widget, orchestrator: ATCOrchestrator) -> None:
        super().__init__(
            parent,
            text="Emergencias (LIFO)",
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
            text="0 emergencias activas",
            bg=BG_PANEL,
            fg=COLOR_GRAY,
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

        for text, cmd in [("Reportar emergencia", self._report_emergency), ("Resolver emergencia", self._resolve_emergency)]:
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

    def _report_emergency(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Reportar Emergencia")
        dialog.configure(bg=BG_DARK)
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Severity selector
        sev_row = tk.Frame(dialog, bg=BG_DARK)
        sev_row.pack(fill="x", padx=14, pady=6)
        tk.Label(
            sev_row, text="Severidad:", bg=BG_DARK, fg=COLOR_WHITE,
            font=FONT_BODY, width=14, anchor="w",
        ).pack(side="left")
        severity_var = tk.StringVar(value="1")
        option_menu = tk.OptionMenu(sev_row, severity_var, "1", "2", "3")
        option_menu.configure(
            bg=BG_CARD, fg=COLOR_WHITE, font=FONT_BODY,
            relief="flat", highlightthickness=0,
            activebackground=BG_CARD, activeforeground=COLOR_CYAN,
        )
        option_menu["menu"].configure(bg=BG_CARD, fg=COLOR_WHITE, font=FONT_BODY)
        option_menu.pack(side="left", padx=4)

        # Description
        desc_row = tk.Frame(dialog, bg=BG_DARK)
        desc_row.pack(fill="x", padx=14, pady=6)
        tk.Label(
            desc_row, text="Descripción:", bg=BG_DARK, fg=COLOR_WHITE,
            font=FONT_BODY, width=14, anchor="w",
        ).pack(side="left")
        desc_entry = tk.Entry(
            desc_row, bg=BG_CARD, fg=COLOR_WHITE, font=FONT_BODY,
            insertbackground=COLOR_WHITE, relief="flat", width=32,
            highlightthickness=1, highlightcolor=COLOR_CYAN,
            highlightbackground=BG_PANEL,
        )
        desc_entry.pack(side="left", fill="x", expand=True)

        def _confirm() -> None:
            description = desc_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "La descripción es obligatoria.", parent=dialog)
                return
            try:
                self._orchestrator.report_emergency(int(severity_var.get()), description)
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        tk.Button(
            dialog, text="Confirmar",
            bg=COLOR_RED, fg=COLOR_WHITE, font=FONT_BODY,
            relief="flat", cursor="hand2",
            activebackground="#C0392B", activeforeground=COLOR_WHITE,
            command=_confirm,
        ).pack(pady=10)

        dialog.wait_window()
        self.master.master.refresh_all()

    def _resolve_emergency(self) -> None:
        try:
            incident = self._orchestrator.resolve_emergency()
            messagebox.showinfo(
                "Emergencia resuelta",
                f"Incidente resuelto:\n\n{incident}",
                parent=self,
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)
        self.master.master.refresh_all()

    def refresh(self) -> None:
        """Rebuilds the listbox and updates the incident counter label."""
        status = self._orchestrator.get_system_status()
        count = status["incidents_count"]
        self._count_label.config(
            text=f"{count} emergencia(s) activa(s)",
            fg=COLOR_RED if count > 0 else COLOR_GRAY,
        )
        self._listbox.delete(0, tk.END)
        for inc_str in status["incidents"]:
            self._listbox.insert(tk.END, f"  {inc_str}")
            idx = self._listbox.size() - 1
            if "Severidad 3" in inc_str:
                color = COLOR_RED
            elif "Severidad 2" in inc_str:
                color = COLOR_YELLOW
            else:
                color = COLOR_WHITE
            self._listbox.itemconfig(idx, fg=color)

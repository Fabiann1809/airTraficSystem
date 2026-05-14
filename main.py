import sys

from core.application.atc_orchestrator import ATCOrchestrator


def initialize_demo_data(orchestrator: ATCOrchestrator) -> None:
    """Preloads the system with demo waypoints, aircraft, and one active emergency."""
    for wp in ("BOG-01", "CLO-02", "MDE-03", "CTG-04", "BAQ-05"):
        orchestrator.add_waypoint(wp)

    orchestrator.add_aircraft_to_queue("AV001", "BOG", "MDE", 80)
    orchestrator.add_aircraft_to_queue("AV002", "CLO", "CTG", 15)
    orchestrator.add_aircraft_to_queue("AV003", "MDE", "BAQ", 60)

    orchestrator.report_emergency(2, "Fallo en tren de aterrizaje AV002")

    orchestrator._event_log.log_event(
        "Datos de prueba cargados. Sistema listo para operar."
    )


def print_banner() -> None:
    """Prints the ATC system banner to the console."""
    lines = [
        "╔════════════════════════════════════════════╗",
        "║   SISTEMA DE CONTROL DE TRÁFICO AÉREO     ║",
        "║          ATC Project v1.0                  ║",
        "║      Python puro + Tkinter                 ║",
        "╚════════════════════════════════════════════╝",
    ]
    for line in lines:
        print(line)


def main() -> None:
    """Entry point: loads demo data and launches GUI or CLI depending on sys.argv."""
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print_banner()

    orchestrator = ATCOrchestrator()
    initialize_demo_data(orchestrator)

    try:
        if "--cli" in sys.argv:
            from core.presentation.terminal_interface import TerminalInterface
            ui = TerminalInterface(orchestrator)
            ui.start_loop()
        else:
            import tkinter as tk
            from core.presentation.gui.main_window import MainWindow
            app = MainWindow(orchestrator)
            app.mainloop()
    except KeyboardInterrupt:
        print("\nSistema ATC cerrado.")
        sys.exit(0)


if __name__ == "__main__":
    main()

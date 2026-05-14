import os
import sys

from core.application.atc_orchestrator import ATCOrchestrator
from core.domain.entities.aircraft import Aircraft

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

_MENU = f"""{CYAN}
╔══════════════════════════════════════════╗
║    SISTEMA DE CONTROL DE TRÁFICO AÉREO  ║
╠══════════════════════════════════════════╣
║  [1] Agregar avión a cola de espera     ║
║  [2] Aterrizar siguiente avión          ║
║  [3] Reportar emergencia                ║
║  [4] Resolver emergencia activa         ║
║  [5] Navegar plan de vuelo              ║
║  [6] Ciclar radar                       ║
║  [7] Ver estado del sistema             ║
║  [8] Ver log de eventos                 ║
║  [0] Salir                              ║
╚══════════════════════════════════════════╝{RESET}"""


class TerminalInterface:
    """CLI mode for the ATC system, providing a text-based menu loop."""

    def __init__(self, orchestrator: ATCOrchestrator) -> None:
        self._orchestrator = orchestrator
        if sys.platform == "win32":
            os.system("")  # Enable ANSI escape codes on Windows

    def start_loop(self) -> None:
        """Starts the interactive menu loop until the user selects 0 or hits Ctrl+C."""
        _handlers = {
            "1": self._add_aircraft,
            "2": self._land_next,
            "3": self._report_emergency,
            "4": self._resolve_emergency,
            "5": self._navigate_flight_path,
            "6": self._cycle_radar,
            "7": self._show_status,
            "8": self._show_log,
        }
        try:
            while True:
                print(_MENU)
                choice = input(f"{CYAN}Seleccione una opción: {RESET}").strip()
                if choice == "0":
                    self._exit()
                handler = _handlers.get(choice)
                if handler:
                    handler()
                elif choice != "0":
                    print(f"{YELLOW}Opción inválida. Ingrese un número del 0 al 8.{RESET}")
        except KeyboardInterrupt:
            self._exit()

    # ------------------------------------------------------------------ #
    # Option handlers                                                      #
    # ------------------------------------------------------------------ #

    def _add_aircraft(self) -> None:
        print(f"\n{CYAN}─── Agregar avión a cola de espera ───{RESET}")
        try:
            flight_id = input("  Flight ID:                  ").strip()
            origin = input("  Origen:                     ").strip()
            destination = input("  Destino:                    ").strip()
            fuel_level = int(input("  Nivel de combustible (0-100): ").strip())
            aircraft = self._orchestrator.add_aircraft_to_queue(
                flight_id, origin, destination, fuel_level
            )
            print(f"{GREEN}  ✓ Avión agregado: {aircraft}{RESET}")
        except ValueError as e:
            print(f"{RED}  ✗ Error: {e}{RESET}")

    def _land_next(self) -> None:
        print(f"\n{CYAN}─── Aterrizar siguiente avión ───{RESET}")
        try:
            aircraft, runway = self._orchestrator.land_next_aircraft()
            print(
                f"{GREEN}  ✓ {aircraft.flight_id} autorizado para aterrizar "
                f"en pista {runway + 1}{RESET}"
            )
        except ValueError as e:
            print(f"{RED}  ✗ Error: {e}{RESET}")

    def _report_emergency(self) -> None:
        print(f"\n{CYAN}─── Reportar emergencia ───{RESET}")
        try:
            severity = int(input("  Nivel de severidad (1-3): ").strip())
            description = input("  Descripción:               ").strip()
            incident = self._orchestrator.report_emergency(severity, description)
            print(f"{YELLOW}  ⚠ Emergencia reportada: {incident}{RESET}")
        except ValueError as e:
            print(f"{RED}  ✗ Error: {e}{RESET}")

    def _resolve_emergency(self) -> None:
        print(f"\n{CYAN}─── Resolver emergencia activa ───{RESET}")
        try:
            incident = self._orchestrator.resolve_emergency()
            print(f"{GREEN}  ✓ Emergencia resuelta: {incident}{RESET}")
        except ValueError as e:
            print(f"{RED}  ✗ Error: {e}{RESET}")

    def _navigate_flight_path(self) -> None:
        print(f"\n{CYAN}─── Navegar plan de vuelo ───{RESET}")
        status = self._orchestrator.get_system_status()
        waypoints = status["waypoints"]
        current = status["current_waypoint"]
        if waypoints:
            for wp in waypoints:
                marker = f"{CYAN}► {RESET}" if wp == current else "  "
                print(f"  {marker}{wp}")
        else:
            print(f"  {YELLOW}Sin waypoints registrados{RESET}")
        print(f"\n  {CYAN}[1]{RESET} Siguiente  {CYAN}[2]{RESET} Anterior  "
              f"{CYAN}[3]{RESET} Agregar  {CYAN}[4]{RESET} Reiniciar  {CYAN}[0]{RESET} Volver")
        choice = input("  Opción: ").strip()
        try:
            if choice == "1":
                wp = self._orchestrator.navigate_waypoint_forward()
                print(f"{GREEN}  → Navegando a: {wp}{RESET}")
            elif choice == "2":
                wp = self._orchestrator.navigate_waypoint_backward()
                print(f"{GREEN}  ← Regresando a: {wp}{RESET}")
            elif choice == "3":
                coords = input("  Coordenadas: ").strip()
                if coords:
                    self._orchestrator.add_waypoint(coords)
                    print(f"{GREEN}  ✓ Waypoint '{coords}' agregado{RESET}")
            elif choice == "4":
                first = self._orchestrator.reset_waypoint_navigation()
                print(f"{GREEN}  ⟲ Navegación reiniciada → {first}{RESET}")
            elif choice != "0":
                print(f"{YELLOW}  Opción inválida.{RESET}")
        except ValueError as e:
            print(f"{RED}  ✗ {e}{RESET}")

    def _cycle_radar(self) -> None:
        print(f"\n{CYAN}─── Ciclar radar ───{RESET}")
        active = self._orchestrator.get_active_sector()
        print(f"  Sector activo: {CYAN}{active}{RESET}")
        print(f"  {CYAN}[1]{RESET} Siguiente  {CYAN}[2]{RESET} Anterior  {CYAN}[0]{RESET} Volver")
        choice = input("  Opción: ").strip()
        if choice == "1":
            q = self._orchestrator.cycle_radar_forward()
            print(f"{GREEN}  → Cuadrante: {q.name}{RESET}")
        elif choice == "2":
            q = self._orchestrator.cycle_radar_backward()
            print(f"{GREEN}  ← Cuadrante: {q.name}{RESET}")
        elif choice != "0":
            print(f"{YELLOW}  Opción inválida.{RESET}")

    def _show_status(self) -> None:
        status = self._orchestrator.get_system_status()
        print(f"\n{CYAN}╔══ ESTADO DEL SISTEMA ══════════════════╗{RESET}")

        print(f"\n{CYAN}  Pistas de aterrizaje:{RESET}")
        for r in status["runways"]:
            if r["status"] == "Libre":
                icon = f"{GREEN}[LIBRE  ]{RESET}"
                detail = ""
            else:
                icon = f"{RED}[OCUPADA]{RESET}"
                detail = f"  {r['aircraft']}"
            print(f"    Pista {r['index'] + 1}: {icon}{detail}")

        free_count = self._orchestrator.get_free_runway_count()
        inc_count = self._orchestrator.get_incident_count()
        print(f"\n  {CYAN}Resumen:{RESET} Pistas libres {GREEN}{free_count}/4{RESET}  "
              f"Emergencias {RED if inc_count else GREEN}{inc_count}{RESET}")

        print(f"\n{CYAN}  Cola de espera ({status['queue_size']} aviones):{RESET}")
        if status["queue"]:
            for i, ac in enumerate(status["queue"], 1):
                fuel_tag = ""
                if "CRÍTICO" in ac or "emergency" in ac:
                    color, fuel_tag = YELLOW, f" {RED}[CRÍTICO]{RESET}"
                elif "BAJO" in ac:
                    color, fuel_tag = YELLOW, f" {YELLOW}[BAJO]{RESET}"
                else:
                    color = ""
                print(f"    {i}. {color}{ac}{RESET}{fuel_tag}")
        else:
            print(f"    {YELLOW}Cola vacía{RESET}")

        print(f"\n{CYAN}  Emergencias activas ({status['incidents_count']}):{RESET}")
        if status["incidents"]:
            for inc in status["incidents"]:
                print(f"    {RED}{inc}{RESET}")
        else:
            print(f"    {GREEN}Sin emergencias{RESET}")

        print(f"\n{CYAN}  Radar activo:    {status['active_sector'] or 'N/A'}{RESET}")
        print(f"{CYAN}  Waypoint actual: {status['current_waypoint'] or 'Ninguno'}{RESET}")
        if status["waypoints"]:
            print(f"  Plan: {' → '.join(status['waypoints'])}")
        print(f"{CYAN}╚{'═' * 40}╝{RESET}")

    def _show_log(self) -> None:
        status = self._orchestrator.get_system_status()
        print(f"\n{CYAN}╔══ LOG DE EVENTOS ({status['log_size']} entradas) ══╗{RESET}")
        if not status["log"]:
            print(f"  {YELLOW}Log vacío{RESET}")
        else:
            for entry in status["log"]:
                color = RED if "EMERGENCIA" in entry["message"] else ""
                print(f"  {color}[{entry['timestamp']}] {entry['message']}{RESET}")
        print(f"{CYAN}╚{'═' * 40}╝{RESET}")

    def _exit(self) -> None:
        print(f"\n{CYAN}Cerrando sistema ATC. ¡Hasta pronto!{RESET}\n")
        sys.exit(0)

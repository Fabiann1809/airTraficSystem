from datetime import datetime
from typing import Optional

from core.domain.entities.aircraft import Aircraft
from core.domain.entities.incident import Incident
from core.domain.entities.quadrant import Quadrant
from core.domain.mechanisms.airfield_tracker import AirfieldTracker
from core.domain.mechanisms.landing_sequence import LandingSequence
from core.domain.mechanisms.incident_handler import IncidentHandler
from core.domain.mechanisms.flight_path import FlightPath
from core.domain.mechanisms.airspace_scanner import AirspaceScanner
from core.domain.mechanisms.event_log import EventLog


class ATCOrchestrator:
    """Facade that acts as the single entry point for all ATC system operations.

    The presentation layer (GUI and CLI) communicates exclusively through this
    orchestrator, never directly with the underlying data structures.
    """

    def __init__(self) -> None:
        self._airfield = AirfieldTracker(capacity=4)
        self._landing_sequence = LandingSequence()
        self._incident_handler = IncidentHandler()
        self._flight_path = FlightPath()
        self._scanner = AirspaceScanner()
        self._event_log = EventLog()

        for quadrant in [
            Quadrant("Q-001", "Norte"),
            Quadrant("Q-002", "Sur"),
            Quadrant("Q-003", "Este"),
            Quadrant("Q-004", "Oeste"),
        ]:
            self._scanner.initialize_sector(quadrant)

        self._event_log.log_event("Sistema ATC inicializado correctamente")

    # ------------------------------------------------------------------ #
    # Aircraft / Queue                                                     #
    # ------------------------------------------------------------------ #

    def add_aircraft_to_queue(
        self,
        flight_id: str,
        origin: str,
        destination: str,
        fuel_level: int,
    ) -> Aircraft:
        """Validates, creates an Aircraft and adds it to the landing queue."""
        if not (0 <= fuel_level <= 100):
            raise ValueError(
                f"Nivel de combustible inválido: {fuel_level}. "
                "Debe estar entre 0 y 100."
            )
        priority = "emergency" if fuel_level < 20 else "normal"
        aircraft = Aircraft(flight_id, origin, destination, fuel_level, priority)
        self._landing_sequence.enqueue_aircraft(aircraft)
        self._event_log.log_event(
            f"Avión {flight_id} agregado a la cola "
            f"({origin} → {destination}, fuel: {fuel_level}%, {priority})"
        )
        return aircraft

    def land_next_aircraft(self) -> tuple[Aircraft, int]:
        """Dequeues the next aircraft and assigns it to the first free runway.

        Returns a tuple of (aircraft, runway_index).
        """
        if self._landing_sequence.is_empty():
            raise ValueError("No hay aviones en cola de espera")

        aircraft = self._landing_sequence.peek_next()
        runway_index = self._airfield.get_free_runway()

        if runway_index is None:
            occupied = sum(
                1 for r in self._airfield.display_status()
                if r["status"] == "Ocupada"
            )
            raise ValueError(
                f"No hay pistas disponibles. Pistas ocupadas: {occupied}/4"
            )

        self._landing_sequence.dequeue_aircraft()
        self._airfield.assign_runway(runway_index, aircraft)
        self._event_log.log_event(
            f"Avión {aircraft.flight_id} autorizado a aterrizar "
            f"en pista {runway_index + 1}"
        )
        return (aircraft, runway_index)

    def release_runway(self, runway_index: int) -> None:
        """Frees the runway at the given index."""
        self._airfield.release_runway(runway_index)
        self._event_log.log_event(f"Pista {runway_index + 1} liberada")

    # ------------------------------------------------------------------ #
    # Emergencies                                                          #
    # ------------------------------------------------------------------ #

    def report_emergency(self, severity_level: int, description: str) -> Incident:
        """Creates an Incident with an auto-generated ID and pushes it onto the stack."""
        incident_id = f"INC-{datetime.now().strftime('%H%M%S%f')}"
        incident = Incident(incident_id, severity_level, description)
        self._incident_handler.report_incident(incident)
        self._event_log.log_event(
            f"EMERGENCIA reportada [{incident_id}] "
            f"Severidad {severity_level}: {description}"
        )
        return incident

    def resolve_emergency(self) -> Incident:
        """Pops and returns the most recent incident from the stack."""
        if self._incident_handler.is_empty():
            raise ValueError("No hay emergencias activas")
        incident = self._incident_handler.resolve_incident()
        self._event_log.log_event(
            f"Emergencia [{incident.incident_id}] resuelta"
        )
        return incident

    # ------------------------------------------------------------------ #
    # Radar                                                                #
    # ------------------------------------------------------------------ #

    def cycle_radar_forward(self) -> Quadrant:
        """Advances the radar scanner to the next sector and returns it."""
        quadrant = self._scanner.scan_next_sector()
        self._event_log.log_event(f"Radar → Cuadrante {quadrant.name}")
        return quadrant

    def cycle_radar_backward(self) -> Quadrant:
        """Moves the radar scanner to the previous sector and returns it."""
        quadrant = self._scanner.scan_previous_sector()
        self._event_log.log_event(f"Radar ← Cuadrante {quadrant.name}")
        return quadrant

    def get_active_sector(self) -> Optional[Quadrant]:
        """Returns the currently active radar sector without moving the pointer."""
        return self._scanner.get_active_sector()

    # ------------------------------------------------------------------ #
    # Flight path                                                          #
    # ------------------------------------------------------------------ #

    def add_waypoint(self, coordinates: str) -> None:
        """Appends a waypoint to the flight path."""
        self._flight_path.add_waypoint(coordinates)
        self._event_log.log_event(f"Waypoint agregado: {coordinates}")

    def navigate_waypoint_forward(self) -> str:
        """Advances to the next waypoint and returns its coordinates."""
        result = self._flight_path.navigate_forward()
        if result is None:
            raise ValueError("No hay waypoint siguiente en el plan de vuelo")
        self._event_log.log_event(f"Navegación → {result}")
        return result

    def navigate_waypoint_backward(self) -> str:
        """Moves to the previous waypoint and returns its coordinates."""
        result = self._flight_path.navigate_backward()
        if result is None:
            raise ValueError("No hay waypoint anterior en el plan de vuelo")
        self._event_log.log_event(f"Navegación ← {result}")
        return result

    def get_current_waypoint(self) -> Optional[str]:
        """Returns the current waypoint coordinates without navigating."""
        return self._flight_path.get_current()

    # ------------------------------------------------------------------ #
    # System status                                                        #
    # ------------------------------------------------------------------ #

    def reset_waypoint_navigation(self) -> Optional[str]:
        """Resets the flight path navigation pointer to the first waypoint."""
        self._flight_path.reset_navigation()
        current = self._flight_path.get_current()
        if current:
            self._event_log.log_event(
                f"Navegación reiniciada al waypoint inicial: {current}"
            )
        return current

    def get_incident_count(self) -> int:
        """Returns the number of unresolved incidents currently on the stack."""
        return self._incident_handler.size()

    def get_free_runway_count(self) -> int:
        """Returns the number of runways available for landing right now."""
        return self._airfield.free_count()

    # ------------------------------------------------------------------ #
    # System status                                                        #
    # ------------------------------------------------------------------ #

    def get_system_status(self) -> dict:
        """Returns a complete snapshot of the current system state."""
        stack_copy = self._incident_handler.display_stack()
        active_incident = self._incident_handler.get_active_incident()
        active_sector = self._scanner.get_active_sector()

        return {
            "queue_size": self._landing_sequence.size(),
            "queue": [str(a) for a in self._landing_sequence.display_queue()],
            "incidents_count": self._incident_handler.size(),
            "incidents": [str(i) for i in reversed(stack_copy)],
            "active_incident": str(active_incident) if active_incident else None,
            "active_sector": str(active_sector) if active_sector else None,
            "current_waypoint": self._flight_path.get_current(),
            "waypoints": self._flight_path.display_path(),
            "runways": self._airfield.display_status(),
            "log": self._event_log.display_log(),
            "log_size": self._event_log.size(),
        }

from dataclasses import dataclass, field


@dataclass
class Aircraft:
    """Represents an aircraft in the air traffic control system."""

    flight_id: str
    origin: str
    destination: str
    fuel_level: int
    priority: str = "normal"

    def __post_init__(self) -> None:
        if self.priority not in ("normal", "emergency"):
            raise ValueError(
                f"Prioridad inválida '{self.priority}'. Debe ser 'normal' o 'emergency'."
            )
        if self.fuel_level < 20:
            self.priority = "emergency"

    def __str__(self) -> str:
        return (
            f"{self.flight_id} | {self.origin} → {self.destination} "
            f"| Fuel: {self.fuel_level}% | {self.priority}"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def is_emergency(self) -> bool:
        """Returns True if this aircraft has emergency landing priority."""
        return self.priority == "emergency"

    def fuel_status(self) -> str:
        """Returns a human-readable fuel level label in Spanish."""
        if self.fuel_level < 20:
            return "CRÍTICO"
        if self.fuel_level < 40:
            return "BAJO"
        if self.fuel_level < 70:
            return "NORMAL"
        return "ÓPTIMO"

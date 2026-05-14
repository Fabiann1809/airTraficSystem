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

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Incident:
    """Represents an emergency incident in the air traffic control system."""

    incident_id: str
    severity_level: int
    description: str
    timestamp: str = field(
        default_factory=lambda: datetime.now().strftime("%H:%M:%S")
    )

    def __post_init__(self) -> None:
        if self.severity_level not in (1, 2, 3):
            raise ValueError(
                f"Nivel de severidad inválido '{self.severity_level}'. Debe ser 1, 2 o 3."
            )

    def __str__(self) -> str:
        return (
            f"[{self.incident_id}] Severidad {self.severity_level}: "
            f"{self.description} ({self.timestamp})"
        )

    def __repr__(self) -> str:
        return self.__str__()

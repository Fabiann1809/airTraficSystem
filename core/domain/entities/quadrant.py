from dataclasses import dataclass, field


@dataclass
class Quadrant:
    """Represents a radar monitoring quadrant in the airspace."""

    quadrant_id: str
    name: str
    aircraft_count: int = 0

    def __str__(self) -> str:
        return f"Cuadrante {self.name} ({self.quadrant_id}) | Aeronaves: {self.aircraft_count}"

    def __repr__(self) -> str:
        return self.__str__()

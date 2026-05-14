from typing import Optional
from core.domain.entities.aircraft import Aircraft


class AirfieldTracker:
    """Static array structure that tracks the occupancy state of runways.

    Emulates a fixed-size array where each index maps to a physical runway.
    Provides O(1) access by index and linear search for a free slot.
    """

    def __init__(self, capacity: int) -> None:
        self._runways: list = [None] * capacity
        self._capacity: int = capacity

    def assign_runway(self, runway_index: int, aircraft: Aircraft) -> None:
        """Assigns an aircraft to the given runway index."""
        if runway_index < 0 or runway_index >= self._capacity:
            raise IndexError(
                f"Índice de pista {runway_index} fuera de rango. "
                f"Capacidad: {self._capacity}."
            )
        if self._runways[runway_index] is not None:
            raise ValueError(
                f"La pista {runway_index} ya está ocupada "
                f"por {self._runways[runway_index]}."
            )
        self._runways[runway_index] = aircraft

    def release_runway(self, runway_index: int) -> None:
        """Frees the runway at the given index."""
        if runway_index < 0 or runway_index >= self._capacity:
            raise IndexError(
                f"Índice de pista {runway_index} fuera de rango. "
                f"Capacidad: {self._capacity}."
            )
        if self._runways[runway_index] is None:
            raise ValueError(f"La pista {runway_index} ya está libre.")
        self._runways[runway_index] = None

    def is_runway_free(self, runway_index: int) -> bool:
        """Returns True if the runway at the given index has no aircraft."""
        return self._runways[runway_index] is None

    def get_free_runway(self) -> Optional[int]:
        """Returns the index of the first free runway, or None if all are occupied."""
        for i in range(self._capacity):
            if self._runways[i] is None:
                return i
        return None

    def display_status(self) -> list[dict]:
        """Returns a list of dicts describing each runway's current state."""
        result = []
        for i in range(self._capacity):
            aircraft = self._runways[i]
            result.append({
                "index": i,
                "status": "Libre" if aircraft is None else "Ocupada",
                "aircraft": str(aircraft) if aircraft is not None else None,
            })
        return result

    def occupied_count(self) -> int:
        """Returns the number of runways currently occupied by an aircraft."""
        return sum(1 for r in self._runways if r is not None)

    def free_count(self) -> int:
        """Returns the number of runways currently available for landing."""
        return self._capacity - self.occupied_count()

    def __len__(self) -> int:
        """Supports len(tracker) — returns the total runway capacity."""
        return self._capacity

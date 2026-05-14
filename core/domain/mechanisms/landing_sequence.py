from typing import Optional
from core.domain.entities.aircraft import Aircraft


class LandingSequence:
    """FIFO queue that manages the landing order of aircraft.

    Implemented manually using a plain Python list as internal storage.
    Aircraft are enqueued at the tail and dequeued from the head,
    ensuring strict first-come first-served landing priority.
    """

    def __init__(self) -> None:
        self._sequence: list[Aircraft] = []

    def enqueue_aircraft(self, aircraft: Aircraft) -> None:
        """Adds an aircraft to the end of the landing queue."""
        self._sequence.append(aircraft)

    def dequeue_aircraft(self) -> Optional[Aircraft]:
        """Removes and returns the first aircraft in the queue. Returns None if empty."""
        if not self._sequence:
            return None
        aircraft = self._sequence[0]
        self._sequence = self._sequence[1:]
        return aircraft

    def peek_next(self) -> Optional[Aircraft]:
        """Returns the first aircraft without removing it. Returns None if empty."""
        if not self._sequence:
            return None
        return self._sequence[0]

    def is_empty(self) -> bool:
        """Returns True if there are no aircraft waiting to land."""
        return len(self._sequence) == 0

    def size(self) -> int:
        """Returns the number of aircraft currently in the queue."""
        return len(self._sequence)

    def display_queue(self) -> list[Aircraft]:
        """Returns a copy of the queue in landing order (front to back)."""
        return list(self._sequence)

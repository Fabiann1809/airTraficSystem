from typing import Optional
from core.domain.entities.incident import Incident


class IncidentHandler:
    """LIFO stack that manages active emergency incidents.

    Implemented manually using a plain Python list as internal storage.
    The most recently reported incident sits at the top and is resolved first,
    reflecting the urgency model of emergency command handling.
    """

    def __init__(self) -> None:
        self._incidents: list[Incident] = []

    def report_incident(self, incident: Incident) -> None:
        """Pushes a new incident onto the top of the stack."""
        self._incidents.append(incident)

    def resolve_incident(self) -> Optional[Incident]:
        """Pops and returns the top incident. Returns None if the stack is empty."""
        if not self._incidents:
            return None
        return self._incidents.pop()

    def get_active_incident(self) -> Optional[Incident]:
        """Returns the top incident without removing it. Returns None if empty."""
        if not self._incidents:
            return None
        return self._incidents[-1]

    def is_empty(self) -> bool:
        """Returns True if there are no active incidents."""
        return len(self._incidents) == 0

    def size(self) -> int:
        """Returns the number of unresolved incidents on the stack."""
        return len(self._incidents)

    def display_stack(self) -> list[Incident]:
        """Returns a copy of the stack. Index 0 is the bottom; last index is the top."""
        return list(self._incidents)

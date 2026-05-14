from typing import Optional
from core.domain.entities.quadrant import Quadrant


class SectorNode:
    """Node of the circular doubly linked list representing one radar sector."""

    def __init__(self, data: Quadrant) -> None:
        self.data: Quadrant = data
        self.next_sector: Optional[SectorNode] = None
        self.previous_sector: Optional[SectorNode] = None


class AirspaceScanner:
    """Circular doubly linked list that cycles through radar sectors indefinitely.

    The circular structure guarantees that next_sector and previous_sector
    are never None once at least one sector exists, enabling an infinite
    monitoring loop without boundary checks.
    """

    def __init__(self) -> None:
        self._active_sector: Optional[SectorNode] = None
        self._count: int = 0

    def initialize_sector(self, quadrant: Quadrant) -> None:
        """Inserts a new sector at the end of the circular ring.

        When the list is empty the single node points to itself in both directions.
        All insertions maintain the circular invariant: no pointer is ever None.
        """
        new_node = SectorNode(quadrant)
        if self._active_sector is None:
            new_node.next_sector = new_node
            new_node.previous_sector = new_node
            self._active_sector = new_node
        else:
            last_node = self._active_sector.previous_sector
            last_node.next_sector = new_node
            new_node.previous_sector = last_node
            new_node.next_sector = self._active_sector
            self._active_sector.previous_sector = new_node
        self._count += 1

    def scan_next_sector(self) -> Optional[Quadrant]:
        """Moves the active sector pointer forward and returns the sector data.

        Returns None only if no sectors have been initialized.
        """
        if self._active_sector is None:
            return None
        self._active_sector = self._active_sector.next_sector
        return self._active_sector.data

    def scan_previous_sector(self) -> Optional[Quadrant]:
        """Moves the active sector pointer backward and returns the sector data.

        Returns None only if no sectors have been initialized.
        """
        if self._active_sector is None:
            return None
        self._active_sector = self._active_sector.previous_sector
        return self._active_sector.data

    def get_active_sector(self) -> Optional[Quadrant]:
        """Returns the data of the currently active sector without moving the pointer."""
        if self._active_sector is None:
            return None
        return self._active_sector.data

    def sector_count(self) -> int:
        """Returns the total number of sectors in the scanner ring."""
        return self._count

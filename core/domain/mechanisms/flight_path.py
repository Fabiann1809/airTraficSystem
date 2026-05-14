from typing import Optional


class WaypointNode:
    """Node of the doubly linked list representing a single waypoint."""

    def __init__(self, coordinates: str) -> None:
        self.coordinates: str = coordinates
        self.next_waypoint: Optional[WaypointNode] = None
        self.previous_waypoint: Optional[WaypointNode] = None


class FlightPath:
    """Doubly linked list that stores and navigates waypoints in a flight plan.

    Bidirectional traversal lets the controller move forward or backward
    through the planned route at any point during a flight.
    """

    def __init__(self) -> None:
        self._head: Optional[WaypointNode] = None
        self._tail: Optional[WaypointNode] = None
        self._current: Optional[WaypointNode] = None

    def add_waypoint(self, coordinates: str) -> None:
        """Appends a new waypoint to the end of the path.

        If the path is empty the new node also becomes the current position.
        """
        new_node = WaypointNode(coordinates)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
            self._current = new_node
        else:
            new_node.previous_waypoint = self._tail
            self._tail.next_waypoint = new_node
            self._tail = new_node

    def navigate_forward(self) -> Optional[str]:
        """Advances the current position one waypoint forward.

        Returns the coordinates of the new position, or None if already at the end.
        """
        if self._current is None or self._current.next_waypoint is None:
            return None
        self._current = self._current.next_waypoint
        return self._current.coordinates

    def navigate_backward(self) -> Optional[str]:
        """Moves the current position one waypoint backward.

        Returns the coordinates of the new position, or None if already at the start.
        """
        if self._current is None or self._current.previous_waypoint is None:
            return None
        self._current = self._current.previous_waypoint
        return self._current.coordinates

    def get_current(self) -> Optional[str]:
        """Returns the coordinates of the current waypoint without moving."""
        if self._current is None:
            return None
        return self._current.coordinates

    def reset_navigation(self) -> None:
        """Resets the current position back to the first waypoint."""
        self._current = self._head

    def is_empty(self) -> bool:
        """Returns True if the flight path has no waypoints."""
        return self._head is None

    def display_path(self) -> list[str]:
        """Returns all waypoint coordinates in order from head to tail."""
        result: list[str] = []
        node = self._head
        while node is not None:
            result.append(node.coordinates)
            node = node.next_waypoint
        return result

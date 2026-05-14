from typing import Optional
from datetime import datetime


class EventNode:
    """Node of the singly linked list representing one log entry."""

    def __init__(self, message: str) -> None:
        self.message: str = message
        self.timestamp: str = datetime.now().strftime("%H:%M:%S")
        self.next_event: Optional[EventNode] = None


class EventLog:
    """Singly linked list that stores a chronological record of system events.

    Events are appended at the tail and can only be traversed from head to tail,
    reflecting the strictly forward nature of time and event history.
    """

    def __init__(self) -> None:
        self._head: Optional[EventNode] = None
        self._tail: Optional[EventNode] = None
        self._size: int = 0

    def log_event(self, message: str) -> None:
        """Appends a new timestamped event to the end of the log."""
        new_node = EventNode(message)
        if self._head is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next_event = new_node  # type: ignore[union-attr]
            self._tail = new_node
        self._size += 1

    def display_log(self) -> list[dict]:
        """Traverses the list from head to tail and returns all entries as dicts."""
        result: list[dict] = []
        node = self._head
        while node is not None:
            result.append({"timestamp": node.timestamp, "message": node.message})
            node = node.next_event
        return result

    def clear_log(self) -> None:
        """Resets the log by discarding all nodes."""
        self._head = None
        self._tail = None
        self._size = 0

    def size(self) -> int:
        """Returns the number of events recorded in the log."""
        return self._size

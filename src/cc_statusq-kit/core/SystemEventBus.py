from typing import Callable, Dict, List, Type, TypeVar

from .SystemEvent import SystemEvent

T = TypeVar("T", bound=SystemEvent)


class SystemEventBus:
    """Bus de eventos propio del Orquestador (independiente de los hijos)."""

    def __init__(self):
        self._subscribers: Dict[Type[SystemEvent], List[Callable]] = {}

    def subscribe(self, event_type: Type[T], callback: Callable[[T], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event: SystemEvent):
        for event_type, callbacks in self._subscribers.items():
            if isinstance(event, event_type):
                for callback in callbacks:
                    callback(event)

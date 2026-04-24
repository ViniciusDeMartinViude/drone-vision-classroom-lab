from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable


class MessageBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> None:
        self._subscribers[topic].append(callback)

    def publish(self, topic: str, message: Any) -> None:
        for callback in self._subscribers.get(topic, []):
            callback(message)

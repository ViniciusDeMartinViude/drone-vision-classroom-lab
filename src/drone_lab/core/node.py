from __future__ import annotations

from drone_lab.core.bus import MessageBus


class Node:
    def __init__(self, name: str, bus: MessageBus) -> None:
        self.name = name
        self.bus = bus

    def log(self, message: str) -> None:
        print(f"[{self.name}] {message}")

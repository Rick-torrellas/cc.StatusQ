from typing import Dict, List

from cc.statusq.core.base import Monitorable


class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, Monitorable] = {}

    def add(self, adapter: Monitorable):
        if adapter.get_id() in self._adapters:
            raise ValueError(f"Adapter '{adapter.get_id()}' is already registered.")
        self._adapters[adapter.get_id()] = adapter

    def get_all(self) -> List[Monitorable]:
        return list(self._adapters.values())
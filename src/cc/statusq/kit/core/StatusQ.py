from cc.statusq.core.base import Monitorable, SystemEventBus

from .AdapterRegistry import AdapterRegistry
from .SystemRunner import SystemRunner


class StatusQ:
    def __init__(self, event_bus: SystemEventBus):
        self._event_bus = event_bus
        self.registry = AdapterRegistry()
        self.runner = SystemRunner(self.registry)

    def register_child(self, child: Monitorable):
        self.registry.add(child)

    def telemetry_stream(self, interval: float):
        self.runner.run(interval)

    def pulse_all(self):
        for child in self.registry.get_all():
            child.pulse()
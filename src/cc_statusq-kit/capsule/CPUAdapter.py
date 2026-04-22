from cc_statusq_cpu.core import CPUEventBus, DataReceivedEvent, StatusqCPU

from ..core.Monitorable import Monitorable
from ..core.SystemEvent import HealthReportEvent
from ..core.SystemEventBus import SystemEventBus


class CPUAdapter(Monitorable):

    def __init__(self, cpu_app: StatusqCPU, cpu_bus: CPUEventBus, global_bus: SystemEventBus):
        self.cpu_app = cpu_app
        self.global_bus = global_bus

        cpu_bus.subscribe(DataReceivedEvent, self._translate_to_system)

    def _translate_to_system(self, event: DataReceivedEvent) -> None:
        system_report = HealthReportEvent(
            source=self.get_id(),
            data={
                "load": event.status.total_usage_percentage,
                "temp": event.status.current_temperature,
                "cores": event.status.logical_cores,
            },
        )
        self.global_bus.publish(system_report)

    def get_id(self) -> str:
        return "cpu-monitor"

    def pulse(self) -> None:
        self.cpu_app.run_single_check()

    def start_stream(self, interval: float) -> None:
        self.cpu_app.run_continuous_monitoring(interval=interval)

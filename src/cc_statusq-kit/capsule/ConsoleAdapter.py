from ..core.Monitorable import Monitorable
from ..core.SystemEvent import HealthReportEvent
from ..core.SystemEventBus import SystemEventBus


class ConsoleAdapter(Monitorable):

    def __init__(self, global_bus: SystemEventBus):
        self.global_bus = global_bus
        self.global_bus.subscribe(HealthReportEvent, self._handle_report)

    def _handle_report(self, event: HealthReportEvent) -> None:
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"[{timestamp}] 📢 REPORT RECEIVED FROM: {event.source}")
        for key, value in event.data.items():
            print(f"   |-- {key}: {value}")
        print("-" * 40)

    def get_id(self) -> str:
        return "console-logger"

    def pulse(self) -> None:
        print("🔍 ConsoleLogger: System pulsed.")

    def start_stream(self, interval: float) -> None:
        print(f"🚀 ConsoleLogger: Listening to data stream (interval: {interval}s)...")

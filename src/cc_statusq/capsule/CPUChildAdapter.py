from core.Monitorable import Monitorable
from statusq_cpu.core.StatusqCPU import StatusqCPU  # El hijo


class CPUChildAdapter(Monitorable):
    """Adapta la aplicación StatusqCPU al contrato del Orquestador."""
    def __init__(self, cpu_app: StatusqCPU):
        self.cpu_app = cpu_app

    def get_id(self) -> str:
        return "cpu-monitor"

    def pulse(self) -> None:
        self.cpu_app.run_single_check()

    def start_stream(self, interval: float) -> None:
        self.cpu_app.run_continuous_monitoring(interval=interval)
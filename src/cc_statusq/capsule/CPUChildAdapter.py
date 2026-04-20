from cc_statusq_cpu.core import CPUEventBus, DataReceivedEvent, StatusqCPU

from ..core.Monitorable import Monitorable
from ..core.SystemEvent import HealthReportEvent
from ..core.SystemEventBus import SystemEventBus


class CPUChildAdapter(Monitorable):
    """Adapta la aplicación StatusqCPU al contrato del Orquestador."""
    
    def __init__(self, cpu_app: StatusqCPU, cpu_bus: CPUEventBus, global_bus: SystemEventBus):
        self.cpu_app = cpu_app
        self.global_bus = global_bus
        
        # 1. El adaptador se "engancha" al bus de la app hija.
        # Esto es lo que evita meter el bus dentro de StatusqCPU directamente.
        cpu_bus.subscribe(DataReceivedEvent, self._translate_to_system)

    def _translate_to_system(self, event: DataReceivedEvent) -> None:
        """Convierte eventos específicos de CPU en eventos generales de sistema."""
        system_report = HealthReportEvent(
            source=self.get_id(),
            data={
                "load": event.status.total_usage_percentage,
                "temp": event.status.current_temperature,
                "cores": event.status.logical_cores
            }
        )
        # 2. Publica el reporte en el bus de la Aplicación Madre (StatusQ)
        self.global_bus.publish(system_report)

    def get_id(self) -> str:
        return "cpu-monitor"

    def pulse(self) -> None:
        # El orquestador pide un pulso, nosotros disparamos la lógica del hijo
        self.cpu_app.run_single_check()

    def start_stream(self, interval: float) -> None:
        # El orquestador inicia el hilo, nosotros activamos el monitoreo continuo
        self.cpu_app.run_continuous_monitoring(interval=interval)
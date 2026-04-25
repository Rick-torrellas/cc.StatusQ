import time

from cc.statusq.core.base import Monitorable, SystemEventBus
from cc.statusq.core.events import HealthReportEvent, SystemShutdownEvent
from cc.statusq.cpu.core import CPUEventBus, DataReceivedEvent, StatusqCPU


class CPUAdapter(Monitorable):
    def __init__(self, cpu_app: StatusqCPU, cpu_bus: CPUEventBus, global_bus: SystemEventBus):
        self.cpu_app = cpu_app
        self.global_bus = global_bus
        self._running = True  

        cpu_bus.subscribe(DataReceivedEvent, self._translate_to_system)
        
        self.global_bus.subscribe(SystemShutdownEvent, self._handle_shutdown)

    def _handle_shutdown(self, event: SystemShutdownEvent) -> None:
        
        self._running = False

    def _translate_to_system(self, event: DataReceivedEvent) -> None:
        status = event.status
        
        system_report = HealthReportEvent(
            source=self.get_id(),
            data={
                # Uso y Carga
                "load_total": status.total_usage_percentage,
                "load_per_cpu": status.per_cpu_usage_percentage,  # Lista de % por núcleo
                "load_avg": getattr(status, "load_average", "N/A"), # Carga 1, 5, 15 min
                
                # Frecuencias (en MHz)
                "freq_current": status.current_frequency,
                "freq_min": status.min_frequency,
                "freq_max": status.max_frequency,
                
                # Hardware y Estado
                "temp": status.current_temperature,
                "cores_logical": status.logical_cores,
                "cores_physical": status.physical_cores,
                
                # Estadísticas de Contexto (si están disponibles)
                "ctx_switches": getattr(status, "context_switches", 0),
                "interrupts": getattr(status, "interrupts", 0),
                "soft_interrupts": getattr(status, "soft_interrupts", 0),
                "syscalls": getattr(status, "syscalls", 0),
            },
        )
        self.global_bus.publish(system_report)

    def get_id(self) -> str:
        return "cpu-monitor"

    @property
    def requires_main_thread(self) -> bool:
        """Este adaptador es un worker, no necesita el hilo principal."""
        return False

    def pulse(self) -> None:
        self.cpu_app.run_single_check()

    def start_stream(self, interval: float) -> None:
        """
        Bucle de streaming controlado. 
        Sustituimos el método automático por uno que respeta self._running.
        """
        while self._running:
            self.cpu_app.run_single_check()
            time.sleep(interval)
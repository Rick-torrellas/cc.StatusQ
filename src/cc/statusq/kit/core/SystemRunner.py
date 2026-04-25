import threading
import time

from .AdapterRegistry import AdapterRegistry


class SystemRunner:
    def __init__(self, registry: AdapterRegistry):
        self.registry = registry

    def run(self, interval: float):
        all_adapters = self.registry.get_all()
        
        # 1. Separamos quién bloquea y quién no
        blockers = [a for a in all_adapters if a.requires_main_thread]
        workers = [a for a in all_adapters if not a.requires_main_thread]

        # 2. Lanzamos los trabajadores en hilos secundarios (daemons)
        for adapter in workers:
            t = threading.Thread(
                target=adapter.start_stream, 
                args=(interval,), 
                daemon=True,
                name=f"Thread-{adapter.get_id()}"
            )
            t.start()

        # 3. Ejecutamos el bloqueante en el hilo principal
        if blockers:
            # Si hay varios, el primero toma el control
            blockers[0].start_stream(interval)
        else:
            # Si no hay UI, mantenemos vivo el proceso principal manualmente
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nSaliendo limpiamente...")
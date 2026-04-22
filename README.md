# cc.StatusQ-kit

> Efficient monitoring and management of CPU status.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Rick-torrellas/cc.StatusQ-kit/badges/version.json)
![test](https://github.com/Rick-torrellas/cc.StatusQ-kit/actions/workflows/main.yaml/badge.svg)(https://github.com/Rick-torrellas/cc.StatusQ-kit/actions/workflows/main.yaml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Download](https://img.shields.io/github/v/release/Rick-torrellas/cc.StatusQ-kit?label=Download&color=orange)](https://github.com/Rick-torrellas/cc.StatusQ-kit/releases)
[![docs](https://img.shields.io/badge/docs-read_now-blue?style=flat-square)](https://rick-torrellas.github.io/cc-book-kit/)
[![Ask DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue?logo=gitbook&logoColor=white)](https://deepwiki.com/Rick-torrellas/cc.StatusQ-kit)

## 📖 Description

StatusQ is a modular, event-driven monitoring engine designed to decouple system data collection from the presentation layer. Built on a robust Event Bus (Pub-Sub) architecture, it allows you to observe system metrics (like CPU, Memory, or Network) through a platform-agnostic core.

---

## Installation

```
pip install cc.statusq-kit
```

---

## Usage

```python
from cc_statusq_cpu.core import StatusqCPU, CPUEventBus
from cc_statusq_cpu.capsule import PsutilCPUProvider
from cc_statusq_kit.core.StatusQ import StatusQ
from cc_statusq_kit.core.SystemEventBus import SystemEventBus
from cc_statusq_kit.capsule.CPUAdapter import CPUAdapter
from cc_statusq_kit.capsule.ConsoleAdapter import ConsoleAdapter

# 1. Initialize the Global System Event Bus
global_bus = SystemEventBus()
cpu_provider = PsutilCPUProvider()
# 2. Initialize Sub-system components (Specific to CPU Library)
cpu_bus = CPUEventBus()
cpu_app = StatusqCPU(provider=cpu_provider,event_bus=cpu_bus)
# 3. Create the Orchestrator
orchestrator = StatusQ(event_bus=global_bus)
# 4. Initialize and Register Adapters
# The ConsoleAdapter listens for HealthReportEvents on the global bus
console = ConsoleAdapter(global_bus=global_bus)

# The CPUAdapter translates specific CPU events into global HealthReportEvents
cpu_monitor = CPUAdapter(cpu_app=cpu_app, cpu_bus=cpu_bus, global_bus=global_bus)
orchestrator.register_child(console)
orchestrator.register_child(cpu_monitor)
# --- EXECUTION MODES ---
# MODE A: Single Pulse (Manual check)
print("--- Executing Single Pulse ---")
orchestrator.pulse_all()
# MODE B: Continuous Telemetry Stream (Multi-threaded)
print("\n--- Starting Telemetry Stream (Press Ctrl+C to stop) ---")
try:
    # Starts a background thread for each child to stream data every 2 seconds
    orchestrator.telemetry_stream(interval=2.0)
except KeyboardInterrupt:
    print("\nStopping orchestrator...")
```

---

## 📈 System Flow

* Registration: Adapters are added to the StatusQ child list.
* Trigger: When pulse_all() or telemetry_stream() is called, the orchestrator invokes the corresponding methods on the adapters.
* Translation: The CPUAdapter captures hardware data and publishes a HealthReportEvent to the SystemEventBus.
* Consumption: The ConsoleAdapter receives the event via the bus and displays the formatted metrics.

---
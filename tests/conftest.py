from unittest.mock import MagicMock

import pytest
from adapters.ConsoleLogAdapter import ConsoleLoggerAdapter
from adapters.CPUChildAdapter import CPUChildAdapter
from core.StatusQ import StatusQ
from core.SystemEvent import HealthReportEvent

# Importaciones del proyecto (ajusta el path según tu estructura de carpetas)
from core.SystemEventBus import SystemEventBus


@pytest.fixture
def event_bus():
    """Proporciona una instancia limpia del bus de eventos global."""
    return SystemEventBus()


@pytest.fixture
def statusq_app(event_bus):
    """Proporciona la instancia del orquestador principal."""
    return StatusQ(event_bus=event_bus)


@pytest.fixture
def mock_cpu_app():
    """
    Simula la aplicación hija StatusqCPU (externa).
    Permite verificar si se llaman a run_single_check o run_continuous_monitoring.
    """
    mock = MagicMock()
    # Podrías añadir lógica aquí si necesitas que devuelva valores específicos
    return mock


@pytest.fixture
def mock_cpu_bus():
    """Simula el bus de eventos interno de la aplicación CPU."""
    return MagicMock()


@pytest.fixture
def cpu_adapter(mock_cpu_app, mock_cpu_bus, event_bus):
    """Instancia del adaptador de CPU configurado con mocks."""
    return CPUChildAdapter(
        cpu_app=mock_cpu_app, 
        cpu_bus=mock_cpu_bus, 
        global_bus=event_bus
    )


@pytest.fixture
def console_adapter(event_bus):
    """Instancia del adaptador de consola."""
    return ConsoleLoggerAdapter(global_bus=event_bus)


@pytest.fixture
def sample_health_report():
    """Genera un evento de salud genérico para pruebas de integración."""
    return HealthReportEvent(
        source="test-source",
        data={"metric_a": 10, "metric_b": 0.5}
    )
from unittest.mock import MagicMock

import pytest
from cc_statusq_kit.core import HealthReportEvent, StatusQ, SystemEventBus


@pytest.fixture
def global_event_bus():
    """
    Provides a clean instance of the SystemEventBus for each test.
    This ensures that subscriptions from one test don't leak into another.
    """
    return SystemEventBus()

@pytest.fixture
def statusq_orchestrator(global_event_bus):
    """
    Provides an instance of the StatusQ orchestrator initialized with 
    a fresh global event bus.
    """
    return StatusQ(event_bus=global_event_bus)

@pytest.fixture
def mock_cpu_app():
    """
    Mocks the StatusqCPU external dependency.
    This allows us to test the CPUAdapter without the actual 
    cc_statusq_cpu library installed.
    """
    mock_app = MagicMock()
    # Mocking the ID or any specific behavior needed
    mock_app.run_single_check = MagicMock()
    mock_app.run_continuous_monitoring = MagicMock()
    return mock_app

@pytest.fixture
def mock_cpu_bus():
    """
    Mocks the CPUEventBus used by the daughter application.
    This is useful for triggering DataReceivedEvents manually in tests.
    """
    return MagicMock()

@pytest.fixture
def sample_health_data():
    """
    Provides a standard dictionary of health data for assertions.
    """
    return {
        "load": 45.5,
        "temp": 60.0,
        "cores": 8
    }

@pytest.fixture
def sample_health_event(sample_health_data):
    """
    Provides a pre-configured HealthReportEvent.
    """
    return HealthReportEvent(
        source="test-monitor",
        data=sample_health_data
    )
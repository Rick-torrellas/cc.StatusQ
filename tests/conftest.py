from unittest.mock import MagicMock

import pytest

from .Monitorable import Monitorable
from .StatusQ import StatusQ

# Importing from your core structure
from .SystemEventBus import SystemEventBus


@pytest.fixture
def event_bus() -> SystemEventBus:
    """
    Provides a clean instance of the SystemEventBus for each test.
    This ensures no event leakage between test cases.
    """
    return SystemEventBus()

@pytest.fixture
def orchestrator(event_bus: SystemEventBus) -> StatusQ:
    """
    Provides the StatusQ (Mother Application) initialized with a clean bus.
    """
    return StatusQ(event_bus=event_bus)

@pytest.fixture
def mock_child() -> MagicMock:
    """
    Creates a mock that adheres to the Monitorable Protocol.
    Useful for testing if StatusQ correctly triggers child methods.
    """
    child = MagicMock(spec=Monitorable)
    child.get_id.return_value = "mock-adapter"
    return child

@pytest.fixture
def spy_callback() -> MagicMock:
    """
    A generic spy function to subscribe to the bus and verify 
    if events are actually being published.
    """
    return MagicMock()

@pytest.fixture
def sample_health_data() -> dict:
    """
    Provides consistent mock data for HealthReportEvent testing.
    """
    return {
        "load": 15.5,
        "temp": 42.0,
        "cores": 8
    }
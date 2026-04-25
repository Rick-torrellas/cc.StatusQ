from unittest.mock import MagicMock

from cc.statusq.core.events import HealthReportEvent

from cc.statusq.kit.capsule import CPUAdapter


# Using a dummy class to simulate the DataReceivedEvent from the daughter app
class MockDataReceivedEvent:
    def __init__(self, usage, temp, cores):
        self.status = MagicMock()
        self.status.total_usage_percentage = usage
        self.status.current_temperature = temp
        self.status.logical_cores = cores


def test_cpu_adapter_initialization_subscribes_to_cpu_bus(mock_cpu_app, mock_cpu_bus, global_event_bus):
    """
    Test that CPUAdapter subscribes to DataReceivedEvent on the CPU bus during init.
    """
    from cc_statusq_cpu.core import DataReceivedEvent

    adapter = CPUAdapter(cpu_app=mock_cpu_app, cpu_bus=mock_cpu_bus, global_bus=global_event_bus)

    # Verify the adapter registered its translation method to the local CPU bus
    mock_cpu_bus.subscribe.assert_called_once_with(DataReceivedEvent, adapter._translate_to_system)


def test_cpu_adapter_get_id(mock_cpu_app, mock_cpu_bus, global_event_bus):
    """
    Verify the adapter ID is correctly set.
    """
    adapter = CPUAdapter(mock_cpu_app, mock_cpu_bus, global_event_bus)
    assert adapter.get_id() == "cpu-monitor"


def test_cpu_adapter_translation_logic(mock_cpu_app, mock_cpu_bus, global_event_bus):
    """
    Test the core logic: receiving a local CPU event should publish
    a HealthReportEvent on the global bus with mapped data.
    """
    adapter = CPUAdapter(mock_cpu_app, mock_cpu_bus, global_event_bus)

    # Mocking the incoming event from the CPU library
    mock_local_event = MockDataReceivedEvent(usage=25.0, temp=55.5, cores=4)

    # We spy on the global bus publish method
    global_event_bus.publish = MagicMock()

    # Trigger the translation manually
    adapter._translate_to_system(mock_local_event)

    # Capture the argument passed to publish
    global_event_bus.publish.assert_called_once()
    published_event = global_event_bus.publish.call_args[0][0]

    # Assertions on the published HealthReportEvent
    assert isinstance(published_event, HealthReportEvent)
    assert published_event.source == "cpu-monitor"
    assert published_event.data["load"] == 25.0
    assert published_event.data["temp"] == 55.5
    assert published_event.data["cores"] == 4


def test_cpu_adapter_pulse_triggers_app_check(mock_cpu_app, mock_cpu_bus, global_event_bus):
    """
    Verify that calling pulse() on the adapter triggers the underlying
    CPU application's single check.
    """
    adapter = CPUAdapter(mock_cpu_app, mock_cpu_bus, global_event_bus)
    adapter.pulse()

    mock_cpu_app.run_single_check.assert_called_once()


def test_cpu_adapter_start_stream_triggers_continuous_monitoring(mock_cpu_app, mock_cpu_bus, global_event_bus):
    """
    Verify that start_stream() starts the continuous monitoring in the CPU app.
    """
    adapter = CPUAdapter(mock_cpu_app, mock_cpu_bus, global_event_bus)
    test_interval = 2.5

    adapter.start_stream(interval=test_interval)

    mock_cpu_app.run_continuous_monitoring.assert_called_once_with(interval=test_interval)

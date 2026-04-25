from unittest.mock import MagicMock, patch

from cc.statusq.core.events import HealthReportEvent

from cc.statusq.kit.capsule.ConsoleAdapter import ConsoleAdapter


def test_console_adapter_subscription(global_event_bus):
    """
    Test if ConsoleAdapter correctly subscribes to HealthReportEvent
    on the global event bus during initialization.
    """
    # We use a spy/mock for the subscribe method to verify the call
    with patch.object(global_event_bus, "subscribe") as mock_subscribe:
        adapter = ConsoleAdapter(global_bus=global_event_bus)

        # Verify that subscribe was called with HealthReportEvent and the adapter's handler
        mock_subscribe.assert_called_once_with(HealthReportEvent, adapter._handle_report)


def test_console_adapter_get_id():
    """
    Test that the adapter returns the correct hardcoded ID.
    """
    bus = MagicMock()
    adapter = ConsoleAdapter(global_bus=bus)
    assert adapter.get_id() == "console-logger"


def test_console_adapter_handle_report_output(global_event_bus, sample_health_event, capsys):
    """
    Test if _handle_report correctly prints the event data to the console.
    """
    adapter = ConsoleAdapter(global_bus=global_event_bus)

    # Manually trigger the handler with the sample event from conftest
    adapter._handle_report(sample_health_event)

    # Capture the printed output
    captured = capsys.readouterr()

    # Verify the output contains the source and the data keys/values
    assert "REPORT RECEIVED FROM: test-monitor" in captured.out
    assert "load: 45.5" in captured.out
    assert "temp: 60.0" in captured.out
    assert "cores: 8" in captured.out


def test_console_adapter_integration_with_bus(global_event_bus, sample_health_event, capsys):
    """
    Integration test: verify that publishing an event to the bus
    results in a console print via the ConsoleAdapter.
    """
    # Initialize adapter (it subscribes automatically)
    _ = ConsoleAdapter(global_bus=global_event_bus)

    # Publish the event to the global bus
    global_event_bus.publish(sample_health_event)

    # Capture and verify output
    captured = capsys.readouterr()
    assert "REPORT RECEIVED FROM: test-monitor" in captured.out
    assert "load: 45.5" in captured.out


def test_console_adapter_pulse_and_stream_methods(capsys):
    """
    Test the pulse and start_stream methods to ensure they provide feedback.
    """
    bus = MagicMock()
    adapter = ConsoleAdapter(global_bus=bus)

    # Test pulse
    adapter.pulse()
    captured_pulse = capsys.readouterr()
    assert "ConsoleLogger: System pulsed" in captured_pulse.out

    # Test start_stream
    adapter.start_stream(1.0)
    captured_stream = capsys.readouterr()
    assert "Listening to data stream" in captured_stream.out
    assert "1.0s" in captured_stream.out

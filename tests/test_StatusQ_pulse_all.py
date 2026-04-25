from unittest.mock import MagicMock

from cc.statusq.core.events import DiscoveryStartedEvent

from cc.statusq.kit.core import StatusQ


def test_pulse_all_notifies_children(global_event_bus):
    """
    Test that pulse_all calls the pulse method on every registered child.
    """
    orchestrator = StatusQ(event_bus=global_event_bus)

    # Create mock children
    child_1 = MagicMock()
    child_2 = MagicMock()

    # Register children
    orchestrator.register_child(child_1)
    orchestrator.register_child(child_2)

    # Execute pulse_all
    orchestrator.pulse_all()

    # Verify pulse was called on each child
    child_1.pulse.assert_called_once()
    child_2.pulse.assert_called_once()


def test_pulse_all_publishes_discovery_event(global_event_bus):
    """
    Test that pulse_all publishes a DiscoveryStartedEvent to the bus
    with the correct number of registered children.
    """
    orchestrator = StatusQ(event_bus=global_event_bus)

    # Spy on the event bus publish method
    with MagicMock() as mock_callback:
        # Subscribe to DiscoveryStartedEvent to catch the publication
        global_event_bus.subscribe(DiscoveryStartedEvent, mock_callback)

        # Register 3 dummy children
        for _ in range(3):
            orchestrator.register_child(MagicMock())

        orchestrator.pulse_all()

        # Verify the event was published with count=3
        mock_callback.assert_called_once()
        event_received = mock_callback.call_args[0][0]
        assert isinstance(event_received, DiscoveryStartedEvent)
        assert event_received.count == 3


def test_pulse_all_with_no_children(global_event_bus):
    """
    Test that pulse_all still publishes a discovery event even
    if no children are registered.
    """
    orchestrator = StatusQ(event_bus=global_event_bus)
    mock_callback = MagicMock()
    global_event_bus.subscribe(DiscoveryStartedEvent, mock_callback)

    orchestrator.pulse_all()

    # Verify event published with count 0
    event_received = mock_callback.call_args[0][0]
    assert event_received.count == 0

from unittest.mock import MagicMock

from cc.statusq.core.base import Monitorable


def test_register_single_child(statusq_orchestrator):
    """
    Test that a single child is correctly added to the internal list.
    """
    # Create a mock that implements the Monitorable protocol
    mock_child = MagicMock(spec=Monitorable)

    # Register the child
    statusq_orchestrator.register_child(mock_child)

    # Verify the child is in the list
    assert len(statusq_orchestrator._children) == 1
    assert mock_child in statusq_orchestrator._children


def test_register_multiple_children(statusq_orchestrator):
    """
    Test that multiple children can be registered and the order is preserved.
    """
    child_a = MagicMock(spec=Monitorable)
    child_b = MagicMock(spec=Monitorable)

    statusq_orchestrator.register_child(child_a)
    statusq_orchestrator.register_child(child_b)

    assert len(statusq_orchestrator._children) == 2
    assert statusq_orchestrator._children[0] == child_a
    assert statusq_orchestrator._children[1] == child_b


def test_pulse_all_triggers_registered_children(statusq_orchestrator, global_event_bus):
    """
    Integration test: verify that pulse_all calls the pulse method
    of all registered children.
    """
    child_1 = MagicMock(spec=Monitorable)
    child_2 = MagicMock(spec=Monitorable)

    statusq_orchestrator.register_child(child_1)
    statusq_orchestrator.register_child(child_2)

    # Execute pulse_all
    statusq_orchestrator.pulse_all()

    # Verify that each child's pulse method was called exactly once
    child_1.pulse.assert_called_once()
    child_2.pulse.assert_called_once()


def test_register_child_type_integrity(statusq_orchestrator):
    """
    Verify that the registered child maintains its interface.
    """
    mock_child = MagicMock(spec=Monitorable)
    mock_child.get_id.return_value = "test-adapter"

    statusq_orchestrator.register_child(mock_child)

    # Retrieve from internal list and check behavior
    registered_child = statusq_orchestrator._children[0]
    assert registered_child.get_id() == "test-adapter"

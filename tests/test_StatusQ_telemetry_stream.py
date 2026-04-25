from unittest.mock import MagicMock, patch

import pytest

from cc.statusq.kit.core import StatusQ


class MockChild:
    """Helper mock class that implements Monitorable protocol."""

    def __init__(self, child_id):
        self.child_id = child_id
        self.start_stream_called = False
        self.received_interval = None

    def get_id(self) -> str:
        return self.child_id

    def pulse(self) -> None:
        pass

    def start_stream(self, interval: float) -> None:
        self.start_stream_called = True
        self.received_interval = interval


def test_telemetry_stream_starts_threads_for_all_children(global_event_bus):
    """
    Test that telemetry_stream correctly triggers start_stream
    on all registered children using threads.
    """
    orchestrator = StatusQ(event_bus=global_event_bus)

    # Create multiple mock children
    child1 = MockChild("child-1")
    child2 = MockChild("child-2")

    orchestrator.register_child(child1)
    orchestrator.register_child(child2)

    # We patch 'threading.Thread' to avoid actual blocking and
    # to verify how threads are instantiated.
    with patch("threading.Thread") as MockThread:
        # Mock the instance of the thread
        mock_thread_instance = MagicMock()
        MockThread.return_value = mock_thread_instance

        # Call the method under test
        interval = 2.0
        orchestrator.telemetry_stream(interval)

        # Verify a Thread was created for each child
        assert MockThread.call_count == 2

        # Verify start() and join() were called on each thread
        assert mock_thread_instance.start.call_count == 2
        assert mock_thread_instance.join.call_count == 2

        # Verify the arguments passed to the Thread constructor for the first child
        # target should be child.start_stream and args should be (interval,)
        args, kwargs = MockThread.call_args_list[0]
        assert kwargs["target"] == child1.start_stream
        assert kwargs["args"] == (interval,)
        assert kwargs["daemon"] is True


def test_telemetry_stream_with_no_children(global_event_bus):
    """
    Ensure telemetry_stream does not fail if no children are registered.
    """
    orchestrator = StatusQ(event_bus=global_event_bus)

    with patch("threading.Thread") as MockThread:
        orchestrator.telemetry_stream(1.0)
        MockThread.assert_not_called()


@pytest.mark.timeout(2)  # Safety timeout
def test_telemetry_stream_real_execution_logic(global_event_bus):
    """
    A more functional test using real threads but with immediate return
    to verify the interaction without mocking the Thread class itself.
    """
    orchestrator = StatusQ(event_bus=global_event_bus)
    child = MockChild("real-thread-test")
    orchestrator.register_child(child)

    # In this case, since MockChild.start_stream returns immediately,
    # join() will also return immediately.
    orchestrator.telemetry_stream(0.5)

    assert child.start_stream_called is True
    assert child.received_interval == 0.5

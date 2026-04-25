from cc.statusq.core.base import Monitorable, SystemEventBus
from cc.statusq.core.events import HealthReportEvent
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import DataTable, Footer, Header, Log


class HealthDashboard(App):
    """Internal Textual App that manages the TUI rendering."""
    TITLE = "StatusQ System Monitor"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            DataTable(id="metrics-table"),
            Log(id="event-log"),
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Source", "Metric", "Value", "Timestamp")

    def update_ui(self, event: HealthReportEvent) -> None:
        """Updates the TUI widgets with data from the event bus."""
        timestamp = event.timestamp.strftime("%H:%M:%S")
        table = self.query_one(DataTable)
        log = self.query_one(Log)

        log.write_line(f"New data from: {event.source}")
        
        for key, value in event.data.items():
            table.add_row(event.source, key, str(value), timestamp)

class TextualAdapter(Monitorable):
    """Adapter connecting SystemEventBus to the Textual TUI."""
    
    def __init__(self, global_bus: SystemEventBus):
        self.global_bus = global_bus
        self.app = HealthDashboard()
        # Subscribe to health reports published on the bus
        self.global_bus.subscribe(HealthReportEvent, self._handle_report)

    def _handle_report(self, event: HealthReportEvent) -> None:
        """Thread-safe bridge to update the UI."""
        self.app.call_from_thread(self.app.update_ui, event)

    def get_id(self) -> str:
        return "textual-tui"

    def pulse(self) -> None:
        """Manual trigger implementation."""
        if self.app.is_running:
            self.app.call_from_thread(
                self.app.query_one(Log).write_line, "🔍 Pulse received"
            )

    def start_stream(self, interval: float) -> None:
        """Starts the blocking Textual main loop."""
        self.app.run()
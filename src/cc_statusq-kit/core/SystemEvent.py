from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True, kw_only=True)
class SystemEvent:
    """Base mística para todos los eventos del orquestador."""

    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True, kw_only=True)
class DiscoveryStartedEvent(SystemEvent):
    """Fired cuando el orquestador empieza a buscar aplicaciones hijas."""

    count: int


@dataclass(frozen=True, kw_only=True)
class HealthReportEvent(SystemEvent):
    """Evento que consolida métricas de una aplicación hija."""

    source: str  # e.g., "CPU", "RAM"
    data: Dict[str, Any]

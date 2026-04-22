from typing import Protocol, runtime_checkable


@runtime_checkable
class Monitorable(Protocol):
    """
    Contrato que cualquier 'aplicación hija' debe implementar
    para ser orquestada.
    """

    def get_id(self) -> str: ...
    def pulse(self) -> None: ...  # Equivalente a run_single_check
    def start_stream(self, interval: float) -> None: ...

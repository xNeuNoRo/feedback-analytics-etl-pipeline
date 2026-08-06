from typing import Protocol, List, Tuple, Any


# ... -> es para indicar que puede tener cualquier implementacion, no importa que parametros tenga, solo nos interesa que tenga el metodo extract y que devuelva una lista de tuplas
class IExtractor(Protocol):
    """Contrato para todos los extractores de datos."""

    def extract(self, filepath: str) -> List[Tuple[Any, ...]]:
        ...

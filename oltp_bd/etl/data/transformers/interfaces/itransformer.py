from typing import Protocol, List, Tuple, Any

# ... -> es para indicar que puede tener cualquier implementacion, no importa que parametros tenga, solo nos interesa que tenga el metodo extract y que devuelva una lista de tuplas
class ITransformer(Protocol):
    """Contrato para todas las transformaciones de datos."""

    def transform(self, raw_data: List[Tuple[Any, ...]]) -> List[Tuple[Any, ...]]:
        ...

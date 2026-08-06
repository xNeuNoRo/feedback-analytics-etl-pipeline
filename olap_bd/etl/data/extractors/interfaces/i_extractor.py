from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IExtractor(ABC):
    """
    Interfaz abstracta para los extractores del ETL (de esta forma aplicamos un strategy pattern)
    """

    @abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        """
        Extrae y devuelve una lista de diccionarios con registros crudos.
        """
        pass

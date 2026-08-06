from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ITransformer(ABC):
    """
    Interfaz abstracta para los componentes de Transformacion del ETL.
    Establece el contrato para limpiar datos, aplicar NLP y estructurar las entidades.
    """

    @abstractmethod
    def transform(self, raw_records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Transforma datos en crudo y genera un diccionario con las listas de datos
        para las 5 dimensiones (dim_time, dim_client, dim_product, dim_source, dim_sentiment)
        y para la tabla de hechos (fact_feedbacks).
        """
        pass

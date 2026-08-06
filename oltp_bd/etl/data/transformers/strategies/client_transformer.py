from typing import List, Tuple, Any
from data.transformers.interfaces.itransformer import ITransformer
import pandas as pd


class ClientTransformer(ITransformer):
    """Estrategia de transformación para los clientes."""

    def transform(self, raw_data: List[Tuple[Any, ...]]) -> List[Tuple[Any, ...]]:
        # Inicializamos nuestro listado de tuplas que contendrá los datos limpios y transformados
        cleaned_list: List[Tuple[Any, ...]] = []

        # Iteramos en cada fila de los datos crudos
        for row in raw_data:
            # row[0] es el nombre del cliente y row[1] es el email del cliente
            # Eliminamos espacios en blanco al inicio y al final del nombre
            name = str(row[0]).strip() if pd.notna(row[0]) else ""
            # Eliminamos espacios en blanco y convertimos el email a minúsculas
            email = str(row[1]).strip().lower() if pd.notna(row[1]) else ""

            # Agregamos la tupla limpia a la lista de resultados
            cleaned_list.append((name, email))

        return cleaned_list

from typing import List, Tuple, Any
from data.transformers.interfaces.itransformer import ITransformer
import pandas as pd


class ProductTransformer(ITransformer):
    """Estrategia de transformación para los productos."""

    def transform(self, raw_data: List[Tuple[Any, ...]]) -> List[Tuple[Any, ...]]:
        # Inicializamos nuestro listado de tuplas que contendrá los datos limpios y transformados
        cleaned_list: List[Tuple[Any, ...]] = []

        for row in raw_data:
            # row[0] es Nombre, row[1] es Categoria

            # Eliminamos espacios en blanco al inicio y al final del nombre
            name = str(row[0]).strip() if pd.notna(row[0]) else ""
            # Eliminamos espacios en blanco al inicio y al final de la categoría
            category = str(row[1]).strip() if pd.notna(row[1]) else ""

            # Agregamos la tupla limpia a la lista de resultados
            cleaned_list.append((name, category))

        return cleaned_list

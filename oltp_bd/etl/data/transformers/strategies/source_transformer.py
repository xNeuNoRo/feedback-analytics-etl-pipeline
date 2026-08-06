from typing import List, Tuple, Any
from data.transformers.interfaces.itransformer import ITransformer
import pandas as pd


class SourceTransformer(ITransformer):
    """Estrategia de transformación para las fuentes."""

    def transform(self, raw_data: List[Tuple[Any, ...]]) -> List[Tuple[Any, ...]]:
        # Inicializamos nuestro listado de tuplas que contendrá los datos limpios y transformados
        cleaned_list: List[Tuple[Any, ...]] = []

        for row in raw_data:
            # row[0] es el ID de la fuente, row[1] es el tipo de fuente, row[2] es la fecha
            source_id = str(row[0]).strip().upper() if pd.notna(row[0]) else ""
            source_type = str(row[1]).strip() if pd.notna(row[1]) else ""
            upload_date = str(row[2]).strip() if pd.notna(row[2]) else None

            # Agregamos la tupla limpia a la lista de resultados
            cleaned_list.append((source_id, source_type, upload_date))

        return cleaned_list

import pandas as pd
from typing import List, Tuple, Any


class CsvExtractor:
    """
    Clase encargada de extraer datos de archivos CSV
    """

    def extract_columns(self, filepath: str, required_columns: List[str]) -> List[Tuple[Any, ...]]:
        """
        Lee cualquier CSV y extrae unicamente las columnas solicitadas en formato de tuplas.    
        """
        # Leemos el CSV usando pandas
        df = pd.read_csv(filepath)

        # Filtramos nulos basandonos en las columnas que nos pidieron
        df = df.dropna(subset=required_columns)

        # Devolvemos una lista de tuplas con los datos de las columnas requeridas
        return list(df[required_columns].itertuples(index=False, name=None))

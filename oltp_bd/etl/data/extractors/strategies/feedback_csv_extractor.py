import pandas as pd
from typing import List, Tuple, Any
from data.extractors.helpers.csv_extractor import CsvExtractor
from data.extractors.interfaces.iextractor import IExtractor


class FeedbackCsvExtractor(IExtractor):
    """
    Extractor CSV de los feedbacks. Implementa la interfaz IExtractor.
    """

    def __init__(self, helper: CsvExtractor):
        self._helper = helper

    def extract(self, filepath: str) -> List[Tuple[Any, ...]]:
        print(
            f"Extrayendo datos de feedbacks desde el archivo CSV: {filepath}")
        
        # Leemos el CSV
        df = pd.read_csv(filepath)
        
        # Devolvemos una lista de tuplas con los datos del CSV, sin el índice y sin nombre para las tuplas
        return list(df.itertuples(index=False, name=None))

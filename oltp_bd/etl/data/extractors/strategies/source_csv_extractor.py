from typing import List, Tuple, Any
from data.extractors.helpers.csv_extractor import CsvExtractor
from data.extractors.interfaces.iextractor import IExtractor


class SourceCsvExtractor(IExtractor):
    """
    Extractor CSV de las fuentes. Implementa la interfaz IExtractor.
    """

    def __init__(self, helper: CsvExtractor):
        self._helper = helper

    def extract(self, filepath: str) -> List[Tuple[Any, ...]]:
        print(f"Extrayendo datos de fuentes desde el archivo CSV: {filepath}")

        # Las columnas que necesitamos extraer del CSV
        required_columns = ['IdFuente', 'TipoFuente', 'FechaCarga']

        # Usamos el helper para extraer las columnas requeridas
        return self._helper.extract_columns(filepath, required_columns)

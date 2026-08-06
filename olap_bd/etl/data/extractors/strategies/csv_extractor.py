import os
import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from data.extractors.interfaces.i_extractor import IExtractor
from data.extractors.helpers.extractor_helpers import auto_clean_value

logger = logging.getLogger(__name__)


class CsvExtractor(IExtractor):
    """
    Strategy de Extraccion para archivos CSV.
    Lee cualquier archivo CSV, auto-limpia valores y aplica el mapa de columnas y valores predeterminados que le especifiquemos.
    """

    def __init__(
        self,
        filepath: str,
        column_mapping: Dict[str, str],
        default_values: Optional[Dict[str, Any]] = None
    ):
        self._filepath = filepath
        self._column_mapping = column_mapping
        self._default_values = default_values or {}

    def extract(self) -> List[Dict[str, Any]]:
        """Lee el archivo CSV, auto-limpia valores y aplica el mapa de columnas dinamicamente."""
        if not os.path.exists(self._filepath):
            logger.warning(
                "El archivo CSV '%s' no fue encontrado.", self._filepath)
            return []

        try:
            logger.info(
                "Iniciando extraccion generica desde CSV: %s", self._filepath)

            # Leemos el CSV usando pandas
            df = pd.read_csv(self._filepath)
            results: List[Dict[str, Any]] = []

            # Iteramos sobre cada fila del DataFrame y aplicamos el mapeo de columnas y limpieza de valores
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                # Creamos un dict con los valores predeterminados
                record: Dict[str, Any] = dict(self._default_values)

                # Mapeamos segun el column_mapping y limpiamos los valores
                for csv_col, target_key in self._column_mapping.items():
                    if csv_col in row_dict:
                        record[target_key] = auto_clean_value(
                            row_dict[csv_col])

                results.append(record)

            logger.info("Extracción completada de '%s'. Registros obtenidos: %d",
                        self._filepath, len(results))
            return results

        except Exception as e:
            logger.error("Error al extraer CSV '%s': %s",
                         self._filepath, str(e))
            return []

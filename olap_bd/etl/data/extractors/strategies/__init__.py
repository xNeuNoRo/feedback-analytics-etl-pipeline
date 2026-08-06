from .api_extractor import ApiExtractor
from .database_extractor import DatabaseExtractor
from .csv_extractor import CsvExtractor

# Convertimos esta carpeta strategies en un paquete de PY para importacion mas sencilla
__all__ = ["ApiExtractor", "DatabaseExtractor", "CsvExtractor"]

from .interfaces import IExtractor
from .strategies import ApiExtractor, DatabaseExtractor, CsvExtractor

# Convertimos esta carpeta strategies en un paquete de PY para importacion mas sencilla
__all__ = ["IExtractor", "ApiExtractor", "DatabaseExtractor", "CsvExtractor"]

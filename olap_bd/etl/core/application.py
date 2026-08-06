import time
import logging
from typing import List, Dict, Any
from data.extractors.interfaces.i_extractor import IExtractor
from data.transformers.interfaces.i_transformer import ITransformer
from load.loader_service import LoaderService

logger = logging.getLogger(__name__)


class OlapEtlApplication:
    """
    Servicio Orquestador de todo el Pipeline ETL.
    Combina la extracción de fuentes, la transformación por dimensiones/NLP y la carga en DAOs.
    """

    def __init__(
        self,
        extractors: List[IExtractor],
        transformer: ITransformer,
        loader: LoaderService
    ):
        self._extractors = extractors
        self._transformer = transformer
        self._loader = loader

    def run_pipeline(self) -> Dict[str, Any]:
        """Ejecuta el ciclo completo ETL y mide los tiempos de procesamiento para tener un seguimiento del rendimiento del pipeline."""

        start_time = time.time()
        logger.info("=========================================================")
        logger.info("   INICIANDO PIPELINE ETL ANALITICO (BIG DATA 2026-C2)   ")
        logger.info("=========================================================")

        # Ejecutamos la fase 1, la extracción de datos desde las fuentes que alimentan el Data Warehouse OLAP
        all_raw_records: List[Dict[str, Any]] = []
        for index, extractor in enumerate(self._extractors, 1):
            extractor_name = extractor.__class__.__name__
            logger.info(
                "Ejecutando Extractor [%d/%d]: %s", index, len(self._extractors), extractor_name)
            extracted = extractor.extract()
            logger.info("Extractor '%s' extrajo %d registros.",
                        extractor_name, len(extracted))
            all_raw_records.extend(extracted)

        total_extracted = len(all_raw_records)
        logger.info(
            "FASE 1 EXTRACCION COMPLETADA. Total registros crudos: %d", total_extracted)

        # Ejecutamos la fase 2, la transformación de los datos crudos a un formato analítico, incluyendo análisis de sentimientos y normalización y todo eso.
        logger.info(
            "Iniciando Transformación y Análisis NLP de Sentimientos...")
        transformed_payload = self._transformer.transform(all_raw_records)
        facts_count = len(transformed_payload.get("fact_feedbacks", []))
        logger.info(
            "FASE 2 TRANSFORMACION COMPLETADA. Total registros procesados: %d", facts_count)

        # Ejecutamos la fase 3, la carga de los datos transformados en el Data Warehouse OLAP
        logger.info("Iniciando Carga de datos en el Data Warehouse OLAP...")
        total_loaded = self._loader.load(transformed_payload)
        logger.info(
            "FASE 3 CARGA COMPLETADA. Total registros insertados en fact_feedbacks: %d", total_loaded)

        elapsed_time = round(time.time() - start_time, 2)
        logger.info("=========================================================")
        logger.info("   PIPELINE ETL ANALÍTICO EJECUTADO CON ÉXITO")
        logger.info("   Tiempo Total de Ejecución: %s segundos", elapsed_time)
        logger.info("=========================================================")

        return {
            "status": "success",
            "extracted_count": total_extracted,
            "transformed_count": facts_count,
            "loaded_count": total_loaded,
            "elapsed_seconds": elapsed_time
        }

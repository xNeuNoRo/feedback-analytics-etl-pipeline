import logging
from typing import Dict, List, Any
from core.database import OlapDatabaseManager
from load.daos.dim_time_dao import DimTimeDao
from load.daos.dim_client_dao import DimClientDao
from load.daos.dim_product_dao import DimProductDao
from load.daos.dim_source_dao import DimSourceDao
from load.daos.dim_sentiment_dao import DimSentimentDao
from load.daos.fact_feedbacks_dao import FactFeedbacksDao

logger = logging.getLogger(__name__)


class LoaderService:
    """
    Servicio de Carga para la base de datos analítica OLAP.
    Basicamente orquesta la resolución de dimensiones con los DAOs e inserta los hechos en fact_feedbacks.
    """

    def __init__(
        self,
        olap_db_manager: OlapDatabaseManager,
        time_dao: DimTimeDao,
        client_dao: DimClientDao,
        product_dao: DimProductDao,
        source_dao: DimSourceDao,
        sentiment_dao: DimSentimentDao,
        fact_dao: FactFeedbacksDao
    ):
        self._db_manager = olap_db_manager
        self._time_dao = time_dao
        self._client_dao = client_dao
        self._product_dao = product_dao
        self._source_dao = source_dao
        self._sentiment_dao = sentiment_dao
        self._fact_dao = fact_dao

    def load(self, transformed_data: Dict[str, List[Dict[str, Any]]]) -> int:
        """Carga las dimensiones y hechos en el Modelo en Estrella."""
        facts_list = transformed_data.get("fact_feedbacks", [])
        logger.info(
            "Iniciando carga de %d hechos en la BD OLAP...", len(facts_list))

        if not facts_list:
            return 0
        
        inserted_count = 0
        try:
            with self._db_manager.get_session() as session:
                for item in facts_list:
                    time_key = self._time_dao.get_or_create(
                        session, item["time"])
                    client_key = self._client_dao.get_or_create(
                        session, item["client"])
                    product_key = self._product_dao.get_or_create(
                        session, item["product"])
                    source_key = self._source_dao.get_or_create(
                        session, item["source"])
                    sentiment_key = self._sentiment_dao.get_or_create(
                        session, item["sentiment"])

                    self._fact_dao.insert_fact(
                        session=session,
                        time_key=time_key,
                        client_key=client_key,
                        product_key=product_key,
                        source_key=source_key,
                        sentiment_key=sentiment_key,
                        fact_item=item
                    )
                    inserted_count += 1

                session.commit()

            logger.info(
                "Carga completada con éxito en la BD OLAP. Registros insertados: %d", inserted_count)
            return inserted_count

        except Exception as e:
            logger.error("Error durante la carga en la BD OLAP: %s", str(e))
            raise

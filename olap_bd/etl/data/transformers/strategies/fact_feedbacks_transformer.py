import logging
from typing import List, Dict, Any
from data.transformers.interfaces.i_transformer import ITransformer
from data.transformers.strategies.dim_time_transformer import DimTimeTransformer
from data.transformers.strategies.dim_client_transformer import DimClientTransformer
from data.transformers.strategies.dim_product_transformer import DimProductTransformer
from data.transformers.strategies.dim_source_transformer import DimSourceTransformer
from data.transformers.strategies.dim_sentiment_transformer import DimSentimentTransformer

logger = logging.getLogger(__name__)


class FactFeedbacksTransformer(ITransformer):
    """
    Transformador orquestador de datos para el Data Warehouse OLAP.
    Combina los transformadores de las 5 dimensiones (Time, Client, Product, Source, Sentiment)
    y genera el payload estructurado para la fact table fact_feedbacks.
    """

    def __init__(
        self,
        time_tf: DimTimeTransformer,
        client_tf: DimClientTransformer,
        product_tf: DimProductTransformer,
        source_tf: DimSourceTransformer,
        sentiment_tf: DimSentimentTransformer
    ):
        self._time_tf = time_tf
        self._client_tf = client_tf
        self._product_tf = product_tf
        self._source_tf = source_tf
        self._sentiment_tf = sentiment_tf

    def transform(self, raw_records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Procesa la lista de diccionarios crudos y construye el diccionario agrupado de facts y dims."""
        logger.info(
            "Iniciando transformación y análisis NLP de %d registros crudos...", len(raw_records))

        facts_list: List[Dict[str, Any]] = []

        for record in raw_records:
            try:
                time_dim = self._time_tf.transform_date(
                    record.get("created_at"))
                client_dim = self._client_tf.transform_client(record)
                product_dim = self._product_tf.transform_product(record)
                source_dim = self._source_tf.transform_source(record)
                sentiment_dim = self._sentiment_tf.transform_sentiment(
                    comment=record.get("comment", ""),
                    rating=record.get("rating"),
                    raw_sentiment=record.get("raw_sentiment")
                )

                fact_item = {
                    "time": time_dim,
                    "client": client_dim,
                    "product": product_dim,
                    "source": source_dim,
                    "sentiment": sentiment_dim,
                    "rating": record.get("rating"),
                    "feedback_count": 1,
                    "comment_text": record.get("comment", ""),
                    "original_external_id": record.get("external_id")
                }
                facts_list.append(fact_item)

            except Exception as e:
                logger.error("Error al transformar registro: %s", str(e))

        logger.info(
            "Transformación completada con éxito. Payloads generados: %d", len(facts_list))
        return {
            "fact_feedbacks": facts_list
        }

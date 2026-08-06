from core.application import OlapEtlApplication
from load.loader_service import LoaderService
from data.transformers.strategies.fact_feedbacks_transformer import FactFeedbacksTransformer
from data.transformers.strategies.dim_sentiment_transformer import DimSentimentTransformer
from data.transformers.strategies.dim_source_transformer import DimSourceTransformer
from data.transformers.strategies.dim_product_transformer import DimProductTransformer
from data.transformers.strategies.dim_client_transformer import DimClientTransformer
from data.transformers.strategies.dim_time_transformer import DimTimeTransformer
from data.transformers.helpers.nlp_sentiment_analyzer import NlpSentimentAnalyzer
from data.extractors.interfaces.i_extractor import IExtractor
import sys
from datetime import datetime
from typing import List, Dict, Any

from pathlib import Path

etl_dir = str(Path(__file__).resolve().parents[1])
if etl_dir not in sys.path:
    sys.path.insert(0, etl_dir)

parent_root = str(Path(__file__).resolve().parents[4])
if parent_root not in sys.path:
    sys.path.insert(0, parent_root)


def test_nlp_sentiment_analyzer():
    """Prueba que el motor NLP clasifique correctamente los comentarios en español."""
    analyzer = NlpSentimentAnalyzer()

    # Positivo
    pos = analyzer.analyze_sentiment(
        "Excelente producto, súper rápido y buena atención", rating=5)
    assert pos == "Positivo", f"Esperado Positivo, obtenido {pos}"

    # Negativo
    neg = analyzer.analyze_sentiment(
        "Pésimo servicio, muy lento y llegó defectuoso", rating=1)
    assert neg == "Negativo", f"Esperado Negativo, obtenido {neg}"

    # Neutro
    neu = analyzer.analyze_sentiment("Todo normal sin novedad", rating=3)
    assert neu == "Neutro", f"Esperado Neutro, obtenido {neu}"

    print("Test NlpSentimentAnalyzer Passed!")


def test_fact_feedbacks_transformer():
    """Prueba que el transformador componga todas las dimensiones y el registro de hechos."""
    analyzer = NlpSentimentAnalyzer()
    time_tf = DimTimeTransformer()
    client_tf = DimClientTransformer()
    product_tf = DimProductTransformer()
    source_tf = DimSourceTransformer()
    sentiment_tf = DimSentimentTransformer(nlp_analyzer=analyzer)

    transformer = FactFeedbacksTransformer(
        time_tf=time_tf,
        client_tf=client_tf,
        product_tf=product_tf,
        source_tf=source_tf,
        sentiment_tf=sentiment_tf
    )

    raw_record = {
        "external_id": "EXT-999",
        "comment": "Gran servicio de entrega",
        "rating": 5,
        "created_at": datetime(2026, 8, 3, 15, 0, 0),
        "client_name": "María López",
        "client_country": "República Dominicana",
        "product_name": "Teclado Mapeado",
        "category_name": "Accesorios",
        "source_id": "SRC-WEB",
        "source_type_name": "Web",
        "platform": "Sitio Web"
    }

    result = transformer.transform([raw_record])
    facts = result.get("fact_feedbacks", [])
    assert len(facts) == 1

    fact = facts[0]
    assert fact["time"]["year"] == 2026
    assert fact["time"]["month"] == 8
    assert fact["time"]["quarter_name"] == "Q3"
    assert fact["time"]["day_of_week_name"] == "Lunes"
    assert fact["sentiment"]["sentiment_name"] == "Positivo"
    assert fact["client"]["country"] == "República Dominicana"
    print("Test FactFeedbacksTransformer Passed!")


class DummyExtractor(IExtractor):
    def extract(self) -> List[Dict[str, Any]]:
        return [
            {
                "external_id": "MOCK-1",
                "comment": "Comentario de prueba",
                "rating": 4,
                "created_at": datetime.utcnow().isoformat()
            }
        ]


class DummyLoaderService:
    def load(self, transformed_data: Dict[str, List[Dict[str, Any]]]) -> int:
        facts = transformed_data.get("fact_feedbacks", [])
        return len(facts)


def test_application_orchestrator():
    """Prueba la ejecución completa del orquestador OlapEtlApplication."""

    extractor = DummyExtractor()
    analyzer = NlpSentimentAnalyzer()
    transformer = FactFeedbacksTransformer(
        time_tf=DimTimeTransformer(),
        client_tf=DimClientTransformer(),
        product_tf=DimProductTransformer(),
        source_tf=DimSourceTransformer(),
        sentiment_tf=DimSentimentTransformer(nlp_analyzer=analyzer)
    )
    loader = DummyLoaderService()  # type: ignore

    app = OlapEtlApplication(
        extractors=[extractor],
        transformer=transformer,
        loader=loader  # type: ignore
    )

    results = app.run_pipeline()
    assert results["status"] == "success"
    assert results["extracted_count"] == 1
    assert results["transformed_count"] == 1
    assert results["loaded_count"] == 1
    print("Test OlapEtlApplication Orchestrator Passed!")


if __name__ == "__main__":
    test_nlp_sentiment_analyzer()
    test_fact_feedbacks_transformer()
    test_application_orchestrator()
    print("All OLAP ETL Integration Tests Passed Successfully!")

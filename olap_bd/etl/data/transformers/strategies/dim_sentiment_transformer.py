from typing import Dict, Any, Optional
from data.transformers.helpers.nlp_sentiment_analyzer import NlpSentimentAnalyzer


class DimSentimentTransformer:
    """Transformador para la dimensión dim_sentiment mediante el uso del NLP."""

    def __init__(self, nlp_analyzer: NlpSentimentAnalyzer):
        self._nlp_analyzer = nlp_analyzer

    def transform_sentiment(
        self,
        comment: str,
        rating: Optional[int] = None,
        raw_sentiment: Optional[str] = None
    ) -> Dict[str, Any]:
        """Aplica el NLP de sentimientos de comentarios y devuelve el diccionario para dim_sentiment."""
        sentiment_name = self._nlp_analyzer.analyze_sentiment(
            comment=comment,
            rating=rating,
            raw_sentiment=raw_sentiment
        )
        return {
            "sentiment_name": sentiment_name
        }

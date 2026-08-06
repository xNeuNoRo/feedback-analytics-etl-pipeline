import re
import logging
from typing import Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)


class NlpSentimentAnalyzer:
    """
    Motor de Análisis de Sentimientos mediante NLP (Natural Language Processing).
    Utiliza VADER (Valence Aware Dictionary and sEntiment Reasoner) con palabras clave tokenizadas
    en español para clasificar comentarios en 'Positivo', 'Negativo' o 'Neutro'.
    """

    # Palabras clave en español para analizar sentimientos positivos y negativos
    SPANISH_POSITIVE_KEYWORDS = {
        "excelente", "bueno", "buen", "gran", "fantastico", "maravilloso", "increible",
        "encanta", "perfecto", "rapido", "recomiendo", "satisfecho", "genial", "top",
        "eficiente", "amable", "calidad", "super"
    }

    # Palabras clave en español para analizar sentimientos negativos
    SPANISH_NEGATIVE_KEYWORDS = {
        "malo", "pesimo", "horrible", "terrible", "tardo", "lento", "roto", "defectuoso",
        "estafa", "caro", "incompetente", "error", "basura", "desastre", "decepcion",
        "problema", "mal"
    }

    # Inicializamos el analizador de sentimientos VADER
    def __init__(self):
        self._vader = SentimentIntensityAnalyzer()

    def analyze_sentiment(
        self,
        comment: str,
        rating: Optional[int] = None,
        raw_sentiment: Optional[str] = None
    ) -> str:
        """
        Analiza el texto del comentario y determina el sentimiento categórico.
        Aplica tokenización por palabras completas y fallback por calificación si el texto es ambiguo.
        """
        # Si ya viene un sentimiento directo desde la fuente, lo mapeamos
        if raw_sentiment and isinstance(raw_sentiment, str):
            clean_raw = raw_sentiment.strip().capitalize()
            if clean_raw in ("Positivo", "Negativo", "Neutro"):
                return clean_raw
            if "pos" in clean_raw.lower() or "good" in clean_raw.lower():
                return "Positivo"
            if "neg" in clean_raw.lower() or "bad" in clean_raw.lower():
                return "Negativo"

        # Tokenización y análisis de palabras clave en español
        comment_lower = comment.lower().strip()
        # Tokenizamos el comentario en palabras completas usando regex para evitar coincidencias parciales
        words = set(re.findall(r'\b\w+\b', comment_lower))

        # Contamos las coincidencias con las palabras clave positivas y negativas
        pos_hits = len(words.intersection(self.SPANISH_POSITIVE_KEYWORDS))
        neg_hits = len(words.intersection(self.SPANISH_NEGATIVE_KEYWORDS))

        # Si hay más palabras positivas que negativas, clasificamos como Positivo
        if pos_hits > neg_hits and pos_hits > 0:
            return "Positivo"

        # Si hay más palabras negativas que positivas, clasificamos como Negativo
        if neg_hits > pos_hits and neg_hits > 0:
            return "Negativo"

        # Si no hay palabras clave claras, usamos la calificación como fallback
        if rating is not None:
            if rating >= 4:
                return "Positivo"
            if rating <= 2:
                return "Negativo"
            if rating == 3:
                return "Neutro"

        # Analizamos el sentimiento usando VADER como último recurso
        scores = self._vader.polarity_scores(comment)

        # Compound score lo que hace es dar un valor entre -1 y 1 que indica la polaridad general del texto
        # Si es positivo seria > 0.05, negativo < -0.05 y neutro entre esos valores
        # 0.0 que le especificamos es un valor neutro por defecto en caso de que no se encuentre la clave
        compound = scores.get("compound", 0.0)

        # Clasificamos según el compound score de VADER
        if compound >= 0.05:
            return "Positivo"
        elif compound <= -0.05:
            return "Negativo"

        # Si no se puede determinar un sentimiento claro, devolvemos Neutro
        return "Neutro"

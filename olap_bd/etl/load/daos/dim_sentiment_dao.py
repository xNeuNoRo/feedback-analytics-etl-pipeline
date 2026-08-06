from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session


class DimSentimentDao:
    """DAO de dim_sentiment llamando a fn_upsert_dim_sentiment de la BD OLAP."""

    # Cache para evitar múltiples inserciones de sentimientos idénticos en la misma ejecución
    def __init__(self):
        self._cache: Dict[str, int] = {}

    def get_or_create(self, session: Session, st: Dict[str, Any]) -> int:
        # Obtenemos el nombre del sentimiento para usarlo como clave de cache
        name_val = st.get("sentiment_name", "Neutro")

        # Si ya tenemos el sentimiento en cache, devolvemos el ID almacenado
        if name_val in self._cache:
            return self._cache[name_val]

        # Si no está en cache, llamamos a la función de upsert en la BD OLAP

        # Armamos la query para llamar a la función fn_upsert_dim_sentiment
        stmt = text("""
            SELECT fn_upsert_dim_sentiment(CAST(:sentiment_name AS varchar));
        """)

        # Ejecutamos la query y obtenemos el ID del sentimiento insertado o actualizado
        res = session.execute(stmt, {"sentiment_name": name_val}).scalar()

        # Si la función devuelve None, asignamos un ID por defecto (1) para evitar errores
        key = int(res) if res is not None else 1

        # Guardamos el ID en cache para futuras referencias
        self._cache[name_val] = key
        return key

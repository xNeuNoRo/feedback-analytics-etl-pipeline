import json
import logging
from typing import List, Dict, Any
from sqlalchemy import text
from data.extractors.interfaces.i_extractor import IExtractor
from core.database import OltpDatabaseManager

logger = logging.getLogger(__name__)


class DatabaseExtractor(IExtractor):
    """
    Stratregy de Extracción desde la BD Relacional OLTP.
    Consulta reseñas directamente usando modelos SQLAlchemy ya que son simples SELECTs y JOINs, sin necesidad de usar procedimientos almacenados.
    """

    def __init__(self, oltp_db_manager: OltpDatabaseManager):
        self._db_manager = oltp_db_manager

    def extract(self) -> List[Dict[str, Any]]:
        """Consulta reseñas desde la BD OLTP y las convierte a diccionarios."""
        logger.info("Iniciando extracción desde la BD Relacional OLTP...")
        results: List[Dict[str, Any]] = []

        try:
            stmt = text("""
                SELECT 
                    f.external_id,
                    f.comment,
                    f.rating,
                    f.created_at,
                    f.sentiment AS raw_sentiment,
                    f.platform,
                    f.metadata AS metadata_json,
                    c.id AS client_id,
                    c.name AS client_name,
                    c.email AS client_email,
                    p.id AS product_id,
                    p.name AS product_name,
                    cat.name AS category_name,
                    s.id AS source_id,
                    st.name AS source_type_name
                FROM feedbacks f
                LEFT JOIN clients c ON f.client_id = c.id
                LEFT JOIN products p ON f.product_id = p.id
                LEFT JOIN categories cat ON p.category_id = cat.id
                LEFT JOIN sources s ON f.source_id = s.id
                LEFT JOIN source_types st ON s.source_type_id = st.id
                ORDER BY f.created_at DESC
            """)

            with self._db_manager.get_session() as session:
                rows = session.execute(stmt).mappings().all()
                for row in rows:
                    metadata: Dict[str, Any] = {}
                    raw_meta = row.get("metadata_json")
                    if isinstance(raw_meta, dict):
                        metadata = raw_meta
                    elif isinstance(raw_meta, str) and raw_meta.strip():
                        try:
                            metadata = json.loads(raw_meta)
                        except json.JSONDecodeError:
                            metadata = {}

                    country = metadata.get(
                        "country", metadata.get("pais", "Desconocido"))
                    age_group = metadata.get(
                        "age_group", metadata.get("edad", "Desconocido"))
                    client_type = metadata.get(
                        "client_type", metadata.get("tipo", "Regular"))

                    created_at_val = row.get("created_at")
                    created_at_str = created_at_val.isoformat() if (created_at_val is not None and hasattr(
                        created_at_val, "isoformat")) else str(created_at_val) if created_at_val is not None else None

                    record = {
                        "external_id": row.get("external_id"),
                        "comment": row.get("comment"),
                        "rating": row.get("rating"),
                        "created_at": created_at_str,
                        "raw_sentiment": row.get("raw_sentiment"),

                        "client_id": row.get("client_id"),
                        "client_name": row.get("client_name") or "Cliente Anónimo",
                        "client_email": row.get("client_email"),
                        "client_country": str(country),
                        "client_age_group": str(age_group),
                        "client_type": str(client_type),

                        "product_id": row.get("product_id"),
                        "product_name": row.get("product_name") or "Producto General",
                        "category_name": row.get("category_name") or "General",

                        "source_id": row.get("source_id") or "SRC-DB",
                        "source_type_name": row.get("source_type_name") or "Web",
                        "platform": row.get("platform") or "Web"
                    }
                    results.append(record)

            logger.info(
                "Extracción desde la BD OLTP completada. Registros obtenidos: %d", len(results))
            return results

        except Exception as e:
            logger.error(
                "Error durante la extracción desde la BD OLTP: %s", str(e))
            return []

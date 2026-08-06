from typing import Dict, Any, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session


class DimSourceDao:
    """DAO de dim_source invocando fn_upsert_dim_source de la BD OLAP."""

    # Cache para evitar múltiples inserciones de fuentes idénticas en la misma ejecución
    def __init__(self):
        self._cache: Dict[Tuple[str, str], int] = {}

    def get_or_create(self, session: Session, s: Dict[str, Any]) -> int:
        # Obtenemos el original_source_id y la plataforma para usarlo como clave de cache
        orig_id = str(s.get("original_source_id") or "SRC-UNKNOWN")
        platform = str(s.get("platform") or "General")
        cache_key = (orig_id, platform)

        # Si ya tenemos la fuente en cache, devolvemos el ID almacenado
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Si no está en cache, llamamos a la función de upsert en la BD OLAP

        # Armamos la query para llamar a la función fn_upsert_dim_source
        stmt = text("""
            SELECT fn_upsert_dim_source(
                CAST(:original_source_id AS varchar),
                CAST(:source_type_name AS varchar),
                CAST(:platform AS varchar)
            );
        """)

        # Ejecutamos la query y obtenemos el ID de la fuente insertada o actualizada
        res = session.execute(stmt, {
            "original_source_id": orig_id,
            "source_type_name": str(s.get("source_type_name") or "General"),
            "platform": platform
        }).scalar()

        # Si la función devuelve None, asignamos un ID por defecto (1) para evitar errores
        key = int(res) if res is not None else 1

        # Guardamos el ID en cache para futuras referencias
        self._cache[cache_key] = key
        return key

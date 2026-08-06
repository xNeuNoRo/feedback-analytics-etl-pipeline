import re
from typing import Dict, Any, Tuple, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session


class DimClientDao:
    """DAO de dim_client llamando a fn_upsert_dim_client de la BD OLAP."""

    # Cache para evitar múltiples inserciones de clientes idénticos en la misma ejecución
    def __init__(self):
        self._cache: Dict[Tuple[Optional[int], str], int] = {}

    def get_or_create(self, session: Session, c: Dict[str, Any]) -> int:
        # Obtenemos el original_client_id y el nombre del cliente para usarlo como clave de cache
        raw_orig_id = c.get("original_client_id")
        orig_id: Optional[int] = None
        if raw_orig_id is not None:
            nums = re.sub(r'\D', '', str(raw_orig_id))
            orig_id = int(nums) if nums else None

        name_val = c.get("name", "Cliente Anónimo")
        cache_key = (raw_orig_id, name_val)

        # Si ya tenemos el cliente en cache, devolvemos el ID almacenado
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Si no está en cache, llamamos a la función de upsert en la BD OLAP

        # Armamos la query para llamar a la función fn_upsert_dim_client
        stmt = text("""
            SELECT fn_upsert_dim_client(
                CAST(:original_client_id AS int),
                CAST(:name AS varchar),
                CAST(:email AS varchar),
                CAST(:country AS varchar),
                CAST(:age_group AS varchar),
                CAST(:client_type AS varchar)
            );
        """)

        # Ejecutamos la query y obtenemos el ID del cliente insertado o actualizado
        res = session.execute(stmt, {
            "original_client_id": orig_id,
            "name": name_val,
            "email": c.get("email"),
            "country": c.get("country", "Desconocido"),
            "age_group": c.get("age_group", "Desconocido"),
            "client_type": c.get("client_type", "Regular")
        }).scalar()

        # Si la función devuelve None, asignamos un ID por defecto (1) para evitar errores
        key = int(res) if res is not None else 1

        # Guardamos el ID en cache para futuras referencias
        self._cache[cache_key] = key
        return key

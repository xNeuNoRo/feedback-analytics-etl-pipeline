from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session


class DimTimeDao:
    """DAO de dim_time invocando fn_upsert_dim_time de la BD OLAP."""

    # Cache para evitar múltiples inserciones de fechas idénticas en la misma ejecución
    def __init__(self):
        self._cache: Dict[str, int] = {}

    def get_or_create(self, session: Session, t: Dict[str, Any]) -> int:
        # Obtenemos la fecha completa para usarla como clave de cache
        full_date_val = t["full_date"]
        cache_key = str(full_date_val)

        # Si ya tenemos la fecha en cache, devolvemos el ID almacenado
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Si no está en cache, llamamos a la función de upsert en la BD OLAP

        # Armamos la query para llamar a la función fn_upsert_dim_time
        stmt = text("""
            SELECT fn_upsert_dim_time(
                CAST(:full_date AS date),
                CAST(:year AS int),
                CAST(:month AS int),
                CAST(:quarter_num AS int),
                CAST(:quarter_name AS varchar),
                CAST(:day_of_week_num AS int),
                CAST(:day_of_week_name AS varchar)
            );
        """)

        # Ejecutamos la query y obtenemos el ID de la fecha insertada o actualizada
        res = session.execute(stmt, {
            "full_date": t["full_date"],
            "year": t["year"],
            "month": t["month"],
            "quarter_num": t["quarter_num"],
            "quarter_name": t["quarter_name"],
            "day_of_week_num": t["day_of_week_num"],
            "day_of_week_name": t["day_of_week_name"]
        }).scalar()

        # Si la función devuelve None, asignamos un ID por defecto (1) para evitar errores
        key = int(res) if res is not None else 1

        # Guardamos el ID en cache para futuras referencias
        self._cache[cache_key] = key
        return key

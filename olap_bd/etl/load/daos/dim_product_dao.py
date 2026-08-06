import re
from typing import Dict, Any, Tuple, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session


class DimProductDao:
    """DAO de dim_product llamando a fn_upsert_dim_product de la BD OLAP."""

    # Cache para evitar múltiples inserciones de productos idénticos en la misma ejecución
    def __init__(self):
        self._cache: Dict[Tuple[Any, str], int] = {}

    def get_or_create(self, session: Session, p: Dict[str, Any]) -> int:
        # Obtenemos el original_product_id y el nombre del producto para usarlo como clave de cache
        raw_orig_id = p.get("original_product_id")
        orig_id: Optional[int] = None
        if raw_orig_id is not None:
            nums = re.sub(r'\D', '', str(raw_orig_id))
            orig_id = int(nums) if nums else None

        pname = p.get("product_name", "Producto General")
        cache_key = (raw_orig_id, pname)

        # Si ya tenemos el producto en cache, devolvemos el ID almacenado
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Si no está en cache, llamamos a la función de upsert en la BD OLAP

        # Armamos la query para llamar a la función fn_upsert_dim_product
        stmt = text("""
            SELECT fn_upsert_dim_product(
                CAST(:original_product_id AS int),
                CAST(:product_name AS varchar),
                CAST(:category_name AS varchar)
            );
        """)

        # Ejecutamos la query y obtenemos el ID del producto insertado o actualizado
        res = session.execute(stmt, {
            "original_product_id": orig_id,
            "product_name": pname,
            "category_name": p.get("category_name", "General")
        }).scalar()

        # Si la función devuelve None, asignamos un ID por defecto (1) para evitar errores
        key = int(res) if res is not None else 1

        # Guardamos el ID en cache para futuras referencias
        self._cache[cache_key] = key
        return key

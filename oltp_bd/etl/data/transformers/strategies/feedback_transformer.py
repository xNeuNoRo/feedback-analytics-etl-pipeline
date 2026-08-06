from typing import List, Tuple, Any, Dict
import pandas as pd
from data.transformers.interfaces.itransformer import ITransformer
from data.transformers.helpers.string_helper import StringHelper


class FeedbackTransformer(ITransformer):
    """Estrategia de transformación para las opiniones (Feedbacks)."""

    def __init__(
        self,
        helper: StringHelper,
        csv_headers: List[str],
        column_mapping: Dict[str, str],
        source_id: str,
        platform: str
    ):
        self._helper = helper
        self._headers = csv_headers
        self._mapping = column_mapping
        self._source_id = source_id
        self._platform = platform

    def transform(self, raw_data: List[Tuple[Any, ...]]) -> List[Tuple[Any, ...]]:
        # Inicializamos el listado de tuplas que contendrá los datos limpios y transformados
        cleaned_list: List[Tuple[Any, ...]] = []
        for row in raw_data:
            # Creamos un diccionario a partir del row y los headers
            row_dict = dict(zip(self._headers, row))

            # Extraemos y transformamos los datos según el mapeo definido
            ext_col: str = self._mapping['external_id']
            raw_ext = row_dict.get(ext_col)
            ext_id = str(raw_ext).strip() if pd.notna(raw_ext) else ""

            # Extraemos el ID del producto segun el mapeo definido y usamos el helper para obtener un ID limpio
            prod_col: str = self._mapping['product_id']
            prod_id = self._helper.extract_id(row_dict.get(prod_col))

            # Extraemos el ID del cliente segun el mapeo definido y usamos el helper para obtener un ID limpio
            client_col = self._mapping.get('client_id')
            client_id = self._helper.extract_id(
                row_dict.get(client_col)) if client_col else None

            # Extraemos la fecha de creación según el mapeo definido
            created_at_col: str = self._mapping['created_at']
            raw_created_at = row_dict.get(created_at_col)
            created_at = raw_created_at if pd.notna(raw_created_at) else None

            # Extraemos el comentario según el mapeo definido
            comment_col: str = self._mapping['comment']
            raw_comment = row_dict.get(comment_col)
            comment = str(raw_comment).strip() if pd.notna(raw_comment) else ""

            # Extraemos el rating según el mapeo definido y lo convertimos a entero si es posible
            rating_col = self._mapping.get('rating')
            raw_rating = row_dict.get(rating_col) if rating_col else None
            rating = int(raw_rating) if pd.notna(raw_rating) else None

            # Extraemos el sentimiento según el mapeo definido
            sentiment = None

            # Extraemos el platform (Si viene en el CSV lo usamos, si no, usamos el inyectado)
            platform_col = self._mapping.get('platform')
            row_platform = row_dict.get(platform_col) if platform_col else None
            final_platform = str(row_platform).strip() if pd.notna(row_platform) else self._platform

            # Creamos la tupla final con todos los datos transformados y la agregamos a la lista de resultados
            final_tuple = (ext_id, prod_id, client_id, self._source_id,
                           final_platform, comment, created_at, rating, sentiment)

            # Agregamos la tupla final a la lista de resultados
            cleaned_list.append(final_tuple)

        return cleaned_list

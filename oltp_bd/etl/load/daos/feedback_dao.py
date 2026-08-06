from psycopg import Cursor
from typing import List, Tuple, Any
from core.database import with_db_connection


class FeedbackDAO:
    """
    DAO encargado de insertar las transacciones de feedback usando el procedure de postgres
    """

    @with_db_connection
    def insert_batch(self, cursor: Cursor, data_list: List[Tuple[Any, ...]]) -> None:
        """
        Inserta una lista masiva de feedbacks (opiniones)

        Args:
            cursor (Cursor): Cursor de la base de datos. (Se inyecta automaticamente con el decorador @with_db_connection)
            data_list (List[Tuple[Any, ...]]): Lista de tuplas con los datos a insertar. El orden debe ser: 
            (external_id, product_id, client_id, source_id, platform, comment, created_at, rating, sentiment)
        """

        # Llamamos al procedure de postgres
        query = "CALL sp_insert_feedback(%s, %s, %s, %s, %s, %s, %s, %s, %s);"

        # executemany envia todos los datos al procedure de postgres
        cursor.executemany(query, data_list)

        # Calculamos cuantos registros se mandaron solo para loguear
        total_records = len(data_list)
        print(f"Se han procesado {total_records} registros de feedback.")

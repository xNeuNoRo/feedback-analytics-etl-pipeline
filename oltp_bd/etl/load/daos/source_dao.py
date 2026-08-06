from psycopg import Cursor
from typing import List, Tuple, Any
from core.database import with_db_connection


class SourceDAO:
    """
    DAO encargado de insertar o actualizar fuentes de datos y sus tipos (ej: Web, Redes, etc) usando la funcion de postgres
    """

    @with_db_connection
    def upsert_batch(self, cursor: Cursor, data_list: List[Tuple[str, str, Any]]) -> None:
        """
        Inserta una lista masiva de fuentes de datos y sus tipos.

        Args:
            cursor (Cursor): Cursor de la base de datos. (Se inyecta automaticamente con el decorador @with_db_connection)
            data_list (List[Tuple[str, str, Any]]): Lista de tuplas con los datos a insertar. Ej: [(IdDeLaFuente1, Tipo1, Fecha), (IdDeLaFuente2, Tipo2, Fecha)]
        """

        # Llamamos a la funcion de postgres
        query = "SELECT fn_upsert_source(%s, %s, %s);"

        # executemany envia todos los datos a la funcion de postgres
        cursor.executemany(query, data_list)

        # Calculamos cuantos registros se mandaron solo para loguear
        total_records = len(data_list)
        print(
            f"Se han procesado {total_records} registros de fuentes de datos y sus tipos.")

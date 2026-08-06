from psycopg import Cursor
from typing import List, Tuple
from core.database import with_db_connection


class ClientDAO:
    """
    DAO encargado de insertar o actualizar clientes
    usando la funcion de postgres
    """

    @with_db_connection
    def upsert_batch(self, cursor: Cursor, data_list: List[Tuple[str, str]]) -> None:
        """
        Inserta una lista masiva de clientes.

        Args:
            cursor (Cursor): Cursor de la base de datos. (Se inyecta automaticamente con el decorador @with_db_connection)
            data_list (List[Tuple[str, str]]): Lista de tuplas con los datos a insertar. Ej: [("Nombre1", "correo@ejemplo.com"), ("Nombre2", "correo@ejemplo.com")]
        """

        # Llamamos a la funcion de postgres
        query = "SELECT fn_upsert_client(%s, %s);"

        # executemany envia todos los datos a la funcion de postgres
        cursor.executemany(query, data_list)

        # Calculamos cuantos registros se mandaron solo para loguear
        total_records = len(data_list)
        print(f"Se han procesado {total_records} registros de clientes.")

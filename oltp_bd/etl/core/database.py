import psycopg
from functools import wraps
from typing import Callable, Any, TypeVar, cast
from core.config import Config

# R es el tipo de retorno de la funcion decorada
R = TypeVar('R')

# func es la funcion en si misma, es decir, la funcion que estamos decorando


def with_db_connection(func: Callable[..., R]) -> Callable[..., R]:
    """
    Decorador para abrir una conexion a PostgreSQL,
    maneja la transaccion automaticamente e inyecta el
    'cursor' en la funcion decorada.
    """
    # el decorador nativo wraps de python, sirve para que la funcion decorada conserve el nombre y docstring de la funcion original
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> R:
        # Obtenemos el connection string de la bd
        connection_string: str = Config.get_db_connection_string()

        # Abrimos la conexion a la bd
        # el with es un manejador de contexto, que se encarga de cerrar la conexion automaticamente al salir del bloque
        # y ademas maneja la transaccion automaticamente, es decir, si no hay errores hace commit y si hay errores hace rollback
        with psycopg.connect(connection_string) as conn:
            # Abrimos un cursor para ejecutar las sentencias SQL
            with conn.cursor() as cursor:

                # Inyectamos el cursor de la funcion decorada
                return func(self, cursor, *args, **kwargs)

    # Devolvemos la funcion decorada, casteada al tipo de retorno de la funcion original
    return cast(Callable[..., R], wrapper)

import os
from dotenv import load_dotenv

# Cargamos todas las variables de entorno desde el archivo .env
load_dotenv()


class Config:
    """
    Clase de config centralizada para el proyecto
    """

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5433")
    DB_NAME: str = os.getenv("DB_NAME", "oltp_dev")
    DB_USER: str = os.getenv("DB_USER", "AngelGM")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "angelgonzalez")

    @classmethod
    # cls es como el this de java, es la clase en si misma
    def get_db_connection_string(cls) -> str:
        """
        Metodo para devolver el connection string de la bd
        """

        return f"host={cls.DB_HOST} port={cls.DB_PORT} dbname={cls.DB_NAME} user={cls.DB_USER} password={cls.DB_PASSWORD}"

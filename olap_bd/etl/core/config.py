from pydantic_settings import BaseSettings, SettingsConfigDict


class EtlSettings(BaseSettings):
    """Configuración centralizada para el Pipeline ETL de la Base de Datos Analítica OLAP."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Configuración de conexión a PostgreSQL OLTP
    OLTP_DB_HOST: str = "localhost"
    OLTP_DB_PORT: int = 5433
    OLTP_DB_NAME: str = "oltp_dev"
    OLTP_DB_USER: str = "postgres"
    OLTP_DB_PASSWORD: str = "postgres"

    # Configuración de conexión a PostgreSQL OLAP Data Warehouse
    OLAP_DB_HOST: str = "localhost"
    OLAP_DB_PORT: int = 5434
    OLAP_DB_NAME: str = "olap_dev"
    OLAP_DB_USER: str = "postgres"
    OLAP_DB_PASSWORD: str = "postgres"

    # Configuración de la API REST de Redes Sociales
    API_BASE_URL: str = "http://localhost:8000"
    API_KEY: str = "oltp-secret-api-key-bigdata-project-2026"

    # Ruta de los Archivos CSV de Entrada de la BD OLAP
    CSV_FOLDER_PATH: str = "./data/input"

    # Nivel de Log para el Pipeline ETL
    LOG_LEVEL: str = "INFO"

    @property
    def oltp_database_url(self) -> str:
        """URL de conexión SQLAlchemy para la base de datos OLTP."""
        return f"postgresql+psycopg://{self.OLTP_DB_USER}:{self.OLTP_DB_PASSWORD}@{self.OLTP_DB_HOST}:{self.OLTP_DB_PORT}/{self.OLTP_DB_NAME}"

    @property
    def olap_database_url(self) -> str:
        """URL de conexión SQLAlchemy para el Data Warehouse OLAP."""
        return f"postgresql+psycopg://{self.OLAP_DB_USER}:{self.OLAP_DB_PASSWORD}@{self.OLAP_DB_HOST}:{self.OLAP_DB_PORT}/{self.OLAP_DB_NAME}"


etl_settings = EtlSettings()

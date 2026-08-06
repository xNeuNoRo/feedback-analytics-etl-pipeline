from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde las variables de entorno o archivo .env."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Configuración de conexión a la base de datos OLTP (PostgreSQL)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_NAME: str = "oltp_dev"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_MIN_POOL_SIZE: int = 2
    DB_MAX_POOL_SIZE: int = 10

    # Configuración del servidor de la API
    API_ENV: str = "development"
    API_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # Clave de autenticación para el header X-API-Key
    API_KEY: str = "oltp-secret-api-key-bigdata-project-2026"

    @property
    def database_url(self) -> str:
        """Construye la URL de conexión SQLAlchemy"""
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

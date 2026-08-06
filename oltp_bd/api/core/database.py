import logging
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import Settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Administrador de motor e inicio de sesiones usando SQLAlchemy.
    Basicamente maneja el pool de conexiones de SQLAlchemy.
    """

    def __init__(self, config: Settings):
        self._config = config
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    def initialize_pool(self) -> None:
        """Inicializa el Engine y el sessionmaker de SQLAlchemy."""
        if not self._engine:
            logger.info(
                "Inicializando Motor SQLAlchemy en el puerto %s...", self._config.DB_PORT)
            self._engine = create_engine(
                self._config.database_url,
                pool_size=self._config.DB_MIN_POOL_SIZE,
                max_overflow=self._config.DB_MAX_POOL_SIZE,
                pool_pre_ping=True,
                echo=False
            )
            self._session_factory = sessionmaker(
                bind=self._engine, autoflush=False, expire_on_commit=False)
            logger.info("Motor SQLAlchemy listo.")

    def close_pool(self) -> None:
        """Cierra de forma limpia todas las conexiones del motor de SQLAlchemy."""
        if self._engine:
            logger.info("Cerrando motor SQLAlchemy...")
            self._engine.dispose()
            self._engine = None
            self._session_factory = None
            logger.info("Motor SQLAlchemy cerrado correctamente.")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Administrador de contexto para obtener una sesión ORM de SQLAlchemy.
        Se asegura de cerrar la sesión automáticamente al terminar la petición.
        """
        if not self._engine or not self._session_factory:
            self.initialize_pool()

        assert self._session_factory is not None
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

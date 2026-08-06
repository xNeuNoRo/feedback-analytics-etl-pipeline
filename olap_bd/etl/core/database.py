import logging
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from .config import EtlSettings

logger = logging.getLogger(__name__)


class OlapDatabaseManager:
    """
    Manager para el Data Warehouse OLAP.
    Maneja el pool de conexiones usando SQLAlchemy.
    """

    def __init__(self, config: EtlSettings):
        self._config = config
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    def initialize(self) -> None:
        """Inicializa el engine de SQLAlchemy para la BD OLAP."""
        if not self._engine:

            logger.info(
                "Inicializando Motor SQLAlchemy para OLAP en el puerto %s...", self._config.OLAP_DB_PORT)

            # Creamos el engine de SQLAlchemy con la URL de conexión a la BD OLAP
            self._engine = create_engine(
                self._config.olap_database_url,
                pool_pre_ping=True,
                echo=False
            )

            # Creamos la factory de sesiones para manejar las transacciones con la BD OLAP
            self._session_factory = sessionmaker(
                bind=self._engine, autoflush=False, expire_on_commit=False)

            logger.info("Motor SQLAlchemy OLAP inicializado con éxito.")

    def close(self) -> None:
        """Cierra de forma limpia el motor de la BD OLAP."""

        # Cerramos el engine de SQLAlchemy si está inicializado
        if self._engine:
            logger.info("Cerrando motor de conexiones OLAP...")
            self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Administrador de contexto para obtener una sesión ORM de la BD OLAP."""

        # Si el engine o la factory de sesiones no están inicializados, los inicializamos
        if not self._engine or not self._session_factory:
            self.initialize()

        # Aseguramos que la factory de sesiones esté disponible
        assert self._session_factory is not None
        session: Session = self._session_factory()

        # Manejamos la sesión con un contexto que asegura commit o rollback según corresponda, y cerramos la sesión al finalizarsssss
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class OltpDatabaseManager:
    """
    Manager para conectarse a la Base de Datos Relacional OLTP.
    Maneja el pool de conexiones a la BD OLTP de forma independiente dentro del ETL.
    """

    def __init__(self, config: EtlSettings):
        self._config = config
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    def initialize(self) -> None:
        """Inicializa el engine de SQLAlchemy para la BD OLTP."""
        if not self._engine:
            logger.info("Inicializando Motor SQLAlchemy para OLTP en el puerto %s...", self._config.OLTP_DB_PORT)
            self._engine = create_engine(
                self._config.oltp_database_url,
                pool_pre_ping=True,
                echo=False
            )
            self._session_factory = sessionmaker(
                bind=self._engine, autoflush=False, expire_on_commit=False)

    def close(self) -> None:
        """Cierra de forma limpia el motor de la BD OLTP."""
        if self._engine:
            logger.info("Cerrando motor de conexiones OLTP...")
            self._engine.dispose()
            self._engine = None
            self._session_factory = None

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Administrador de contexto para obtener una sesión de la BD OLTP."""
        if not self._engine or not self._session_factory:
            self.initialize()
        assert self._session_factory is not None
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

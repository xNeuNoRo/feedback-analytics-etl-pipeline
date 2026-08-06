from dependency_injector import containers, providers
from core.config import settings
from core.database import DatabaseManager
from infrastructure.repositories.feedback_repository import FeedbackRepository
from services.feedback_service import FeedbackService


class Container(containers.DeclarativeContainer):
    """
    Contenedor de Inyección de Dependencias (IoC).
    Conecta y administra la creación de objetos (servicios, repositorios, base de datos).
    """

    wiring_config = containers.WiringConfiguration(
        modules=[
            "routers.feedback_router",
        ]
    )

    # Singleton de la config de la app
    config = providers.Singleton(lambda: settings)

    # Singleton del DatabaseManager (pool de conexiones)
    db_manager = providers.Singleton(
        DatabaseManager,
        config=config
    )

    # Factory del repositorio de feedbacks (Se crea uno nuevo cuando se solicita)
    feedback_repository = providers.Factory(
        FeedbackRepository,
        db_manager=db_manager
    )

    # Factory del servicio de feedbacks (Se crea uno nuevo cuando se solicita)
    feedback_service = providers.Factory(
        FeedbackService,
        repository=feedback_repository
    )

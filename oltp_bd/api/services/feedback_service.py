import logging
from typing import List
from domain.interfaces.i_feedback_repository import IFeedbackRepository
from domain.models.feedback_dto import FeedbackEnrichedDTO

logger = logging.getLogger(__name__)


class FeedbackService:
    """
    Servicio de la aplicación que maneja los casos de uso para consultar feedbacks.
    """

    def __init__(self, repository: IFeedbackRepository):
        self._repository = repository

    def get_social_media_feedbacks(self, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Caso de uso => Obtener todos los feedbacks que provienen de Redes Sociales con paginación.
        """
        logger.info(
            "Ejecutando caso de uso: get_social_media_feedbacks (skip=%d, limit=%d)", skip, limit)
        return self._repository.get_feedbacks_by_source_type("social", skip=skip, limit=limit)

    def get_web_reviews(self, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Caso de uso => Obtener todos los feedbacks que provienen de la Web con paginación.
        """
        logger.info(
            "Ejecutando caso de uso: get_web_reviews (skip=%d, limit=%d)", skip, limit)
        return self._repository.get_feedbacks_by_source_type("Web", skip=skip, limit=limit)

    def get_feedbacks_by_platform(self, platform_name: str, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Caso de uso => Obtener todos los feedbacks de una plataforma específica con paginación.
        """
        logger.info("Ejecutando caso de uso: get_feedbacks_by_platform('%s', skip=%d, limit=%d)",
                    platform_name, skip, limit)
        return self._repository.get_feedbacks_by_platform(platform_name, skip=skip, limit=limit)

    def get_all_feedbacks(self, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Caso de uso => Obtener absolutamente todos los feedbacks almacenados en OLTP con paginación.
        """
        logger.info(
            "Ejecutando caso de uso: get_all_feedbacks (skip=%d, limit=%d)", skip, limit)
        return self._repository.get_all_feedbacks(skip=skip, limit=limit)

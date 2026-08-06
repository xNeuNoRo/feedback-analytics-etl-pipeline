from abc import ABC, abstractmethod
from typing import List
from domain.models.feedback_dto import FeedbackEnrichedDTO


class IFeedbackRepository(ABC):
    """
    Interfaz abstracta para las operaciones de lectura de feedbacks.
    """

    @abstractmethod
    def get_feedbacks_by_source_type(self, source_type_name: str, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Obtiene registros de feedback enriquecidos según el tipo de fuente con paginación.
        """
        pass

    @abstractmethod
    def get_feedbacks_by_platform(self, platform_name: str, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Obtiene registros de feedback enriquecidos según la plataforma especificada con paginación.
        """
        pass

    @abstractmethod
    def get_all_feedbacks(self, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """
        Obtiene registros de feedback almacenados en la BD OLTP con paginación.
        """
        pass

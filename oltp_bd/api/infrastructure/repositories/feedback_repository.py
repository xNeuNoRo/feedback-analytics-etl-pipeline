import json
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from core.database import DatabaseManager
from domain.interfaces.i_feedback_repository import IFeedbackRepository
from domain.models.feedback_dto import (
    FeedbackEnrichedDTO,
    ClientDTO,
    ProductDTO,
    SourceDTO,
)
from infrastructure.models import (
    Feedback,
    Product,
    Source,
    SourceType,
)

logger = logging.getLogger(__name__)


class FeedbackRepository(IFeedbackRepository):
    """
    Implementación concreta del repositorio usando modelos SQLAlchemy.
    """

    def __init__(self, db_manager: DatabaseManager):
        self._dbinfo = db_manager

    def _map_orm_to_dto(self, fb: Feedback) -> FeedbackEnrichedDTO:
        """Convierte una entidad mapeada Feedback a un objeto DTO validado (FeedbackEnrichedDTO)."""
        # Extraemos la metadata del cliente
        metadata: Dict[str, Any] = {}
        raw_metadata = fb.metadata_json
        if isinstance(raw_metadata, dict):
            metadata = raw_metadata
        elif isinstance(raw_metadata, str) and raw_metadata.strip():
            try:
                metadata = json.loads(raw_metadata)
            except json.JSONDecodeError:
                metadata = {}

        country = metadata.get("country", metadata.get("pais", "Desconocido"))
        age_group = metadata.get(
            "age_group", metadata.get("edad", "Desconocido"))
        client_type = metadata.get(
            "client_type", metadata.get("tipo", "Regular"))

        # Construimos el ClientDTO
        client_dto = ClientDTO(
            id=fb.client.id if fb.client else None,
            name=fb.client.name if fb.client else "Cliente Anónimo",
            email=fb.client.email if fb.client else None,
            country=str(country),
            age_group=str(age_group),
            client_type=str(client_type)
        )

        # Construimos el ProductDTO (si existe)
        product_dto: Optional[ProductDTO] = None
        if fb.product:
            product_dto = ProductDTO(
                id=fb.product.id,
                name=fb.product.name,
                category_name=fb.product.category.name if fb.product.category else "Sin Categoría"
            )

        # Construimos el SourceDTO
        source_dto = SourceDTO(
            id=fb.source.id if fb.source else "UNKNOWN",
            source_type_name=fb.source.source_type.name if (
                fb.source and fb.source.source_type) else "Desconocido",
            platform=fb.platform or "Desconocido"
        )

        # Construimos el FeedbackEnrichedDTO final
        return FeedbackEnrichedDTO(
            external_id=fb.external_id,
            comment=fb.comment,
            rating=fb.rating,
            created_at=fb.created_at,
            sentiment=fb.sentiment,
            client=client_dto,
            product=product_dto,
            source=source_dto
        )

    def _get_base_statement(self):
        """Construye la consulta base cargando todas las relaciones con joinedload"""
        return (
            select(Feedback)
            .options(
                joinedload(Feedback.client),
                joinedload(Feedback.product).joinedload(
                    Product.category),
                joinedload(Feedback.source).joinedload(
                    Source.source_type)
            )
            .order_by(Feedback.created_at.desc())
        )

    def get_feedbacks_by_source_type(self, source_type_name: str, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """Obtiene feedbacks filtrados por el tipo de fuente (búsqueda flexible por coincidencia exacta o substring)."""
        pattern = f"%{source_type_name.lower().strip()}%"
        stmt = (
            self._get_base_statement()
            .join(Feedback.source)
            .join(Source.source_type)
            .where(
                (func.lower(SourceType.name) == source_type_name.lower()) |
                (func.lower(SourceType.name).like(pattern))
            )
            .offset(skip)
            .limit(limit)
        )
        with self._dbinfo.get_session() as session:
            feedbacks = session.scalars(stmt).unique().all()
            logger.info("[SQLAlchemy]: Se encontraron %d registros para source_type '%s' (skip=%d, limit=%d)", len(
                feedbacks), source_type_name, skip, limit)
            return [self._map_orm_to_dto(fb) for fb in feedbacks]

    def get_feedbacks_by_platform(self, platform_name: str, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """Obtiene feedbacks filtrados por la plataforma"""
        stmt = (
            self._get_base_statement()
            .where(func.lower(Feedback.platform) == platform_name.lower())
            .offset(skip)
            .limit(limit)
        )
        with self._dbinfo.get_session() as session:
            feedbacks = session.scalars(stmt).unique().all()
            logger.info("[SQLAlchemy]: Se encontraron %d registros para la plataforma '%s' (skip=%d, limit=%d)", len(
                feedbacks), platform_name, skip, limit)
            return [self._map_orm_to_dto(fb) for fb in feedbacks]

    def get_all_feedbacks(self, skip: int = 0, limit: int = 1000) -> List[FeedbackEnrichedDTO]:
        """Obtiene todos los feedbacks almacenados en OLTP"""
        stmt = (
            self._get_base_statement()
            .offset(skip)
            .limit(limit)
        )
        with self._dbinfo.get_session() as session:
            feedbacks = session.scalars(stmt).unique().all()
            logger.info("[SQLAlchemy]: Se encontraron %d registros en total (skip=%d, limit=%d)", len(
                feedbacks), skip, limit)
            return [self._map_orm_to_dto(fb) for fb in feedbacks]

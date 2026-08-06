from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.models.base import Base

if TYPE_CHECKING:
    from infrastructure.models.source_type import SourceType
    from infrastructure.models.feedback import Feedback


class Source(Base):
    """Modelo mapeado a la tabla 'sources' de la BD OLTP."""
    __tablename__ = "sources"

    # Id de la fuente, clave primaria, no autoincremental
    id: Mapped[str] = mapped_column(String(50), primary_key=True)

    # Id del tipo de fuente, clave foránea a la tabla 'source_types', no nulo
    source_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("source_types.id"), nullable=False)

    # Fecha de carga de la fuente, opcional, por defecto la fecha actual
    upload_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=datetime.utcnow)

    # Relación con la tabla 'source_types', una fuente pertenece a un tipo de fuente
    source_type: Mapped["SourceType"] = relationship(back_populates="sources")

    # Relación con la tabla 'feedbacks', una fuente puede tener muchos feedbacks
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="source")

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.models.base import Base

if TYPE_CHECKING:
    from infrastructure.models.client import Client
    from infrastructure.models.product import Product
    from infrastructure.models.source import Source


class Feedback(Base):
    """Modelo mapeado a la tabla 'feedbacks' de la BD OLTP."""
    __tablename__ = "feedbacks"

    # Id del feedback, clave primaria, autoincremental
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    # Id externo del feedback, opcional
    external_id: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True)

    # Id del producto, opcional
    product_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("products.id"), nullable=True)

    # Id del cliente, opcional
    client_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("clients.id"), nullable=True)

    # Id de la fuente, obligatorio
    source_id: Mapped[str] = mapped_column(
        String(50), ForeignKey("sources.id"), nullable=False)

    # Plataforma de la que proviene el feedback, obligatorio
    platform: Mapped[str] = mapped_column(String(50), nullable=False)

    # Contenido del feedback, obligatorio
    comment: Mapped[str] = mapped_column(Text, nullable=False)

    # Fecha de creación del feedback, obligatorio, por defecto la fecha actual
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)

    # Calificación del feedback, opcional
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Sentimiento del feedback, opcional
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Metadatos adicionales del feedback, opcional, almacenados en formato JSON
    metadata_json: Mapped[Optional[Any]] = mapped_column(
        "metadata", JSONB, nullable=True)

    # Relaciones con las tablas 'clients', 'products' y 'sources'
    client: Mapped[Optional["Client"]] = relationship(
        back_populates="feedbacks")
    product: Mapped[Optional["Product"]] = relationship(
        back_populates="feedbacks")
    source: Mapped["Source"] = relationship(back_populates="feedbacks")

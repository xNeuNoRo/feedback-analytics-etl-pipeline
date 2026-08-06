from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.models.base import Base

if TYPE_CHECKING:
    from infrastructure.models.source import Source


class SourceType(Base):
    """Modelo mapeado a la tabla 'source_types' de la BD OLTP."""
    __tablename__ = "source_types"

    # Id del tipo de fuente, clave primaria, autoincremental
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    # Nombre del tipo de fuente, único y no nulo
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # Relación con la tabla 'sources', un tipo de fuente puede tener muchas fuentes
    sources: Mapped[list["Source"]] = relationship(
        back_populates="source_type")

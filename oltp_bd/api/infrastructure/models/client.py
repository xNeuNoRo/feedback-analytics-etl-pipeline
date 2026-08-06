from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.models.base import Base

if TYPE_CHECKING:
    from infrastructure.models.feedback import Feedback


class Client(Base):
    """Modelo mapeado a la tabla 'clients' de la BD OLTP."""
    __tablename__ = "clients"

    # Id del cliente, clave primaria, autoincremental
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    # Nombre y correo electrónico del cliente, ambos no nulos
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relación con la tabla 'feedbacks', un cliente puede tener muchos feedbacks
    feedbacks: Mapped[list["Feedback"]] = relationship(back_populates="client")

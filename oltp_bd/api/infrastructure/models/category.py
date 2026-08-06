from typing import TYPE_CHECKING
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.models.base import Base

if TYPE_CHECKING:
    from infrastructure.models.product import Product


class Category(Base):
    """Modelo mapeado a la tabla 'categories' de la BD OLTP."""
    __tablename__ = "categories"

    # Id de la categoría, clave primaria, autoincremental
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    # Nombre de la categoría, único y no nulo
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relación con la tabla 'products', una categoría puede tener muchos productos
    products: Mapped[list["Product"]] = relationship(back_populates="category")

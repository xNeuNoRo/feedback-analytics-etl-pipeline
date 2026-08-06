from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.models.base import Base

if TYPE_CHECKING:
    from infrastructure.models.category import Category
    from infrastructure.models.feedback import Feedback


class Product(Base):
    """Modelo mapeado a la tabla 'products' de la BD OLTP."""
    __tablename__ = "products"

    # Id del producto, clave primaria, autoincremental
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    # Nombre del producto, no nulo
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Id de la categoría a la que pertenece el producto, no nulo
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False)

    # Relación con la tabla 'categories', un producto pertenece a una categoría
    category: Mapped["Category"] = relationship(back_populates="products")

    # Relación con la tabla 'feedbacks', un producto puede tener muchos feedbacks
    feedbacks: Mapped[list["Feedback"]] = relationship(
        back_populates="product")

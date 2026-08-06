from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from load.models.base import OlapBase


class DimProduct(OlapBase):
    """Modelo mapeado a dim_product."""
    __tablename__ = "dim_product"

    product_key: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    original_product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_name: Mapped[str] = mapped_column(String(255), nullable=False)

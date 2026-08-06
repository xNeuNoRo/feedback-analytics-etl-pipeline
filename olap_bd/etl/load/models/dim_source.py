from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from load.models.base import OlapBase


class DimSource(OlapBase):
    """Modelo mapeado a dim_source."""
    __tablename__ = "dim_source"

    source_key: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    original_source_id: Mapped[str] = mapped_column(String(50), nullable=False)
    source_type_name: Mapped[str] = mapped_column(String(50), nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)

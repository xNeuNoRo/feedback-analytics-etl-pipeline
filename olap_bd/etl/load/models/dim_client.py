from typing import Optional
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from load.models.base import OlapBase


class DimClient(OlapBase):
    """Modelo mapeado a dim_client."""
    __tablename__ = "dim_client"

    client_key: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    original_client_id: Mapped[Optional[int]
                               ] = mapped_column(Integer, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(
        String(100), default="Desconocido", nullable=False)
    age_group: Mapped[str] = mapped_column(
        String(50), default="Desconocido", nullable=False)
    client_type: Mapped[str] = mapped_column(
        String(50), default="Regular", nullable=False)

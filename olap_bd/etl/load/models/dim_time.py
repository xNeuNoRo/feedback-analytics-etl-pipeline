from datetime import date
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column
from load.models.base import OlapBase


class DimTime(OlapBase):
    """Modelo mapeado a dim_time."""
    __tablename__ = "dim_time"

    time_key: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    full_date: Mapped[date] = mapped_column(Date, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter_num: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter_name: Mapped[str] = mapped_column(String(2), nullable=False)
    day_of_week_num: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week_name: Mapped[str] = mapped_column(String(20), nullable=False)

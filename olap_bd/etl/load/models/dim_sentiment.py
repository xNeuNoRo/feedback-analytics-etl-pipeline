from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from load.models.base import OlapBase


class DimSentiment(OlapBase):
    """Modelo mapeado a dim_sentiment."""
    __tablename__ = "dim_sentiment"

    sentiment_key: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    sentiment_name: Mapped[str] = mapped_column(String(20), nullable=False)

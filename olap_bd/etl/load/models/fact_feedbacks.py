from typing import Optional
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from load.models.base import OlapBase


class FactFeedbacks(OlapBase):
    """Modelo mapeado a la tabla de hechos fact_feedbacks."""
    __tablename__ = "fact_feedbacks"

    feedback_key: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    time_key: Mapped[int] = mapped_column(
        Integer, ForeignKey("dim_time.time_key"), nullable=False)
    client_key: Mapped[int] = mapped_column(
        Integer, ForeignKey("dim_client.client_key"), nullable=False)
    product_key: Mapped[int] = mapped_column(
        Integer, ForeignKey("dim_product.product_key"), nullable=False)
    source_key: Mapped[int] = mapped_column(
        Integer, ForeignKey("dim_source.source_key"), nullable=False)
    sentiment_key: Mapped[int] = mapped_column(
        Integer, ForeignKey("dim_sentiment.sentiment_key"), nullable=False)

    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    feedback_count: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    original_feedback_external_id: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True)

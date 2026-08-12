from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session


class FactFeedbacksDao:
    """DAO para la gestión e inserción masiva en fact_feedbacks llamando a los Stored Procedures de la BD OLAP."""

    def clean_facts(self, session: Session) -> None:
        """Invoca el Stored Procedure sp_clean_fact_feedbacks en la BD OLAP para truncar la tabla de hechos."""
        stmt = text("CALL sp_clean_fact_feedbacks();")
        session.execute(stmt)

    def insert_fact(
        self,
        session: Session,
        time_key: int,
        client_key: int,
        product_key: int,
        source_key: int,
        sentiment_key: int,
        fact_item: Dict[str, Any]
    ) -> None:
        """Invoca el Stored Procedure sp_insert_fact_feedback en la BD OLAP para insertar el hecho."""
        stmt = text("""
            CALL sp_insert_fact_feedback(
                CAST(:time_key AS int),
                CAST(:client_key AS int),
                CAST(:product_key AS int),
                CAST(:source_key AS int),
                CAST(:sentiment_key AS int),
                CAST(:rating AS int),
                CAST(:feedback_count AS int),
                CAST(:comment_text AS text),
                CAST(:original_feedback_external_id AS varchar)
            );
        """)

        # Ejecutamos la query para insertar el hecho en la BD OLAP
        session.execute(stmt, {
            "time_key": time_key,
            "client_key": client_key,
            "product_key": product_key,
            "source_key": source_key,
            "sentiment_key": sentiment_key,
            "rating": fact_item.get("rating"),
            "feedback_count": fact_item.get("feedback_count", 1),
            "comment_text": fact_item.get("comment_text", ""),
            "original_feedback_external_id": fact_item.get("original_external_id")
        })

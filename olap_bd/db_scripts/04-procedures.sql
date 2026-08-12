--------------------
-- procedures sql --
--------------------

create procedure sp_clean_fact_feedbacks()
    language plpgsql
as
$$
begin
    -- vaciamos la tabla fact_feedbacks reiniciando la secuencia de llaves primarias
    truncate table fact_feedbacks restart identity;
end;
$$;

create procedure sp_insert_fact_feedback(
    p_time_key int,
    p_client_key int,
    p_product_key int,
    p_source_key int,
    p_sentiment_key int,
    p_rating int,
    p_feedback_count int,
    p_comment_text text,
    p_original_external_id varchar
)
    language plpgsql
as
$$
begin
    -- insertamos el hecho en la tabla fact_feedbacks
    insert into fact_feedbacks (time_key, client_key, product_key, source_key, sentiment_key, rating,
                           feedback_count, comment_text, original_feedback_external_id)
    values (p_time_key, p_client_key, p_product_key, p_source_key, p_sentiment_key, p_rating,
            coalesce(p_feedback_count, 1), p_comment_text, p_original_external_id);
end;
$$;

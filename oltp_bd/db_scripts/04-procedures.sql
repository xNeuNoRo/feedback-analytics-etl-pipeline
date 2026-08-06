--------------------
-- procedures sql --
--------------------

create procedure sp_insert_feedback(
    p_external_id varchar,
    p_product_id int,
    p_client_id int,
    p_source_id varchar,
    p_platform varchar,
    p_comment text,
    p_created_at timestamp,
    p_rating int,
    p_sentiment varchar
)
    language plpgsql
as
$$
begin
    -- Si no existe el producto con el id proporcionado,
    -- Lo ponemos como null para que no se inserte un registro con un product_id no valido
    if p_product_id is not null and not exists (select 1 from products where id = p_product_id) then
        p_product_id := null;
    end if;

    -- Si no existe el cliente con el id proporcionado,
    -- Lo ponemos como null para que no se inserte un registro con un client_id no valido
    if p_client_id is not null and not exists (select 1 from clients where id = p_client_id) then
        p_client_id := null;
    end if;

    insert into feedbacks (external_id, product_id, client_id, source_id, platform, comment, created_at, rating,
                           sentiment)
    values (p_external_id, p_product_id, p_client_id, p_source_id, p_platform, p_comment, p_created_at, p_rating,
            p_sentiment)
    on conflict (external_id) do nothing;
end;
$$;
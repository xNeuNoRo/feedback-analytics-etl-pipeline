-------------------
-- funciones sql --
-------------------


--- DIM TIME ---
create function fn_upsert_dim_time(
    p_full_date date,
    p_year int,
    p_month int,
    p_quarter_num int,
    p_quarter_name varchar,
    p_day_of_week_num int,
    p_day_of_week_name varchar
)
    returns int
    language plpgsql
as
$$
declare
    v_time_key int;
begin
    -- buscamos si ya existe el registro de tiempo
    select time_key into v_time_key
    from dim_time
    where full_date = p_full_date;

    if v_time_key is not null then
        return v_time_key;
    end if;

    -- insertamos la nueva fecha en la dimension
    insert into dim_time (full_date, year, month, quarter_num, quarter_name, day_of_week_num, day_of_week_name)
    values (p_full_date, p_year, p_month, p_quarter_num, p_quarter_name, p_day_of_week_num, p_day_of_week_name)
    returning time_key into v_time_key;

    -- retornamos la variable con la llave de tiempo
    return v_time_key;
end;
$$;


--- DIM CLIENT ---
create function fn_upsert_dim_client(
    p_original_client_id int,
    p_name varchar,
    p_email varchar,
    p_country varchar,
    p_age_group varchar,
    p_client_type varchar
)
    returns int
    language plpgsql
as
$$
declare
    v_client_key int;
begin
    -- buscamos el id de la dimension cliente por id original o por nombre
    if p_original_client_id is not null then
        select client_key into v_client_key
        from dim_client
        where original_client_id = p_original_client_id;
    else
        select client_key into v_client_key
        from dim_client
        where name = p_name and original_client_id is null;
    end if;

    if v_client_key is not null then
        return v_client_key;
    end if;

    -- insertamos el cliente en la dimension
    insert into dim_client (original_client_id, name, email, country, age_group, client_type)
    values (p_original_client_id, coalesce(p_name, 'Cliente Anónimo'), p_email,
            coalesce(p_country, 'Desconocido'), coalesce(p_age_group, 'Desconocido'), coalesce(p_client_type, 'Regular'))
    returning client_key into v_client_key;

    -- retornamos la variable con la llave del cliente
    return v_client_key;
end;
$$;


--- DIM PRODUCT ---
create function fn_upsert_dim_product(
    p_original_product_id int,
    p_product_name varchar,
    p_category_name varchar
)
    returns int
    language plpgsql
as
$$
declare
    v_product_key int;
begin
    -- buscamos el id de la dimension producto
    select product_key into v_product_key
    from dim_product
    where original_product_id = p_original_product_id;

    if v_product_key is not null then
        return v_product_key;
    end if;

    -- insertamos el producto en la dimension
    insert into dim_product (original_product_id, product_name, category_name)
    values (coalesce(p_original_product_id, 0), coalesce(p_product_name, 'Producto General'), coalesce(p_category_name, 'General'))
    returning product_key into v_product_key;

    -- retornamos la variable con la llave del producto
    return v_product_key;
end;
$$;


--- DIM SOURCE ---
create function fn_upsert_dim_source(
    p_original_source_id varchar,
    p_source_type_name varchar,
    p_platform varchar
)
    returns int
    language plpgsql
as
$$
declare
    v_source_key int;
begin
    -- buscamos el id de la dimension fuente
    select source_key into v_source_key
    from dim_source
    where original_source_id = p_original_source_id and platform = p_platform;

    if v_source_key is not null then
        return v_source_key;
    end if;

    -- insertamos la fuente en la dimension
    insert into dim_source (original_source_id, source_type_name, platform)
    values (coalesce(p_original_source_id, 'SRC-UNKNOWN'), coalesce(p_source_type_name, 'General'), coalesce(p_platform, 'General'))
    returning source_key into v_source_key;

    -- retornamos la variable con la llave de la fuente
    return v_source_key;
end;
$$;


--- DIM SENTIMENT ---
create function fn_upsert_dim_sentiment(
    p_sentiment_name varchar
)
    returns int
    language plpgsql
as
$$
declare
    v_sentiment_key int;
begin
    -- buscamos el id de la dimension sentimiento
    select sentiment_key into v_sentiment_key
    from dim_sentiment
    where sentiment_name = p_sentiment_name;

    if v_sentiment_key is not null then
        return v_sentiment_key;
    end if;

    -- insertamos el sentimiento en la dimension
    insert into dim_sentiment (sentiment_name)
    values (coalesce(p_sentiment_name, 'Neutro'))
    returning sentiment_key into v_sentiment_key;

    -- retornamos la variable con la llave del sentimiento
    return v_sentiment_key;
end;
$$;

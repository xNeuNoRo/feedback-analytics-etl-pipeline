-------------------
-- funciones sql --
-------------------


--- CATEGORIES ---
create function fn_upsert_category(p_name varchar)
    returns int
    language plpgsql
as
$$
declare
    v_category_id int;
begin
    -- insertamos o actualizamos la categoria
    insert into categories (name)
    values (p_name)
    on conflict (name) do update -- si ya existe, actualizamos
        set name = excluded.name -- para que no haga nada, pero nos retorne el id
    -- establecemos el id de la categoria en la variable
    returning id into v_category_id;

    -- retornamos la variable con el id de la categoria
    return v_category_id;
end;
$$;

--- PRODUCTS ---
create function fn_upsert_product(p_product_name varchar, p_category_name varchar)
    returns int
    language plpgsql
as
$$
declare
    v_category_id int;
    v_product_id  int;
begin
    -- primero conseguimos el id de la categoria usando la funcion de upsert de categoria
    v_category_id := fn_upsert_category(p_category_name);

    insert into products (name, category_id)
    values (p_product_name, v_category_id)
    on conflict (name) do update -- si ya existe, actualizamos
        set name = excluded.name, category_id = excluded.category_id -- para que no haga nada, pero nos retorne el id
    -- establecemos el id del producto en la variable
    returning id into v_product_id;

    -- retornamos la variable con el id del producto
    return v_product_id;
end;
$$;

--- CLIENTS ---
create function fn_upsert_client(p_name varchar, p_email varchar)
    returns int
    language plpgsql
as
$$
declare
    v_client_id int;
begin
    insert into clients (name, email)
    values (p_name, p_email)
    on conflict (email) do update
        set name = excluded.name -- para que no haga nada, pero nos retorne el id
    -- establecemos el id del cliente en la variable
    returning id into v_client_id;

    -- retornamos la variable con el id del cliente
    return v_client_id;
end;
$$;

--- SOURCE TYPES ---
create function fn_upsert_source_type(p_name varchar)
    returns int
    language plpgsql
as
$$
declare
    v_type_id int;
begin
    insert into source_types (name)
    values (p_name)
    on conflict (name) do update
        set name = excluded.name -- para que no haga nada, pero nos retorne el id
    -- establecemos el id del tipo de fuente en la variable
    returning id into v_type_id;

    -- retornamos la variable con el id del tipo de fuente
    return v_type_id;
end;
$$;

--- SOURCES ---
create function fn_upsert_source(p_source_id varchar, p_source_type_name varchar, p_upload_date timestamp)
    returns varchar
    language plpgsql
as
$$
declare
    v_type_id            int;
    v_returned_source_id varchar;
begin
    -- insertamos o actualizamos el tipo de fuente, asi tenemos el id
    v_type_id := fn_upsert_source_type(p_source_type_name);

    -- insertamos o actualizamos la fuente
    insert into sources (id, source_type_id, upload_date)
    values (p_source_id, v_type_id, p_upload_date)
    on conflict (id) do update
        set source_type_id = excluded.source_type_id, upload_date = excluded.upload_date -- para que no haga nada, pero nos retorne el id
    -- establecemos el id de la fuente en la variable
    returning id into v_returned_source_id;

    -- retornamos la variable con el id de la fuente
    return v_returned_source_id;
end;
$$;
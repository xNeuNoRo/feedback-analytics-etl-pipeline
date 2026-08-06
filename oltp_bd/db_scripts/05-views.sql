------------------------
-- queries (view) sql --
------------------------

--- CATEGORIES ---

-- Conteo de productos por categoria
-- ej: cuantas categorias hay, y cuantas productos tiene cada categoria
create view vw_category_product_count as
select cat.id      as category_id,
       cat.name    as category_name,
       count(p.id) as total_products
from categories cat
         left join products p on cat.id = p.category_id
group by cat.id, cat.name
order by total_products desc;

-- Desglose de sentimientos por categoria
-- ej: cuantas opiniones positivas, negativas y neutras hay por categoria
create view vw_category_sentiment_breakdown as
select cat.id      as category_id,
       cat.name    as category_name,
       f.sentiment as sentiment_type,
       count(f.id) as total_feedbacks
from categories cat
         inner join products p on cat.id = p.category_id
         inner join feedbacks f on p.id = f.product_id
where f.sentiment is not null
group by cat.id, cat.name, f.sentiment
order by cat.name, f.sentiment desc;

-- satisfaccion global por categoria
-- ej: promedio de calificacion por categoria, y cantidad de opiniones calificadas
create view vw_category_overall_satisfaction as
select cat.id                  as category_id,
       cat.name                as category_name,
       count(f.id)             as total_rated_feedbacks,
       round(avg(f.rating), 2) as average_rating
from categories cat
         inner join products p on cat.id = p.category_id
         inner join feedbacks f on p.id = f.product_id
where f.rating is not null
group by cat.id, cat.name
order by average_rating desc;

--- PRODUCTS ---

-- satisfaccion y sentimiento por producto
-- ej: promedio de calificacion por producto, cantidad de opiniones calificadas y desglose de sentimientos
create view vw_product_overall_satisfaction as
select p.id                    as product_id,
       p.name                  as product_name,
       cat.name                as category_name,
       f.sentiment             as sentiment_type,
       count(f.id)             as total_feedbacks,
       round(avg(f.rating), 2) as average_rating
from products p
         inner join categories cat on p.category_id = cat.id
         inner join feedbacks f on p.id = f.product_id
where f.sentiment is not null
group by p.id, p.name, cat.name, f.sentiment
order by product_name, total_feedbacks desc;

-- tendencia de opiniones por producto (a lo largo del tiempo)
-- ej: cuantas opiniones positivas, negativas y neutras hay por producto, agrupadas por mes
create view vw_product_sentiment_trends as
select p.id                                    as product_id,
       p.name                                  as product_name,
       -- date_trunc para agrupar por mes, de esta manera podemos
       -- ver la tendencia de opiniones a lo largo del tiempo
       date_trunc('month', f.created_at)::date as feedback_month,
       f.sentiment                             as sentiment_type,
       count(f.id)                             as total_feedbacks,
       round(avg(f.rating), 2)                 as average_rating
from products p
         inner join feedbacks f on p.id = f.product_id
where f.sentiment is not null
group by p.id, p.name, feedback_month, f.sentiment
order by product_name, feedback_month;


--- CLIENTS ---

-- actividad de clientes
-- ej: cuantas opiniones ha dejado cada cliente, promedio de calificacion y sentimiento predominante en sus opiniones
create view vw_client_activity as
select c.id                                       as client_id,
       c.name                                     as client_name,
       c.email                                    as client_email,
       count(f.id)                                as total_feedbacks,
       count(f.sentiment)                         as total_feedbacks_with_sentiment,
       round(avg(f.rating), 2)                    as average_rating_given,
       -- mode() within group nos permite obtener el valor mas frecuente de un grupo,
       -- en este caso el sentimiento predominante del cliente con (order by f.sentiment)
       mode() within group (order by f.sentiment) as predominant_sentiment
from clients c
         left join feedbacks f on c.id = f.client_id
group by c.id, c.name, c.email
order by total_feedbacks desc;

-- preferencia de plataforma de clientes
-- ej: en que plataforma interactua mas cada cliente, y cuantas interacciones ha tenido
create view vw_client_platform_preference as
select c.id        as client_id,
       c.name      as client_name,
       f.platform  as platform,
       count(f.id) as interactions_on_platform
from clients c
         inner join feedbacks f on c.id = f.client_id
group by c.id, c.name, f.platform
order by c.name, interactions_on_platform desc;


--- SOURCES_TYPES ---

-- volumen de opiniones por tipo de fuente y rating promedio por tipo de fuente
-- ej: cuantas opiniones han llegado por cada tipo de fuente, y cual es el rating promedio de esas opiniones
create view vw_source_volume_kpi as
select st.id                   as source_type_id,
       st.name                 as source_channel,
       count(f.id)             as total_feedbacks,
       round(avg(f.rating), 2) as average_rating
from source_types st
         inner join sources s on st.id = s.source_type_id
         inner join feedbacks f on s.id = f.source_id
group by st.id, st.name
order by total_feedbacks desc;

-- desglose de sentimientos por tipo de fuente
-- ej: cuantas opiniones positivas, negativas, etc han llegado por cada tipo de fuente
create view vw_source_sentiment_breakdown as
select st.id       as source_type_id,
       st.name     as source_channel,
       f.sentiment as sentiment_type,
       count(f.id) as total_feedbacks
from source_types st
         inner join sources s on st.id = s.source_type_id
         inner join feedbacks f on s.id = f.source_id
where f.sentiment is not null
group by st.id, st.name, f.sentiment
order by source_channel, total_feedbacks desc;

--- VISTA MAESTRA DE FEEDBACKS ---

-- Esta vista nos permite tener todos los datos de un feedback en una sola consulta,
-- incluyendo datos del cliente, producto, categoria, fuente y tipo de fuente.
-- ej: Podemos usar esta vista para obtener un reporte completo de feedbacks, con toda la informacion relevante en una sola tabla.
create view vw_feedbacks_master as
select
    -- Ids de feedbacks
    f.id                                    as internal_id,
    f.external_id,
    -- Datoss del cliente
    c.name                                  as client_name,
    c.email                                 as client_email,
    -- Datos del producto y categoria
    p.name                                  as product_name,
    cat.name                                as category_name,
    -- Datos de la fuente y tipo de fuente
    st.name                                 as source_channel,
    f.platform,
    -- Datos del feedback
    f.rating,
    f.sentiment,
    f.comment,
    f.created_at                            as feedback_date,
    date_trunc('month', f.created_at)::date as feedback_month
from feedbacks f
         -- left join porque el cliente puede ser anonimo
         left join clients c on f.client_id = c.id
    -- Los demas datos ya sabemos que existen porque no pueden ser nulos
         inner join products p on f.product_id = p.id
         inner join categories cat on p.category_id = cat.id
         inner join sources s on f.source_id = s.id
         inner join source_types st on s.source_type_id = st.id
order by f.created_at desc;

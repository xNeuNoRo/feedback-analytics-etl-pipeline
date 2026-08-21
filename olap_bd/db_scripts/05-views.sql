---------------
-- views sql --
---------------

-- Vista de resumen de kpis generales
-- responde a: total de comentarios, promedio general de satisfaccion y distribucion global de sentimientos
create or replace view vw_kpi_general as
select
    count(f.feedback_key) as total_comentarios,
    round(avg(f.rating), 2) as rating_promedio,
    count(case when lower(s.sentiment_name) = 'positivo' then 1 end) as total_positivos,
    round((count(case when lower(s.sentiment_name) = 'positivo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_positivos,
    count(case when lower(s.sentiment_name) = 'negativo' then 1 end) as total_negativos,
    round((count(case when lower(s.sentiment_name) = 'negativo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_negativos,
    count(case when lower(s.sentiment_name) = 'neutro' then 1 end) as total_neutros,
    round((count(case when lower(s.sentiment_name) = 'neutro' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_neutros,
    count(distinct f.client_key) as total_clientes_unicos,
    count(distinct f.product_key) as total_productos_evaluados,
    count(distinct f.source_key) as total_canales_utilizados
from fact_feedbacks f
left join dim_sentiment s on f.sentiment_key = s.sentiment_key;


-- Vista de analisis y satisfaccion por producto
-- responde a: producto con mas comentarios, mejor calificacion promedio, mas opiniones negativas y % de satisfaccion
create or replace view vw_analisis_por_producto as
select
    p.product_key,
    p.original_product_id,
    p.product_name,
    p.category_name,
    count(f.feedback_key) as total_comentarios,
    round(avg(f.rating), 2) as rating_promedio,
    count(case when lower(s.sentiment_name) = 'positivo' then 1 end) as total_positivos,
    round((count(case when lower(s.sentiment_name) = 'positivo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_satisfaccion,
    count(case when lower(s.sentiment_name) = 'negativo' then 1 end) as total_negativos,
    round((count(case when lower(s.sentiment_name) = 'negativo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_negativos,
    count(case when lower(s.sentiment_name) = 'neutro' then 1 end) as total_neutros,
    round((count(case when lower(s.sentiment_name) = 'neutro' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_neutros
from dim_product p
left join fact_feedbacks f on p.product_key = f.product_key
left join dim_sentiment s on f.sentiment_key = s.sentiment_key
group by p.product_key, p.original_product_id, p.product_name, p.category_name;


-- Vista de comparativa y rendimiento por canal/fuente
-- responde a: que canal genera mas comentarios, diferencias de tono por canal y canal con mayor proporcion negativa
create or replace view vw_analisis_por_canal as
select
    src.source_key,
    src.source_type_name,
    src.platform,
    count(f.feedback_key) as total_comentarios,
    round((count(f.feedback_key)::numeric / nullif((select count(*) from fact_feedbacks), 0)) * 100, 2) as pct_del_total,
    round(avg(f.rating), 2) as rating_promedio,
    count(case when lower(s.sentiment_name) = 'positivo' then 1 end) as total_positivos,
    round((count(case when lower(s.sentiment_name) = 'positivo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_positivos,
    count(case when lower(s.sentiment_name) = 'negativo' then 1 end) as total_negativos,
    round((count(case when lower(s.sentiment_name) = 'negativo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_negativos,
    count(case when lower(s.sentiment_name) = 'neutro' then 1 end) as total_neutros,
    round((count(case when lower(s.sentiment_name) = 'neutro' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_neutros
from dim_source src
left join fact_feedbacks f on src.source_key = f.source_key
left join dim_sentiment s on f.sentiment_key = s.sentiment_key
group by src.source_key, src.source_type_name, src.platform;


-- Vista de evolucion y tendencias temporales (mensual y trimestral)
-- responde a: cambio de percepcion mes a mes / trimestre a trimestre y deteccion de picos de comentarios
create or replace view vw_evolucion_temporal as
select
    t.year,
    t.month,
    t.quarter_num,
    t.quarter_name,
    to_char(t.full_date, 'yyyy-mm') as periodo_mes,
    count(f.feedback_key) as total_comentarios,
    round(avg(f.rating), 2) as rating_promedio,
    count(case when lower(s.sentiment_name) = 'positivo' then 1 end) as total_positivos,
    round((count(case when lower(s.sentiment_name) = 'positivo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_positivos,
    count(case when lower(s.sentiment_name) = 'negativo' then 1 end) as total_negativos,
    round((count(case when lower(s.sentiment_name) = 'negativo' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_negativos,
    count(case when lower(s.sentiment_name) = 'neutro' then 1 end) as total_neutros,
    round((count(case when lower(s.sentiment_name) = 'neutro' then 1 end)::numeric / nullif(count(f.feedback_key), 0)) * 100, 2) as pct_neutros
from dim_time t
left join fact_feedbacks f on t.time_key = f.time_key
left join dim_sentiment s on f.sentiment_key = s.sentiment_key
group by t.year, t.month, t.quarter_num, t.quarter_name, to_char(t.full_date, 'yyyy-mm');


-- Vista de tendencia y satisfaccion de producto a lo largo del tiempo
-- responde a: como ha variado la satisfaccion de cada producto mes a mes
create or replace view vw_tendencia_producto_tiempo as
select
    p.product_key,
    p.product_name,
    p.category_name,
    t.year,
    t.month,
    t.quarter_name,
    to_char(t.full_date, 'yyyy-mm') as periodo_mes,
    count(f.feedback_key) as total_comentarios,
    round(avg(f.rating), 2) as rating_promedio,
    count(case when lower(s.sentiment_name) = 'positivo' then 1 end) as total_positivos,
    count(case when lower(s.sentiment_name) = 'negativo' then 1 end) as total_negativos,
    count(case when lower(s.sentiment_name) = 'neutro' then 1 end) as total_neutros
from fact_feedbacks f
join dim_product p on f.product_key = p.product_key
join dim_time t on f.time_key = t.time_key
left join dim_sentiment s on f.sentiment_key = s.sentiment_key
group by p.product_key, p.product_name, p.category_name, t.year, t.month, t.quarter_name, to_char(t.full_date, 'yyyy-mm');


-- 6. vista de distribucion consolidada de sentimientos (nlp)
-- responde a: cuantas opiniones fueron clasificadas como positivas, negativas o neutras y su %
create or replace view vw_distribucion_sentimientos as
select
    s.sentiment_key,
    s.sentiment_name,
    count(f.feedback_key) as total_opiniones,
    round((count(f.feedback_key)::numeric / nullif((select count(*) from fact_feedbacks), 0)) * 100, 2) as pct_total,
    round(avg(f.rating), 2) as rating_promedio
from dim_sentiment s
left join fact_feedbacks f on s.sentiment_key = f.sentiment_key
group by s.sentiment_key, s.sentiment_name;


-- Vista de actividad y opiniones por cliente y segmento
-- responde a: que clientes realizan mas comentarios y comportamiento segun tipo o ubicacion
create or replace view vw_analisis_por_cliente as
select
    c.client_key,
    c.original_client_id,
    c.name as client_name,
    c.email as client_email,
    c.country as client_country,
    c.client_type,
    count(f.feedback_key) as total_comentarios,
    round(avg(f.rating), 2) as rating_promedio,
    count(case when lower(s.sentiment_name) = 'positivo' then 1 end) as total_positivos,
    count(case when lower(s.sentiment_name) = 'negativo' then 1 end) as total_negativos,
    count(case when lower(s.sentiment_name) = 'neutro' then 1 end) as total_neutros
from dim_client c
left join fact_feedbacks f on c.client_key = f.client_key
left join dim_sentiment s on f.sentiment_key = s.sentiment_key
group by c.client_key, c.original_client_id, c.name, c.email, c.country, c.client_type;


-- Vista de matriz cruzada: canal vs sentimiento
-- responde a: comparativa detallada del tono de las opiniones por cada canal/plataforma
create or replace view vw_matriz_canal_sentimiento as
select
    src.source_type_name,
    src.platform,
    s.sentiment_name,
    count(f.feedback_key) as total_comentarios,
    round(avg(f.rating), 2) as rating_promedio
from fact_feedbacks f
join dim_source src on f.source_key = src.source_key
join dim_sentiment s on f.sentiment_key = s.sentiment_key
group by src.source_type_name, src.platform, s.sentiment_name;

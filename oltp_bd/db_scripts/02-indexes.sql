-------------------------
-- Indices para las fk --
-------------------------

create index idx_products_category_id on products(category_id) tablespace ts_indexes;
create index idx_sources_source_type_id on sources(source_type_id) tablespace ts_indexes;
create index idx_feedbacks_product_id on feedbacks(product_id) tablespace ts_indexes;
create index idx_feedbacks_client_id on feedbacks(client_id) tablespace ts_indexes;
create index idx_feedbacks_source_id on feedbacks(source_id) tablespace ts_indexes;

--------------------------
-- Indices para queries --
--------------------------

-- Para queries por rango de fechas
create index idx_feedbacks_created_at on feedbacks(created_at) tablespace ts_indexes;

-- Para queries por plataforma
create index idx_feedbacks_platform on feedbacks(platform) tablespace ts_indexes;

-- Para queries por rating
create index idx_feedbacks_rating on feedbacks(rating) tablespace ts_indexes;

-- Para queries por sentimiento
create index idx_feedbacks_sentiment on feedbacks(sentiment) tablespace ts_indexes;
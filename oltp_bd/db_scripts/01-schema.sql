-- Creamos los tablespaces (que son basicamente los filegroups de SQL Server)

-- Aquí iran las tablas de categories, products, clients, sources y source_types
create tablespace ts_dimensions location '/mnt/tablespaces/dimensions';
-- Aquí iran la tabla de feedbacks
create tablespace ts_feedbacks location '/mnt/tablespaces/feedbacks';
-- Aquí iran los índices de las tablas de dimensiones y de feedbacks
create tablespace ts_indexes location '/mnt/tablespaces/indexes';

------------
-- tablas --
------------

create table categories
(
    id   serial,
    name varchar(255) not null,

    -- Constraint pa el indice clustered y mandandolo al tablespace de indices
    constraint pk_categories primary key (id) using index tablespace ts_indexes
) tablespace ts_dimensions;

create table products
(
    id          serial,
    name        varchar(255) not null,
    category_id int          not null,

    -- constraint de la pk
    constraint pk_products primary key (id) using index tablespace ts_indexes
) tablespace ts_dimensions;

create table source_types
(
    id   serial,
    name varchar(50) not null, -- Ej: "Web", "Social Media", etc...

    -- constraint de la pk
    constraint pk_source_types primary key (id) using index tablespace ts_indexes
) tablespace ts_dimensions;

create table sources
(
    id             varchar(50),
    source_type_id int not null,
    upload_date    timestamp default now(),

    -- constraint de la pk
    constraint pk_sources primary key (id) using index tablespace ts_indexes
) tablespace ts_dimensions;

create table clients
(
    id    serial,
    name  varchar(255) not null,
    email varchar(255) not null,

    -- constraint de la pk
    constraint pk_clients primary key (id) using index tablespace ts_indexes
) tablespace ts_dimensions;

create table feedbacks
(
    id          serial,
    external_id varchar(50),
    product_id  int,
    client_id   int, -- nullable porq puede ser de una cuenta anonima en redes sociales
    source_id   varchar(50) not null,
    platform    varchar(50) not null,
    comment     text        not null,
    created_at  timestamp default now(),
    rating      int,
    sentiment   varchar(20),
    -- la metadata es por si guardaria info adicional a medida que se integren diferentes fuentes
    metadata    jsonb,

    -- constraint de la pk
    constraint pk_feedbacks primary key (id) using index tablespace ts_indexes
) tablespace ts_feedbacks;

-----------------
-- constraints --
-----------------

--- CATEGORIES ---
alter table categories
    add constraint uq_categories_name unique (name) using index tablespace ts_indexes;

--- PRODUCTS ---
alter table products
    add constraint fk_products_category foreign key (category_id) references categories (id) on delete cascade;
alter table products
    add constraint uq_products_name unique (name) using index tablespace ts_indexes;

--- SOURCE_TYPES ---
alter table source_types
    add constraint uq_source_types_name unique (name) using index tablespace ts_indexes;

--- SOURCES ---
alter table sources
    add constraint fk_sources_source_type foreign key (source_type_id) references source_types (id) on delete restrict;

--- CLIENTS ---
alter table clients
    add constraint uq_clients_email unique (email) using index tablespace ts_indexes;

--- FEEDBACKS ---
alter table feedbacks
    add constraint fk_feedbacks_product foreign key (product_id) references products (id);
alter table feedbacks
    add constraint fk_feedbacks_client foreign key (client_id) references clients (id);
alter table feedbacks
    add constraint fk_feedbacks_source foreign key (source_id) references sources (id);
alter table feedbacks
    add constraint ck_rating_range check (rating >= 1 and rating <= 5);
alter table feedbacks
    add constraint uq_feedbacks_external_id unique (external_id) using index tablespace ts_indexes;

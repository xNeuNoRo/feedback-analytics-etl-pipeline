-- Creamos los tablespaces (que son basicamente los filegroups de SQL Server)

-- Aquí iran las tablas de dimensiones
create tablespace ts_olap_dims location '/mnt/tablespaces/dimensions';
-- Aquí iran las tablas de facts
create tablespace ts_olap_facts location '/mnt/tablespaces/facts';
-- Aquí iran los índices de las tablas de dimensiones y de facts
create tablespace ts_olap_indexes location '/mnt/tablespaces/indexes';

---------------------------
-- tablas de dimensiones --
---------------------------

create table dim_time
(
    time_key         serial,
    full_date        date        not null,
    year             int         not null,
    month            int         not null,

    quarter_num      int         not null,
    quarter_name     varchar(2)  not null,

    day_of_week_num  int         not null,
    day_of_week_name varchar(20) not null,


    -- Constraint para la pk
    constraint pk_dim_time primary key (time_key) using index tablespace ts_olap_indexes
) tablespace ts_olap_dims;

create table dim_client
(
    client_key         serial,
    original_client_id int,
    name               varchar(255) not null,
    email              varchar(255),
    country            varchar(100) default 'Desconocido',
    age_group          varchar(50)  default 'Desconocido',
    client_type        varchar(50)  default 'Regular',

    -- Constraint para la pk
    constraint pk_dim_client primary key (client_key) using index tablespace ts_olap_indexes
) tablespace ts_olap_dims;

create table dim_product
(
    product_key         serial,
    original_product_id int          not null,
    product_name        varchar(255) not null,
    category_name       varchar(255) not null,

    -- Constraint para la pk
    constraint pk_dim_product primary key (product_key) using index tablespace ts_olap_indexes
) tablespace ts_olap_dims;

create table dim_source
(
    source_key         serial,
    original_source_id varchar(50) not null,
    source_type_name   varchar(50) not null,
    platform           varchar(50) not null,

    -- Constraint para la pk
    constraint pk_dim_source primary key (source_key) using index tablespace ts_olap_indexes
) tablespace ts_olap_dims;

create table dim_sentiment
(
    sentiment_key  serial,
    sentiment_name varchar(20) not null,

    -- Constraint para la pk
    constraint pk_dim_sentiment primary key (sentiment_key) using index tablespace ts_olap_indexes
) tablespace ts_olap_dims;

---------------------
-- tabla de hechos --
---------------------

create table fact_feedbacks
(
    feedback_key                  serial,
    time_key                      int  not null,
    client_key                    int  not null,
    product_key                   int  not null,
    source_key                    int  not null,
    sentiment_key                 int  not null,


    -- Metricas y atributos
    rating                        int,
    feedback_count                int default 1,
    comment_text                  text not null,
    original_feedback_external_id varchar(50),

    -- Constraint para la pk
    constraint pk_fact_feedbacks primary key (feedback_key) using index tablespace ts_olap_indexes,

    -- Constraints para las fk
    constraint fk_fact_time foreign key (time_key) references dim_time (time_key),
    constraint fk_fact_client foreign key (client_key) references dim_client (client_key),
    constraint fk_fact_product foreign key (product_key) references dim_product (product_key),
    constraint fk_fact_source foreign key (source_key) references dim_source (source_key),
    constraint fk_fact_sentiment foreign key (sentiment_key) references dim_sentiment (sentiment_key)
) tablespace ts_olap_facts;
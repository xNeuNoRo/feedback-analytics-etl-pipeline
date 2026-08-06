create index idx_fact_time on fact_feedbacks (time_key) tablespace ts_olap_indexes;
create index idx_fact_client on fact_feedbacks (client_key) tablespace ts_olap_indexes;
create index idx_fact_product on fact_feedbacks (product_key) tablespace ts_olap_indexes;
create index idx_fact_source on fact_feedbacks (source_key) tablespace ts_olap_indexes;
create index idx_fact_sentiment on fact_feedbacks (sentiment_key) tablespace ts_olap_indexes;
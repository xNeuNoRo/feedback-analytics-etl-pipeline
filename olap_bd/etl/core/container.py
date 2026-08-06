import os
from dependency_injector import containers, providers

from .config import etl_settings
from .database import OlapDatabaseManager, OltpDatabaseManager

# Extractores
from data.extractors.strategies.api_extractor import ApiExtractor
from data.extractors.strategies.database_extractor import DatabaseExtractor
from data.extractors.strategies.csv_extractor import CsvExtractor

# Transformadores
from data.transformers.helpers.nlp_sentiment_analyzer import NlpSentimentAnalyzer
from data.transformers.strategies.dim_time_transformer import DimTimeTransformer
from data.transformers.strategies.dim_client_transformer import DimClientTransformer
from data.transformers.strategies.dim_product_transformer import DimProductTransformer
from data.transformers.strategies.dim_source_transformer import DimSourceTransformer
from data.transformers.strategies.dim_sentiment_transformer import DimSentimentTransformer
from data.transformers.strategies.fact_feedbacks_transformer import FactFeedbacksTransformer

# DAOs y Servicio de Carga
from load.daos.dim_time_dao import DimTimeDao
from load.daos.dim_client_dao import DimClientDao
from load.daos.dim_product_dao import DimProductDao
from load.daos.dim_source_dao import DimSourceDao
from load.daos.dim_sentiment_dao import DimSentimentDao
from load.daos.fact_feedbacks_dao import FactFeedbacksDao
from load.loader_service import LoaderService

# App
from .application import OlapEtlApplication


class EtlContainer(containers.DeclarativeContainer):
    """
    Contenedor de Inyección de Dependencias para el Pipeline ETL Analítico (OLAP).
    Configura extractores genéricos e instancias mapeadas para cada fuente CSV.
    """
    wiring_config = containers.WiringConfiguration(
        modules=["main"]
    )

    # Configuramos las settings de la aplicación y de la base de datos OLTP como un Objeto
    config = providers.Object(etl_settings)
    oltp_config = providers.Object(etl_settings)

    # Configuramos el manager de la OLTP Y OLAP como Singletons para que se compartan en toda la aplicación
    oltp_db_manager = providers.Singleton(
        OltpDatabaseManager,
        config=oltp_config
    )

    olap_db_manager = providers.Singleton(
        OlapDatabaseManager,
        config=config
    )

    # Configuramos los extractores específicos para cada fuente de datos (API, BD OLTP y CSVs)
    api_extractor = providers.Factory(
        ApiExtractor,
        api_base_url=config.provided.API_BASE_URL,
        api_key=config.provided.API_KEY
    )

    database_extractor = providers.Factory(
        DatabaseExtractor,
        oltp_db_manager=oltp_db_manager
    )

    # Configuramos los extractores de CSV para cada fuente de datos, mapeando las columnas y estableciendo valores por defecto

    # Extractor CSV de Encuestas
    survey_csv_extractor = providers.Factory(
        CsvExtractor,
        filepath=os.path.join(etl_settings.CSV_FOLDER_PATH,
                              "survey_feedback.csv"),
        column_mapping={
            "IdOpinion": "external_id",
            "IdCliente": "client_id",
            "IdProducto": "product_id",
            "Fecha": "created_at",
            "Comentario": "comment",
            "Clasificación": "raw_sentiment",
            "PuntajeSatisfacción": "rating",
            "Fuente": "platform"
        },
        default_values={
            "source_id": "SRC-SURVEY-CSV",
            "source_type_name": "Encuestas",
            "platform": "EncuestaInterna"
        }
    )

    # Extractor CSV de Redes Sociales
    social_csv_extractor = providers.Factory(
        CsvExtractor,
        filepath=os.path.join(etl_settings.CSV_FOLDER_PATH,
                              "social_feedback.csv"),
        column_mapping={
            "IdComment": "external_id",
            "IdCliente": "client_id",
            "IdProducto": "product_id",
            "Fecha": "created_at",
            "Comentario": "comment",
            "Fuente": "platform"
        },
        default_values={
            "source_id": "SRC-SOCIAL-CSV",
            "source_type_name": "RedesSociales",
            "platform": "SocialCSV"
        }
    )

    # Extractor CSV de Feedbacks Web
    web_csv_extractor = providers.Factory(
        CsvExtractor,
        filepath=os.path.join(
            etl_settings.CSV_FOLDER_PATH, "web_feedback.csv"),
        column_mapping={
            "IdReview": "external_id",
            "IdCliente": "client_id",
            "IdProducto": "product_id",
            "Fecha": "created_at",
            "Comentario": "comment",
            "Rating": "rating"
        },
        default_values={
            "source_id": "SRC-WEB-CSV",
            "source_type_name": "WebReviews",
            "platform": "WebCSV"
        }
    )

    # Configuramos la lista de Extractores para el Pipeline ETL
    extractors_list = providers.List(
        api_extractor,
        database_extractor,
        survey_csv_extractor,
        social_csv_extractor,
        web_csv_extractor
    )

    # Configuramos el analizador de sentimientos NLP y los transformadores de dimensiones y hechos para el Pipeline ETL
    nlp_analyzer = providers.Singleton(NlpSentimentAnalyzer)

    time_transformer = providers.Factory(DimTimeTransformer)
    client_transformer = providers.Factory(DimClientTransformer)
    product_transformer = providers.Factory(DimProductTransformer)
    source_transformer = providers.Factory(DimSourceTransformer)
    sentiment_transformer = providers.Factory(
        DimSentimentTransformer,
        nlp_analyzer=nlp_analyzer
    )

    transformer = providers.Factory(
        FactFeedbacksTransformer,
        time_tf=time_transformer,
        client_tf=client_transformer,
        product_tf=product_transformer,
        source_tf=source_transformer,
        sentiment_tf=sentiment_transformer
    )

    # Configuramos los DAOs y el Servicio de Carga para el Pipeline ETL
    dim_time_dao = providers.Factory(DimTimeDao)
    dim_client_dao = providers.Factory(DimClientDao)
    dim_product_dao = providers.Factory(DimProductDao)
    dim_source_dao = providers.Factory(DimSourceDao)
    dim_sentiment_dao = providers.Factory(DimSentimentDao)
    fact_feedbacks_dao = providers.Factory(FactFeedbacksDao)

    loader = providers.Factory(
        LoaderService,
        olap_db_manager=olap_db_manager,
        time_dao=dim_time_dao,
        client_dao=dim_client_dao,
        product_dao=dim_product_dao,
        source_dao=dim_source_dao,
        sentiment_dao=dim_sentiment_dao,
        fact_dao=fact_feedbacks_dao
    )

    # Finalmente ya con todo armado, configuramos la app ETL que orquesta todo el pipeline de extracción, transformación y carga
    etl_application = providers.Factory(
        OlapEtlApplication,
        extractors=extractors_list,
        transformer=transformer,
        loader=loader
    )

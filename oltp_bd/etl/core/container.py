from dependency_injector import containers, providers

# Helpers y DAOs
from data.extractors.helpers.csv_extractor import CsvExtractor
from data.transformers.helpers.string_helper import StringHelper
from load.daos.product_dao import ProductDAO
from load.daos.client_dao import ClientDAO
from load.daos.source_dao import SourceDAO
from load.daos.feedback_dao import FeedbackDAO


# Extractores
from data.extractors.strategies.product_csv_extractor import ProductCsvExtractor
from data.extractors.strategies.client_csv_extractor import ClientCsvExtractor
from data.extractors.strategies.source_csv_extractor import SourceCsvExtractor
from data.extractors.strategies.feedback_csv_extractor import FeedbackCsvExtractor

# Transformadores
from data.transformers.strategies.product_transformer import ProductTransformer
from data.transformers.strategies.client_transformer import ClientTransformer
from data.transformers.strategies.source_transformer import SourceTransformer
from data.transformers.strategies.feedback_transformer import FeedbackTransformer

# El Orquestador
from load.loader_service import LoaderService


class Container(containers.DeclarativeContainer):
    """
    Contenedor IoC (Inversión de Control).
    Aquí registramos y conectamos todas las piezas de nuestro ETL.
    """

    # Registramos los Helpers (Singleton)
    csv_helper = providers.Singleton(CsvExtractor)
    str_helper = providers.Singleton(StringHelper)

    # Registramos los DAOs (Singleton)
    product_dao = providers.Singleton(ProductDAO)
    client_dao = providers.Singleton(ClientDAO)
    source_dao = providers.Singleton(SourceDAO)
    feedback_dao = providers.Singleton(FeedbackDAO)

    # Registramos los Extractores (Inyectandoles el helper de CSV)
    product_ext = providers.Singleton(ProductCsvExtractor, helper=csv_helper)
    client_ext = providers.Singleton(ClientCsvExtractor, helper=csv_helper)
    source_ext = providers.Singleton(SourceCsvExtractor, helper=csv_helper)
    feedback_ext = providers.Singleton(FeedbackCsvExtractor, helper=csv_helper)

    # Registramos los Transformers
    product_trans = providers.Singleton(ProductTransformer)
    client_trans = providers.Singleton(ClientTransformer)
    source_trans = providers.Singleton(SourceTransformer)

    # Configuramos el mapeo de columnas para nuestro Transformer de Web Reviews
    web_mapping = {
        'external_id': 'IdReview', 'product_id': 'IdProducto', 'client_id': 'IdCliente',
        'created_at': 'Fecha', 'comment': 'Comentario', 'rating': 'Rating'
    }
    web_headers = ['IdReview', 'IdCliente',
                   'IdProducto', 'Fecha', 'Comentario', 'Rating']

    # Configuramos el mapeo de columnas para nuestro Transformer de Social Reviews
    social_mapping = {
        'external_id': 'IdComment', 'product_id': 'IdProducto', 'client_id': 'IdCliente',
        'created_at': 'Fecha', 'comment': 'Comentario', 'platform': 'Fuente'
    }
    social_headers = ['IdComment', 'IdCliente', 'IdProducto', 'Fuente', 'Fecha',
                      'Comentario']

    # Configuramos el mapeo de columnas para nuestro Transformer de Survey Reviews
    survey_mapping = {
        'external_id': 'IdOpinion', 'product_id': 'IdProducto', 'client_id': 'IdCliente',
        'created_at': 'Fecha', 'comment': 'Comentario', 'rating': 'PuntajeSatisfacción', 'platform': 'Fuente'
    }
    survey_headers = ['IdOpinion', 'IdCliente', 'IdProducto', 'Fecha', 'Comentario',
                      'Clasificación', 'PuntajeSatisfacción', 'Fuente']

    # Creamos el Transformer de Web Reviews inyectandole el StringHelper y el mapeo de columnas
    web_feedback_trans = providers.Singleton(
        FeedbackTransformer,
        helper=str_helper,
        csv_headers=web_headers,
        column_mapping=web_mapping,
        # El ID de la fuente para todas las reviews de la web (F001 es de tipo Web)
        source_id='F001',
        platform='Web'  # La plataforma de origen para todas las reviews de la web
    )

    # Creamos el Transformer de Social Reviews inyectandole el StringHelper y el mapeo de columnas
    social_feedback_trans = providers.Singleton(
        FeedbackTransformer,
        helper=str_helper,
        csv_headers=social_headers,
        column_mapping=social_mapping,
        source_id='F005',  # Fallback por si la columna Fuente viene vacía en el CSV
        platform='Social'  # La plataforma de origen para todas las reviews de redes sociales
    )

    # Creamos el Transformer de Survey Reviews inyectandole el StringHelper y el mapeo de columnas
    survey_feedback_trans = providers.Singleton(
        FeedbackTransformer,
        helper=str_helper,
        csv_headers=survey_headers,
        column_mapping=survey_mapping,
        source_id='F002',  # Fallback por si la columna Fuente viene vacía en el CSV
        platform='Survey'  # La plataforma de origen para todas las reviews de encuestas
    )

    # Armamos el Orquestador inyectándole todas sus piezas
    loader_service = providers.Singleton(
        LoaderService,

        # Inyectamos el ETL de productos
        product_extractor=product_ext,
        product_transformer=product_trans,
        product_load=product_dao,

        # Inyectamos el ETL de clientes
        client_extractor=client_ext,
        client_transformer=client_trans,
        client_load=client_dao,

        # Inyectamos el ETL de fuentes
        source_extractor=source_ext,
        source_transformer=source_trans,
        source_load=source_dao,

        # Inyectamos el ETL de feedback
        feedback_extractor=feedback_ext,
        feedback_load=feedback_dao,

        # Inyectamos los transformers de feedback según la fuente
        web_transformer=web_feedback_trans,
        social_transformer=social_feedback_trans,
        survey_transformer=survey_feedback_trans
    )

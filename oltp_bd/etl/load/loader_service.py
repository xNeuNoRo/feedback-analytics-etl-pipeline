from data.extractors.interfaces.iextractor import IExtractor
from data.transformers.interfaces.itransformer import ITransformer


# Importamos los DAOS
from load.daos.product_dao import ProductDAO
from load.daos.client_dao import ClientDAO
from load.daos.source_dao import SourceDAO
from load.daos.feedback_dao import FeedbackDAO


class LoaderService:
    """
    Clase orquestadora de la carga de datos. Esta clase se encarga de coordinar la extracción, transformación y carga de datos en la base de datos.
    """

    def __init__(self,

                 # Inyectamos el ETL de productos
                 product_extractor: IExtractor,
                 product_transformer: ITransformer,
                 product_load: ProductDAO,

                 # Inyectamos el ETL de clientes
                 client_extractor: IExtractor,
                 client_transformer: ITransformer,
                 client_load: ClientDAO,

                 # Inyectamos el ETL de fuentes
                 source_extractor: IExtractor,
                 source_transformer: ITransformer,
                 source_load: SourceDAO,

                 # Inyectamos el extractor y loader de feedback
                 feedback_extractor: IExtractor,
                 feedback_load: FeedbackDAO,

                 # Los transformers de feedback pueden variar según la fuente, por lo que los inyectamos como interfaces
                 web_transformer: ITransformer,
                 social_transformer: ITransformer,
                 survey_transformer: ITransformer
                 ):
        # Inicializamos el ETL de productos
        self._prod_ext = product_extractor
        self._prod_trans = product_transformer
        self._prod_load = product_load

        # Inicializamos el ETL de clientes
        self._cli_ext = client_extractor
        self._cli_trans = client_transformer
        self._cli_load = client_load

        # Inicializamos el ETL de fuentes
        self._src_ext = source_extractor
        self._src_trans = source_transformer
        self._src_load = source_load

        # Inicializamos el ETL de feedback
        self._fb_ext = feedback_extractor
        self._fb_load = feedback_load

        # Inicializamos los transformers de feedback según la fuente
        self._web_trans = web_transformer
        self._social_trans = social_transformer
        self._survey_trans = survey_transformer

    def process_products(self, filepath: str) -> None:
        """Pipeline completo para los Productos."""
        print("\n--- Iniciando ETL de productos ---")
        raw_data = self._prod_ext.extract(filepath)
        cleaned_data = self._prod_trans.transform(raw_data)
        self._prod_load.upsert_batch(cleaned_data)
        print("--- ETL de productos finalizado ---\n")

    def process_clients(self, filepath: str) -> None:
        """Pipeline completo para los Clientes."""
        print("\n--- Iniciando ETL de clientes ---")
        raw_data = self._cli_ext.extract(filepath)
        cleaned_data = self._cli_trans.transform(raw_data)
        self._cli_load.upsert_batch(cleaned_data)
        print("--- ETL de clientes finalizado ---\n")

    def process_sources(self, filepath: str) -> None:
        """Pipeline completo para las Fuentes."""
        print("\n--- Iniciando ETL de fuentes ---")
        raw_data = self._src_ext.extract(filepath)
        cleaned_data = self._src_trans.transform(raw_data)
        self._src_load.upsert_batch(cleaned_data)
        print("--- ETL de fuentes finalizado ---\n")

    def process_web_feedbacks(self, filepath: str) -> None:
        """Pipeline completo para los Feedbacks de la Web."""
        print("\n--- Iniciando ETL de feedbacks de la Web ---")
        raw_data = self._fb_ext.extract(filepath)
        # Usamos el transformer específico para la Web
        cleaned_data = self._web_trans.transform(raw_data)
        self._fb_load.insert_batch(cleaned_data)
        print("--- ETL de feedbacks de la Web finalizado ---\n")

    def process_social_feedbacks(self, filepath: str) -> None:
        """Pipeline completo para los Feedbacks de Redes Sociales."""
        print("\n--- Iniciando ETL de feedbacks de Redes Sociales ---")
        raw_data = self._fb_ext.extract(filepath)
        # Usamos el transformer específico para Redes Sociales
        cleaned_data = self._social_trans.transform(raw_data)
        self._fb_load.insert_batch(cleaned_data)
        print("--- ETL de feedbacks de Redes Sociales finalizado ---\n")

    def process_survey_feedbacks(self, filepath: str) -> None:
        """Pipeline completo para los Feedbacks de Encuestas."""
        print("\n--- Iniciando ETL de feedbacks de Encuestas ---")
        raw_data = self._fb_ext.extract(filepath)
        # Usamos el transformer específico para Encuestas
        cleaned_data = self._survey_trans.transform(raw_data)
        self._fb_load.insert_batch(cleaned_data)
        print("--- ETL de feedbacks de Encuestas finalizado ---\n")

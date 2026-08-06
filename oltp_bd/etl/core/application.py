import sys
from core.container import Container


class EtlApplication:
    """
    Clase principal que encapsula toda la logica de ejecución del ETL.
    De esta forma, el main.py se mantiene limpio y no necesita ser modificado
    si agregamos nuevos pasos al pipeline en el futuro.
    """

    def __init__(self):
        # Configuramos las rutas de los archivos
        self.filepaths = {
            'products': "data/input/products.csv",
            'clients': "data/input/clients.csv",
            'sources': "data/input/sources.csv",
            'web_feedback': "data/input/web_feedback.csv",
            'social_feedback': "data/input/social_feedback.csv",
            'survey_feedback': "data/input/survey_feedback.csv"
        }

        # Inicializamos el contenedor de dependencias
        self.container = Container()

    def run(self) -> None:
        print("Iniciando el proceso de ETL de BigData Project (Electiva 1 con Francis Ramirez 2026-C2)\n")

        try:
            # Obtenemos el orquestador ya ensamblado desde el contenedor
            etl = self.container.loader_service()

            # Ejecutamos el pipeline de ETL en orden
            etl.process_products(self.filepaths['products']) # Products inserta categorias tambien
            etl.process_clients(self.filepaths['clients'])
            etl.process_sources(self.filepaths['sources']) # Sources inserta sourceTypes tambien
            etl.process_web_feedbacks(self.filepaths['web_feedback'])
            etl.process_social_feedbacks(self.filepaths['social_feedback'])
            etl.process_survey_feedbacks(self.filepaths['survey_feedback'])

            print("Se ha completado el proceso de ETL exitosamente.\n")

        except Exception as e:
            print(
                f"\n[ERROR CRÍTICO] El proceso ETL falló durante la ejecución: {str(e)}")
            sys.exit(1)

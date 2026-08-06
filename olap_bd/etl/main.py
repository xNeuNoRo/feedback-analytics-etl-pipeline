from core.application import OlapEtlApplication
from core.container import EtlContainer
from dependency_injector.wiring import Provide, inject
import sys
import logging
from pathlib import Path

# Agregamos la carpeta del etl al sys.path para permitir ejecuciones directas desde esta carpeta
etl_path = str(Path(__file__).resolve().parent)
if etl_path not in sys.path:
    sys.path.insert(0, etl_path)

parent_root = str(Path(__file__).resolve().parents[3])
if parent_root not in sys.path:
    sys.path.insert(0, parent_root)


# Configuramos el registro de eventos (logging)
logging.basicConfig(
    level=logging.INFO,  # Nivel de log para el pipeline ETL
    # Formato de log con timestamp, nivel y nombre del logger
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"  # Formato de fecha y hora en el log
)
# Obtenemos el logger que nos servira para todo el pipeline ETL.
logger = logging.getLogger("main_etl")


# EP (EntryPoint) del pipeline ETL Analítico (OLAP)
@inject
def main(
    app: OlapEtlApplication = Provide[EtlContainer.etl_application]
) -> None:
    """Entry Point principal para la ejecución del pipeline ETL."""

    # Iniciamos el pipeline ETL y capturamos cualquier excepción para loguearla y salir con error
    try:
        results = app.run_pipeline()
        logger.info("Resultado final del pipeline: %s", results)
    except Exception as e:
        logger.error(
            "El pipeline ETL falló con un error inesperado: %s", str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Creamos el contenedor de dependencias para el pipeline ETL
    container = EtlContainer()
    # Configuramos el contenedor para que pueda inyectar dependencias en este módulo
    container.wire(modules=[__name__])
    # Ejecutamos el Entry Point principal del pipeline ETL
    main()

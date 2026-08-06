import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager

# Agregamos el root del proyecto al sys.path para permitir ejecuciones directas desde esta carpeta
root_path = str(Path(__file__).resolve().parents[3])
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.container import Container
from routers.feedback_router import router as feedback_router

# Configuración del sistema de logs estructurado
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("oltp_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejador del ciclo de vida de la aplicación.
    Se encarga de inicializar y cerrar limpiamente el pool de conexiones al arrancar y apagar el servidor.
    """
    logger.info("Iniciando el servidor de la API REST de Feedbacks OLTP...")
    # Inicializar el contenedor de Inyección de Dependencias
    container = Container()
    app.state.container = container

    # Inicializar el pool de conexiones a la base de datos
    db_manager = container.db_manager()
    db_manager.initialize_pool()

    yield

    logger.info("Apagando el servidor de la API REST de Feedbacks OLTP...")
    # Cerrar el pool de conexiones de forma segura
    db_manager.close_pool()


# Crear la instancia principal de FastAPI
app = FastAPI(
    title="API REST de Feedbacks OLTP",
    description=(
        "API REST para consultar y exponer los registros de comentarios de clientes desde la base de datos PostgreSQL OLTP "
        "para ser consumidos por el proceso ETL e insertados en la base de datos analítica OLAP."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar middleware de CORS (Permite peticiones desde cualquier origen)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar las rutas en la aplicación
app.include_router(feedback_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=True
    )

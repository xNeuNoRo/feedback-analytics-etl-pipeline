from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from dependency_injector.wiring import Provide, inject
from sqlalchemy import text

from core.container import Container
from core.database import DatabaseManager
from core.security import verify_api_key
from domain.models.feedback_dto import FeedbackEnrichedDTO
from services.feedback_service import FeedbackService

# Creamos el Router de la API para los endpoints relacionados con los feedbacks de la BD OLTP
router = APIRouter(prefix="/api/v1/feedbacks",
                   tags=["Operaciones de Feedback OLTP"])


@router.get(
    "/social-media",
    response_model=List[FeedbackEnrichedDTO],
    status_code=status.HTTP_200_OK,
    summary="Obtener feedbacks de Redes Sociales",
    description="Devuelve la lista de comentarios que sea de origen Redes Sociales (ej. Instagram, Twitter) con paginación.",
    dependencies=[Depends(verify_api_key)]
)
@inject
def get_social_media_feedbacks(
    skip: int = Query(
        0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(1000, ge=1, le=10000,
                       description="Límite máximo de registros a devolver"),
    service: FeedbackService = Depends(Provide[Container.feedback_service])
) -> List[FeedbackEnrichedDTO]:
    try:
        return service.get_social_media_feedbacks(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los feedbacks de redes sociales: {str(e)}"
        )


@router.get(
    "/web-reviews",
    response_model=List[FeedbackEnrichedDTO],
    status_code=status.HTTP_200_OK,
    summary="Obtener reseñas de la Web",
    description="Devuelve la lista de comentarios publicados directamente en el sitio web con paginación.",
    dependencies=[Depends(verify_api_key)]
)
@inject
def get_web_reviews(
    skip: int = Query(
        0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(1000, ge=1, le=10000,
                       description="Límite máximo de registros a devolver"),
    service: FeedbackService = Depends(Provide[Container.feedback_service])
) -> List[FeedbackEnrichedDTO]:
    try:
        return service.get_web_reviews(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las reseñas web: {str(e)}"
        )


@router.get(
    "/platform/{platform_name}",
    response_model=List[FeedbackEnrichedDTO],
    status_code=status.HTTP_200_OK,
    summary="Obtener feedbacks por plataforma",
    description="Devuelve la lista de comentarios filtrados por plataforma específica (ej. 'Instagram', 'Twitter') con paginación.",
    dependencies=[Depends(verify_api_key)]
)
@inject
def get_feedbacks_by_platform(
    platform_name: str,
    skip: int = Query(
        0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(1000, ge=1, le=10000,
                       description="Límite máximo de registros a devolver"),
    service: FeedbackService = Depends(Provide[Container.feedback_service])
) -> List[FeedbackEnrichedDTO]:
    try:
        return service.get_feedbacks_by_platform(platform_name, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los feedbacks para la plataforma '{platform_name}': {str(e)}"
        )


@router.get(
    "/all",
    response_model=List[FeedbackEnrichedDTO],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los feedbacks",
    description="Devuelve absolutamente todos los comentarios de la base de datos OLTP con paginación.",
    dependencies=[Depends(verify_api_key)]
)
@inject
def get_all_feedbacks(
    skip: int = Query(
        0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(1000, ge=1, le=10000,
                       description="Límite máximo de registros a devolver"),
    service: FeedbackService = Depends(Provide[Container.feedback_service])
) -> List[FeedbackEnrichedDTO]:
    try:
        return service.get_all_feedbacks(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener todos los feedbacks: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Verificar estado de la API y la Base de Datos",
    description="Endpoint de diagnóstico para revisar si la API y la conexión a la BD OLTP están funcionando correctamente."
)
@inject
def healthcheck(
    db_manager: DatabaseManager = Depends(Provide[Container.db_manager])
) -> Dict[str, Any]:
    try:
        with db_manager.get_session() as session:
            result = session.execute(text("SELECT 1")).scalar()
            db_status = "saludable" if result == 1 else "con problemas"
        return {
            "status": "online",
            "database": db_status,
            "port": 5433
        }
    except Exception as e:
        return {
            "status": "degradado",
            "database": "no disponible",
            "error": str(e)
        }

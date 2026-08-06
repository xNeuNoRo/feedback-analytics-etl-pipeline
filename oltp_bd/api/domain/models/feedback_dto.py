from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ClientDTO(BaseModel):
    """Objeto para transportar la información del cliente."""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: Optional[int] = Field(
        default=None, description="ID original del cliente en OLTP (None si es anónimo)")
    name: str = Field(default="Cliente Anónimo",
                      description="Nombre completo del cliente")
    email: Optional[str] = Field(
        default=None, description="Correo electrónico del cliente")
    country: str = Field(default="Desconocido",
                         description="País extraído de la metadata")
    age_group: str = Field(default="Desconocido",
                           description="Rango de edad extraído de la metadata")
    client_type: str = Field(
        default="Regular", description="Tipo o categoría del cliente")


class ProductDTO(BaseModel):
    """Objeto para transportar la información del producto."""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: int = Field(..., description="ID original del producto en OLTP")
    name: str = Field(..., description="Nombre del producto")
    category_name: str = Field(...,
                               description="Nombre de la categoría del producto")


class SourceDTO(BaseModel):
    """Objeto para transportar la información del origen del comentario y su plataforma."""
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: str = Field(...,
                    description="ID original de la fuente en OLTP (ej. F001, F002)")
    source_type_name: str = Field(
        ..., description="Tipo de fuente (ej. Encuestas, Web, Redes Sociales)")
    platform: str = Field(...,
                          description="Plataforma de origen (ej. Instagram, Twitter, Web)")


class FeedbackEnrichedDTO(BaseModel):
    """
    Objeto DTO completo y enriquecido con todo del Feedback.
    """
    model_config = ConfigDict(from_attributes=True, frozen=True)

    external_id: Optional[str] = Field(
        default=None, description="ID de referencia externa")
    comment: str = Field(..., description="Texto del comentario o reseña")
    rating: Optional[int] = Field(
        default=None, ge=1, le=5, description="Puntuación o calificación de 1 a 5")
    created_at: datetime = Field(...,
                                 description="Fecha y hora en que se creó el comentario")
    sentiment: Optional[str] = Field(
        default=None, description="Sentimiento original si existía en OLTP")

    client: ClientDTO = Field(..., description="Datos del cliente asociado")
    product: Optional[ProductDTO] = Field(
        default=None, description="Datos del producto asociado")
    source: SourceDTO = Field(..., description="Datos de la fuente de origen")

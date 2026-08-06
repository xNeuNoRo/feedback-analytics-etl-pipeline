import logging
from typing import List, Dict, Any
import httpx
from data.extractors.interfaces.i_extractor import IExtractor

logger = logging.getLogger(__name__)


class ApiExtractor(IExtractor):
    """
    Strategy de Extracción desde la API REST de Redes Sociales.
    (Api sencilla que imite para simular la extraccion de datos segun el ejercicio)
    """

    def __init__(self, api_base_url: str, api_key: str):
        self._api_base_url = api_base_url.rstrip("/")
        self._api_key = api_key

    def extract(self) -> List[Dict[str, Any]]:
        """Consume el endpoint /api/v1/feedbacks/social-media y devuelve la lista de diccionarios."""
        endpoint = f"{self._api_base_url}/api/v1/feedbacks/social-media"
        headers = {"X-API-Key": self._api_key}

        logger.info("Iniciando extraccion desde API REST: %s", endpoint)
        results: List[Dict[str, Any]] = []

        try:
            # iniciamos el cliente httpx con with para liberar recursos autom.
            with httpx.Client(timeout=10.0) as client:
                response = client.get(endpoint, headers=headers)
                response.raise_for_status()
                data = response.json()

            for item in data:
                client_info = item.get("client") or {}
                product_info = item.get("product") or {}
                source_info = item.get("source") or {}

                record = {
                    "external_id": item.get("external_id"),
                    "comment": item.get("comment", ""),
                    "rating": item.get("rating"),
                    "created_at": item.get("created_at"),
                    "raw_sentiment": item.get("sentiment"),

                    # Cliente
                    "client_id": client_info.get("id"),
                    "client_name": client_info.get("name", "Cliente Anónimo"),
                    "client_email": client_info.get("email"),
                    "client_country": client_info.get("country", "Desconocido"),
                    "client_age_group": str(client_info.get("age_group", "Desconocido")),
                    "client_type": str(client_info.get("client_type", "Regular")),

                    # Producto
                    "product_id": product_info.get("id"),
                    "product_name": product_info.get("name", "Producto General"),
                    "category_name": product_info.get("category_name", "General"),

                    # Fuente
                    "source_id": source_info.get("id", "SRC-API"),
                    "source_type_name": source_info.get("source_type_name", "Redes Sociales"),
                    "platform": source_info.get("platform", "API")
                }
                results.append(record)

            logger.info(
                "Extraccion desde la API completada con exito. Registros obtenidos: %d", len(results))
            return results

        except Exception as e:
            logger.error(
                "Error durante la extraccion de datos desde la API: %s", str(e))
            return []

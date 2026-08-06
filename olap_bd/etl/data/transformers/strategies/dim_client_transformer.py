from typing import Dict, Any


class DimClientTransformer:
    """Transformador para la dimensión dim_client."""

    def transform_client(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza los datos de cliente para la dimensión dim_client."""

        return {
            "original_client_id": raw_record.get("client_id"),
            "name": raw_record.get("client_name") or "Cliente Anónimo",
            "email": raw_record.get("client_email"),
            "country": raw_record.get("client_country") or "Desconocido",
            "age_group": str(raw_record.get("client_age_group") or "Desconocido"),
            "client_type": str(raw_record.get("client_type") or "Regular")
        }

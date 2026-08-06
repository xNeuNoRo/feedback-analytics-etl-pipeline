from typing import Dict, Any


class DimSourceTransformer:
    """Transformador para la dimensión dim_source."""

    def transform_source(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza los datos de la fuente para la dimensión dim_source."""
        return {
            "original_source_id": str(raw_record.get("source_id") or "SRC-UNKNOWN"),
            "source_type_name": str(raw_record.get("source_type_name") or "General"),
            "platform": str(raw_record.get("platform") or "General")
        }

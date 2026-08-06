from typing import Dict, Any


class DimProductTransformer:
    """Transformador para la dimensión dim_product."""

    def transform_product(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza los datos de producto y categoría para la dimensión dim_product."""
        return {
            "original_product_id": raw_record.get("product_id") or 0,
            "product_name": raw_record.get("product_name") or "Producto General",
            "category_name": raw_record.get("category_name") or "General"
        }

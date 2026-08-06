from datetime import datetime, date
from typing import Dict, Any

# Diccionario sencillo para mapear los numeros de dias a sus nombres
DAYS = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}


class DimTimeTransformer:
    """Transformador para la dimensión dim_time."""

    def transform_date(self, raw_date_val: Any) -> Dict[str, Any]:
        """Normaliza los datos de fecha para la dimensión dim_time."""
        if isinstance(raw_date_val, datetime):
            dt = raw_date_val
        elif isinstance(raw_date_val, date):
            dt = datetime.combine(raw_date_val, datetime.min.time())
        elif isinstance(raw_date_val, str) and raw_date_val.strip():
            try:
                dt = datetime.fromisoformat(raw_date_val)
            except ValueError:
                dt = datetime.utcnow()
        else:
            dt = datetime.utcnow()

        month = dt.month
        quarter_num = (month - 1) // 3 + 1
        day_of_week_num = dt.weekday() + 1

        return {
            "full_date": dt.date(),
            "year": dt.year,
            "month": month,
            "quarter_num": quarter_num,
            "quarter_name": f"Q{quarter_num}",
            "day_of_week_num": day_of_week_num,
            "day_of_week_name": DAYS.get(dt.weekday(), "Desconocido")
        }

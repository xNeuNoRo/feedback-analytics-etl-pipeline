import re
from typing import Any
import pandas as pd


def auto_clean_value(val: Any) -> Any:
    """Limpia cualquier valor de celda y lo convierte a un tipo de dato más adecuado (int, float, str o None)."""

    # Comprobamos si el valor es None o NaN
    if val is None or pd.isna(val):
        return None

    # Comprobamos si el valor es un número (int o float) y lo convertimos a int si es posible
    if isinstance(val, (int, float)):
        if isinstance(val, int) or (isinstance(val, float) and val.is_integer()):
            return int(val)
        return float(val)

    # Comprobamos si el valor es un string y lo limpiamos
    val_str = str(val).strip()
    if not val_str:
        return None
    if val_str.isdigit() or (val_str.startswith("-") and val_str[1:].isdigit()):
        return int(val_str)
    return val_str


def clean_str(val: Any, default: str = "") -> str:
    """Limpia strings nulos o vacios de forma segura."""
    cleaned = auto_clean_value(val)
    if cleaned is None:
        return default
    return str(cleaned)


def clean_int(val: Any) -> Any:
    """Convierte un valor numerico o devuelve None si no es valido."""
    if val is None or pd.isna(val):
        return None
    val_str = str(val).strip()
    if not val_str:
        return None
    nums = re.sub(r'\D', '', val_str)
    return int(nums) if nums else None

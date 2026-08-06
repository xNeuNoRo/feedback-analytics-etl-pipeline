import re
import pandas as pd
from typing import Optional, Any


class StringHelper:
    """
    Helper generico con utilidades para transformacion de strings
    """

    @staticmethod
    def extract_id(raw_text: Any) -> Optional[int]:
        """
        Convierte un string id como "P016" a un entero 16. Si no puede convertirlo, devuelve None.
        """

        # Si el texto es nulo o vacío, devolvemos None
        if pd.isna(raw_text) or not str(raw_text).strip():
            return None

        # Usamos una expresión regular para extraer solo los dígitos del string
        nums = re.sub(r'\D', '', str(raw_text))

        # Devolvemos el número como entero, o None si no hay dígitos
        return int(nums) if nums else None

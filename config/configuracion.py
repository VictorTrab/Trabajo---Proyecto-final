"""
Sistema de configuración del juego
"""

import json
import os
from config.constantes import CONFIG_FILE, DEFAULT_INDICATOR


class GameConfig:
    """Clase para manejar la configuración del juego"""

    def __init__(self):
        self.indicator_type = DEFAULT_INDICATOR
        self.load()

    def load(self):
        """Carga la configuración desde archivo"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.indicator_type = data.get("indicator_type", DEFAULT_INDICATOR)
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
                self.indicator_type = DEFAULT_INDICATOR

    def save(self):
        """Guarda la configuración en archivo"""
        try:
            data = {"indicator_type": self.indicator_type}
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")

    def set_indicator(self, indicator_type):
        """Cambia el tipo de indicador visual"""
        self.indicator_type = indicator_type
        self.save()

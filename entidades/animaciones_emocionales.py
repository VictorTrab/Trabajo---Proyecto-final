"""
Animaciones Contextuales - Fase 5 (Optimizado)
Animaciones esenciales por emoción
"""

import math
from typing import Tuple


class AnimadorEmocional:
    """Gestiona animaciones por emoción"""

    def __init__(self):
        self.tiempo = 0
        self.animacion_activa = None
        self.tiempo_animacion = 0

    def iniciar_animacion(self, nombre: str):
        """Inicia animación especial"""
        self.animacion_activa = nombre
        self.tiempo_animacion = 0

    def actualizar(self, dt: float):
        """Actualiza animación"""
        self.tiempo_animacion += dt
        if self.tiempo_animacion >= 1.0:  # Duración fija 1s
            self.animacion_activa = None
            self.tiempo_animacion = 0

    def obtener_transformacion_completa(self, emocion: str) -> dict:
        """Obtiene datos de transformación"""
        offset_x, offset_y = 0, 0
        escala = 1.0

        # Animación celebración
        if self.animacion_activa == "celebracion_exito":
            prog = self.tiempo_animacion
            offset_y = -abs(4 * prog * (1 - prog)) * 30  # Salto
            escala = 1.0 + math.sin(prog * 10) * 0.1

        # Animación continua por emoción
        elif emocion == "feliz":
            offset_y = math.sin(self.tiempo_animacion * 5) * 8
        elif emocion == "triste":
            offset_y = math.sin(self.tiempo_animacion * 2) * 3

        return {
            "offset_x": offset_x,
            "offset_y": offset_y,
            "escala": escala,
            "rotacion": 0,
            "alpha": 1.0,
        }

    def detener(self):
        self.animacion_activa = None


class AnimacionContinua:
    """Animaciones continuas simples"""

    def __init__(self):
        self.tiempo = 0

    def actualizar(self, dt: float):
        self.tiempo += dt

    def respiracion_normal(self) -> float:
        """Respiración suave"""
        return 1.0 + math.sin(self.tiempo * 2) * 0.03

    def flotacion_feliz(self) -> float:
        """Flotación feliz"""
        return math.sin(self.tiempo * 1.5) * 5

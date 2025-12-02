"""
Animaciones Contextuales Avanzadas - Fase 5
Animaciones específicas por emoción y situación
"""

import pygame
import math
from typing import Tuple, Optional


class AnimadorEmocional:
    """Gestiona animaciones contextuales según estado emocional"""

    def __init__(self):
        self.tiempo_animacion = 0
        self.animacion_activa: Optional[str] = None
        self.duracion_animacion = 0

        # Parámetros de animaciones
        self.config_animaciones = {
            "rebote_feliz": {"duracion": 0.6, "amplitud": 15, "frecuencia": 10},
            "caida_triste": {"duracion": 1.0, "gravedad": 0.5},
            "temblor_miedo": {"duracion": 0.4, "intensidad": 8, "frecuencia": 25},
            "sacudida_dolor": {"duracion": 0.3, "intensidad": 12, "frecuencia": 20},
            "pulso_determinado": {"duracion": 0.5, "escala_max": 1.15, "frecuencia": 8},
            "celebracion_exito": {"duracion": 1.5, "rotacion_max": 360, "saltos": 3},
            "abatimiento_fracaso": {"duracion": 1.2, "caida_y": 30, "fade": True},
        }

    def iniciar_animacion(self, nombre: str):
        """Inicia una nueva animación"""
        if nombre in self.config_animaciones:
            self.animacion_activa = nombre
            self.tiempo_animacion = 0
            self.duracion_animacion = self.config_animaciones[nombre]["duracion"]

    def actualizar(self, dt: float):
        """Actualiza el estado de la animación actual"""
        if self.animacion_activa:
            self.tiempo_animacion += dt

            # Finalizar si excede duración
            if self.tiempo_animacion >= self.duracion_animacion:
                self.animacion_activa = None
                self.tiempo_animacion = 0

    def obtener_offset_rebote_feliz(self) -> Tuple[float, float]:
        """Calcula offset para rebote de felicidad"""
        if self.animacion_activa != "rebote_feliz":
            return 0, 0

        config = self.config_animaciones["rebote_feliz"]
        progreso = self.tiempo_animacion / config["duracion"]

        # Rebote sinusoidal que decrece
        amplitud = config["amplitud"] * (1 - progreso)
        offset_y = -abs(
            math.sin(self.tiempo_animacion * config["frecuencia"]) * amplitud
        )

        return 0, offset_y

    def obtener_offset_caida_triste(self) -> Tuple[float, float]:
        """Calcula offset para caída de tristeza"""
        if self.animacion_activa != "caida_triste":
            return 0, 0

        config = self.config_animaciones["caida_triste"]
        progreso = self.tiempo_animacion / config["duracion"]

        # Caída con gravedad simulada
        offset_y = progreso * progreso * 50 * config["gravedad"]

        return 0, offset_y

    def obtener_offset_temblor_miedo(self) -> Tuple[float, float]:
        """Calcula offset para temblor de miedo"""
        if self.animacion_activa != "temblor_miedo":
            return 0, 0

        config = self.config_animaciones["temblor_miedo"]
        progreso = self.tiempo_animacion / config["duracion"]

        # Temblor errático que decrece
        intensidad = config["intensidad"] * (1 - progreso)
        offset_x = math.sin(self.tiempo_animacion * config["frecuencia"]) * intensidad
        offset_y = (
            math.cos(self.tiempo_animacion * config["frecuencia"] * 1.3) * intensidad
        )

        return offset_x, offset_y

    def obtener_offset_sacudida_dolor(self) -> Tuple[float, float]:
        """Calcula offset para sacudida de dolor"""
        if self.animacion_activa != "sacudida_dolor":
            return 0, 0

        config = self.config_animaciones["sacudida_dolor"]
        progreso = self.tiempo_animacion / config["duracion"]

        # Sacudida violenta que decrece rápido
        intensidad = config["intensidad"] * (1 - progreso) ** 2
        offset_x = math.sin(self.tiempo_animacion * config["frecuencia"]) * intensidad
        offset_y = (
            math.cos(self.tiempo_animacion * config["frecuencia"] * 0.8) * intensidad
        )

        return offset_x, offset_y

    def obtener_escala_pulso_determinado(self) -> float:
        """Calcula escala para pulso de determinación"""
        if self.animacion_activa != "pulso_determinado":
            return 1.0

        config = self.config_animaciones["pulso_determinado"]

        # Pulso de escala
        pulso = math.sin(self.tiempo_animacion * config["frecuencia"])
        escala = 1.0 + (config["escala_max"] - 1.0) * max(0, pulso)

        return escala

    def obtener_datos_celebracion_exito(self) -> Tuple[float, float, float, float]:
        """Calcula offset, rotación y alpha para celebración de éxito"""
        if self.animacion_activa != "celebracion_exito":
            return 0, 0, 0, 1.0

        config = self.config_animaciones["celebracion_exito"]
        progreso = self.tiempo_animacion / config["duracion"]

        # Rotación completa
        rotacion = progreso * config["rotacion_max"]

        # Saltos parabólicos
        t_salto = (self.tiempo_animacion * config["saltos"]) % 1.0
        offset_y = -abs(4 * t_salto * (1 - t_salto)) * 40

        # Sin cambio en x
        offset_x = 0

        # Alpha siempre 1
        alpha = 1.0

        return offset_x, offset_y, rotacion, alpha

    def obtener_datos_abatimiento_fracaso(self) -> Tuple[float, float, float]:
        """Calcula offset y alpha para abatimiento de fracaso"""
        if self.animacion_activa != "abatimiento_fracaso":
            return 0, 0, 1.0

        config = self.config_animaciones["abatimiento_fracaso"]
        progreso = self.tiempo_animacion / config["duracion"]

        # Caída lenta
        offset_y = progreso * config["caida_y"]

        # Fade opcional
        alpha = 1.0 - progreso * 0.3 if config.get("fade", False) else 1.0

        return 0, offset_y, alpha

    def obtener_transformacion_completa(self, emocion: str) -> dict:
        """Obtiene todos los datos de transformación para dibujo"""
        offset_x, offset_y = 0, 0
        escala = 1.0
        rotacion = 0
        alpha = 1.0

        # Animaciones por emoción (continuas)
        if emocion == "feliz":
            offset_x, offset_y = self.obtener_offset_rebote_feliz()
        elif emocion == "triste":
            offset_x, offset_y = self.obtener_offset_caida_triste()
        elif emocion == "miedo":
            offset_x, offset_y = self.obtener_offset_temblor_miedo()
        elif emocion == "dolor":
            offset_x, offset_y = self.obtener_offset_sacudida_dolor()
        elif emocion == "determinado":
            escala = self.obtener_escala_pulso_determinado()

        # Animaciones especiales (eventos)
        if self.animacion_activa == "celebracion_exito":
            ox, oy, rot, a = self.obtener_datos_celebracion_exito()
            offset_x, offset_y, rotacion, alpha = ox, oy, rot, a
        elif self.animacion_activa == "abatimiento_fracaso":
            ox, oy, a = self.obtener_datos_abatimiento_fracaso()
            offset_x, offset_y, alpha = ox, oy, a

        return {
            "offset_x": offset_x,
            "offset_y": offset_y,
            "escala": escala,
            "rotacion": rotacion,
            "alpha": alpha,
        }

    def esta_activa(self) -> bool:
        """Verifica si hay una animación en curso"""
        return self.animacion_activa is not None

    def detener(self):
        """Detiene la animación actual"""
        self.animacion_activa = None
        self.tiempo_animacion = 0


class AnimacionContinua:
    """Animaciones que se ejecutan continuamente según emoción"""

    def __init__(self):
        self.tiempo = 0

    def actualizar(self, dt: float):
        """Actualiza el tiempo global"""
        self.tiempo += dt

    def respiracion_normal(
        self, amplitud: float = 0.05, frecuencia: float = 2.0
    ) -> float:
        """Efecto de respiración (escala sutil)"""
        return 1.0 + math.sin(self.tiempo * frecuencia) * amplitud

    def flotacion_feliz(self, amplitud: float = 5.0, frecuencia: float = 1.5) -> float:
        """Flotación suave para felicidad"""
        return math.sin(self.tiempo * frecuencia) * amplitud

    def oscilacion_tristeza(
        self, amplitud: float = 3.0, frecuencia: float = 0.8
    ) -> float:
        """Oscilación lenta para tristeza"""
        return math.sin(self.tiempo * frecuencia) * amplitud

    def vibrar_miedo(self, intensidad: float = 2.0) -> Tuple[float, float]:
        """Vibración sutil continua para miedo"""
        x = math.sin(self.tiempo * 30) * intensidad
        y = math.cos(self.tiempo * 25) * intensidad
        return x, y

    def latido_dolor(self, frecuencia: float = 4.0) -> float:
        """Pulso de latido para dolor"""
        pulso = (math.sin(self.tiempo * frecuencia) + 1) / 2
        return 1.0 + pulso * 0.08

    def energia_determinacion(self, frecuencia: float = 5.0) -> float:
        """Pulso energético para determinación"""
        return 1.0 + abs(math.sin(self.tiempo * frecuencia)) * 0.1

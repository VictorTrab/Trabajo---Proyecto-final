"""
Ambiente Emocional Reactivo - Fase 5
Efectos ambientales que responden a las emociones del jugador
"""

import pygame
import math
import random
from typing import Tuple
from config.constantes import WINDOW_WIDTH, WINDOW_HEIGHT


class AmbienteEmocional:
    """Sistema de efectos ambientales que reaccionan a emociones"""

    def __init__(self):
        self.tiempo = 0

        # Configuración de iluminación emocional
        self.config_iluminacion = {
            "feliz": {
                "brillo_base": 1.1,
                "saturacion": 1.2,
                "color_tinte": (255, 255, 200),  # Amarillo cálido
                "intensidad_tinte": 0.15,
            },
            "triste": {
                "brillo_base": 0.8,
                "saturacion": 0.7,
                "color_tinte": (100, 120, 150),  # Azul frío
                "intensidad_tinte": 0.25,
            },
            "miedo": {
                "brillo_base": 0.7,
                "saturacion": 0.9,
                "color_tinte": (120, 80, 140),  # Púrpura oscuro
                "intensidad_tinte": 0.3,
                "flicker": True,
            },
            "dolor": {
                "brillo_base": 0.85,
                "saturacion": 1.1,
                "color_tinte": (180, 50, 50),  # Rojo oscuro
                "intensidad_tinte": 0.35,
                "pulso": True,
            },
            "determinado": {
                "brillo_base": 1.15,
                "saturacion": 1.3,
                "color_tinte": (255, 180, 100),  # Naranja energético
                "intensidad_tinte": 0.2,
            },
        }

        # Partículas ambientales
        self.particulas_ambiente = []
        self.max_particulas = 30

    def actualizar(self, dt: float, emocion: str):
        """Actualiza el ambiente según la emoción"""
        self.tiempo += dt

        # Actualizar partículas ambientales
        self._actualizar_particulas_ambiente(dt, emocion)

    def _actualizar_particulas_ambiente(self, dt: float, emocion: str):
        """Actualiza partículas de fondo según emoción"""
        # Generar nuevas partículas si es necesario
        if len(self.particulas_ambiente) < self.max_particulas:
            if random.random() < 0.1:  # 10% de probabilidad por frame
                self._generar_particula_ambiente(emocion)

        # Actualizar y filtrar partículas muertas
        for particula in self.particulas_ambiente[:]:
            particula["x"] += particula["vx"] * dt * 60
            particula["y"] += particula["vy"] * dt * 60
            particula["vida"] -= dt

            # Calcular alpha solo si vida_max > 0
            if particula["vida_max"] > 0:
                particula["alpha"] = int(
                    255 * (particula["vida"] / particula["vida_max"])
                )
            else:
                particula["alpha"] = 0

            # Eliminar si está fuera de pantalla o muerta
            if (
                particula["vida"] <= 0
                or particula["x"] < -50
                or particula["x"] > WINDOW_WIDTH + 50
                or particula["y"] < -50
                or particula["y"] > WINDOW_HEIGHT + 50
            ):
                self.particulas_ambiente.remove(particula)

    def _generar_particula_ambiente(self, emocion: str):
        """Genera una partícula ambiental según la emoción"""
        particula = {
            "x": random.uniform(0, WINDOW_WIDTH),
            "y": random.uniform(0, WINDOW_HEIGHT),
            "vx": 0,
            "vy": 0,
            "vida": 0,
            "vida_max": 0,
            "tamano": 0,
            "color": (255, 255, 255),
            "alpha": 255,
        }

        if emocion == "feliz":
            # Burbujas flotantes doradas
            particula["vx"] = random.uniform(-0.5, 0.5)
            particula["vy"] = random.uniform(-1, -0.3)
            particula["vida"] = particula["vida_max"] = random.uniform(3, 6)
            particula["tamano"] = random.uniform(2, 5)
            particula["color"] = (255, 220, 100)

        elif emocion == "triste":
            # Gotas cayendo
            particula["x"] = random.uniform(0, WINDOW_WIDTH)
            particula["y"] = -10
            particula["vx"] = 0
            particula["vy"] = random.uniform(2, 4)
            particula["vida"] = particula["vida_max"] = random.uniform(4, 7)
            particula["tamano"] = random.uniform(1, 3)
            particula["color"] = (100, 150, 200)

        elif emocion == "miedo":
            # Chispas erráticas
            particula["vx"] = random.uniform(-2, 2)
            particula["vy"] = random.uniform(-2, 2)
            particula["vida"] = particula["vida_max"] = random.uniform(1, 2)
            particula["tamano"] = random.uniform(1, 3)
            particula["color"] = (150, 100, 180)

        elif emocion == "dolor":
            # Centellas rojas
            particula["vx"] = random.uniform(-1, 1)
            particula["vy"] = random.uniform(-1, 1)
            particula["vida"] = particula["vida_max"] = random.uniform(1.5, 3)
            particula["tamano"] = random.uniform(2, 4)
            particula["color"] = (200, 80, 80)

        elif emocion == "determinado":
            # Destellos naranjas ascendentes
            particula["vx"] = random.uniform(-0.3, 0.3)
            particula["vy"] = random.uniform(-1.5, -0.5)
            particula["vida"] = particula["vida_max"] = random.uniform(2, 4)
            particula["tamano"] = random.uniform(2, 5)
            particula["color"] = (255, 150, 50)

        self.particulas_ambiente.append(particula)

    def dibujar_particulas_ambiente(self, superficie: pygame.Surface):
        """Dibuja las partículas ambientales"""
        for particula in self.particulas_ambiente:
            if particula["vida"] <= 0:
                continue

            color_alpha = (*particula["color"], max(0, min(255, particula["alpha"])))
            radio = max(
                1,
                int(particula["tamano"] * (particula["vida"] / particula["vida_max"])),
            )

            # Crear superficie temporal con transparencia
            surf_temp = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf_temp, color_alpha, (radio, radio), radio)

            superficie.blit(
                surf_temp, (int(particula["x"] - radio), int(particula["y"] - radio))
            )

    def aplicar_iluminacion_emocional(
        self, superficie: pygame.Surface, emocion: str
    ) -> pygame.Surface:
        """Aplica efectos de iluminación según emoción (opcional, puede ser costoso)"""
        config = self.config_iluminacion.get(emocion)
        if not config:
            return superficie

        # Crear overlay de tinte
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        # Aplicar tinte
        color_tinte = config["color_tinte"]
        intensidad = config["intensidad_tinte"]

        # Modificar intensidad si hay efectos especiales
        if config.get("flicker", False):
            # Parpadeo para miedo
            intensidad *= 0.8 + 0.2 * abs(math.sin(self.tiempo * 15))

        if config.get("pulso", False):
            # Pulso para dolor
            intensidad *= 0.7 + 0.3 * abs(math.sin(self.tiempo * 6))

        alpha = int(255 * intensidad)
        overlay.fill((*color_tinte, alpha))

        # Aplicar overlay
        superficie.blit(overlay, (0, 0))

        return superficie

    def obtener_offset_distorsion_fondo(self, emocion: str) -> Tuple[float, float]:
        """Obtiene offset para distorsión del fondo según emoción"""
        offset_x, offset_y = 0, 0

        if emocion == "miedo":
            # Ondulación sutil
            offset_x = math.sin(self.tiempo * 5) * 2
            offset_y = math.cos(self.tiempo * 4) * 2

        elif emocion == "dolor":
            # Vibración
            offset_x = math.sin(self.tiempo * 20) * 1.5
            offset_y = math.cos(self.tiempo * 18) * 1.5

        return offset_x, offset_y

    def generar_efecto_clima(self, superficie: pygame.Surface, emocion: str):
        """Genera efectos de 'clima emocional' en pantalla"""
        if emocion == "triste":
            # Lluvia adicional (más densa que partículas normales)
            for _ in range(5):
                x = random.randint(0, WINDOW_WIDTH)
                y = random.randint(0, WINDOW_HEIGHT)
                largo = random.randint(10, 20)

                color = (150, 180, 200, 80)
                surf_gota = pygame.Surface((2, largo), pygame.SRCALPHA)
                surf_gota.fill(color)
                superficie.blit(surf_gota, (x, y))

        elif emocion == "miedo":
            # Sombras danzantes
            if random.random() < 0.05:
                x = random.randint(0, WINDOW_WIDTH)
                y = random.randint(0, WINDOW_HEIGHT)
                radio = random.randint(20, 50)

                surf_sombra = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf_sombra, (20, 0, 40, 30), (radio, radio), radio)
                superficie.blit(surf_sombra, (x - radio, y - radio))

    def limpiar(self):
        """Limpia todas las partículas ambientales"""
        self.particulas_ambiente.clear()
        self.tiempo = 0


class FondoDinamico:
    """Fondo que cambia según el estado emocional"""

    def __init__(self):
        self.gradientes = {
            "feliz": [(255, 220, 150), (255, 180, 100)],
            "triste": [(80, 100, 130), (50, 70, 100)],
            "miedo": [(60, 40, 80), (40, 20, 60)],
            "dolor": [(120, 60, 60), (80, 40, 40)],
            "determinado": [(150, 100, 50), (120, 80, 40)],
            "neutral": [(40, 40, 50), (30, 30, 40)],
        }

    def dibujar_fondo_gradiente(self, superficie: pygame.Surface, emocion: str):
        """Dibuja un fondo con gradiente según emoción"""
        colores = self.gradientes.get(emocion, self.gradientes["neutral"])
        color_superior = colores[0]
        color_inferior = colores[1]

        alto = WINDOW_HEIGHT

        for y in range(alto):
            ratio = y / alto
            r = int(color_superior[0] * (1 - ratio) + color_inferior[0] * ratio)
            g = int(color_superior[1] * (1 - ratio) + color_inferior[1] * ratio)
            b = int(color_superior[2] * (1 - ratio) + color_inferior[2] * ratio)

            pygame.draw.line(superficie, (r, g, b), (0, y), (WINDOW_WIDTH, y))

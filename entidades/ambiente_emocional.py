"""
Ambiente Emocional Reactivo - Fase 5 (Optimizado)
Efectos ambientales simples
"""

import pygame
import random
from config.constantes import WINDOW_WIDTH, WINDOW_HEIGHT


class AmbienteEmocional:
    """Sistema de efectos ambientales simples"""

    def __init__(self):
        self.tiempo = 0
        self.particulas = []

    def actualizar(self, dt: float, emocion: str):
        """Actualiza ambiente"""
        self.tiempo += dt

        # Generar partículas
        if len(self.particulas) < 20 and random.random() < 0.08:
            self._generar_particula(emocion)

        # Actualizar partículas
        for p in self.particulas[:]:
            p["x"] += p["vx"] * dt * 60
            p["y"] += p["vy"] * dt * 60
            p["vida"] -= dt

            if p["vida"] <= 0 or p["y"] > WINDOW_HEIGHT + 20:
                self.particulas.remove(p)

    def _generar_particula(self, emocion: str):
        """Genera partícula según emoción"""
        p = {
            "x": random.uniform(0, WINDOW_WIDTH),
            "y": 0,
            "vx": 0,
            "vy": 0,
            "vida": 0,
            "color": (255, 255, 255),
        }

        if emocion == "feliz":
            p["vx"] = random.uniform(-0.3, 0.3)
            p["vy"] = random.uniform(-0.5, 0)
            p["vida"] = 4
            p["color"] = (255, 220, 100)
        elif emocion == "triste":
            p["y"] = -10
            p["vy"] = random.uniform(2, 3)
            p["vida"] = 5
            p["color"] = (100, 150, 200)
        else:
            return

        self.particulas.append(p)

    def dibujar_fondo(self, superficie: pygame.Surface, emocion: str):
        """Dibuja overlay de fondo"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        if emocion == "feliz":
            overlay.fill((255, 255, 200, 20))
        elif emocion == "triste":
            overlay.fill((100, 120, 150, 30))

        superficie.blit(overlay, (0, 0))

    def dibujar_particulas(self, superficie: pygame.Surface):
        """Dibuja partículas"""
        for p in self.particulas:
            alpha = int(100 * (p["vida"] / 5))
            pygame.draw.circle(
                superficie, (*p["color"], alpha), (int(p["x"]), int(p["y"])), 2
            )

    def limpiar(self):
        self.particulas.clear()

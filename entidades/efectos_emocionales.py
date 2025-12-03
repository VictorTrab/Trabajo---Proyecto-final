"""
Sistema de Efectos Visuales Emocionales - Fase 5 (Optimizado)
Efectos esenciales por emoción
"""

import pygame
import math
import random
from typing import List, Tuple
from config.constantes import NEON_BLUE, NEON_YELLOW, RED, WINDOW_WIDTH, WINDOW_HEIGHT


class Particula:
    """Partícula visual individual"""

    def __init__(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int],
        velocidad: Tuple[float, float],
        vida: float,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocidad
        self.vida = vida
        self.vida_max = vida

    def actualizar(self, dt: float):
        """Actualiza posición y estado"""
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vida -= dt

    def dibujar(self, superficie: pygame.Surface):
        """Dibuja la partícula"""
        if self.vida <= 0:
            return
        alpha = int(255 * (self.vida / self.vida_max))
        radio = int(4 * (self.vida / self.vida_max))
        if radio > 0:
            surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color[:3], alpha), (radio, radio), radio)
            superficie.blit(surf, (int(self.x - radio), int(self.y - radio)))

    def esta_viva(self) -> bool:
        return self.vida > 0


class SistemaParticulas:
    """Generador de partículas emocionales"""

    def __init__(self):
        self.particulas: List[Particula] = []

    def generar_felicidad(self, x: float, y: float):
        """Partículas amarillas"""
        for _ in range(8):
            angulo = random.uniform(0, 2 * math.pi)
            vel = random.uniform(2, 4)
            self.particulas.append(
                Particula(
                    x,
                    y,
                    NEON_YELLOW,
                    (math.cos(angulo) * vel, math.sin(angulo) * vel),
                    0.8,
                )
            )

    def generar_tristeza(self, ancho: int):
        """Gotas azules cayendo"""
        if random.random() < 0.08:
            x = random.uniform(0, ancho)
            self.particulas.append(
                Particula(x, -10, NEON_BLUE, (0, random.uniform(3, 5)), 2.5)
            )

    def generar_dolor(self, x: float, y: float):
        """Ondas rojas"""
        for i in range(6):
            angulo = (i / 6) * 2 * math.pi
            self.particulas.append(
                Particula(x, y, RED, (math.cos(angulo) * 3, math.sin(angulo) * 3), 0.6)
            )

    def actualizar(self, dt: float):
        for p in self.particulas:
            p.actualizar(dt)
        self.particulas = [p for p in self.particulas if p.esta_viva()]

    def dibujar(self, superficie: pygame.Surface):
        for p in self.particulas:
            p.dibujar(superficie)

    def limpiar(self):
        self.particulas.clear()


class EfectosEmocionales:
    """Sistema de efectos visuales emocionales"""

    def __init__(self):
        self.particulas = SistemaParticulas()
        self.tiempo = 0
        self.ultimo_efecto = 0

    def actualizar(self, dt: float, emocion: str, pos_cubo: Tuple[float, float]):
        """Actualiza efectos"""
        self.tiempo += dt
        self.particulas.actualizar(dt)

        # Efectos continuos
        if emocion == "feliz" and self.tiempo - self.ultimo_efecto >= 0.5:
            self.particulas.generar_felicidad(pos_cubo[0], pos_cubo[1])
            self.ultimo_efecto = self.tiempo
        elif emocion == "triste":
            self.particulas.generar_tristeza(WINDOW_WIDTH)

    def aplicar_efectos_pantalla(
        self, superficie: pygame.Surface, emocion: str
    ) -> Tuple[int, int]:
        """Aplica filtros de pantalla"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        if emocion == "feliz":
            overlay.fill((*NEON_YELLOW[:3], 30))
            superficie.blit(overlay, (0, 0))
        elif emocion == "triste":
            overlay.fill((20, 40, 80, 50))
            superficie.blit(overlay, (0, 0))
        elif emocion == "dolor":
            pulso = (math.sin(self.tiempo * 8) + 1) / 2
            overlay.fill((*RED[:3], int(60 * pulso)))
            superficie.blit(overlay, (0, 0))

        return 0, 0

    def dibujar_particulas(self, superficie: pygame.Surface):
        self.particulas.dibujar(superficie)

    def evento_especial(self, tipo: str, posicion: Tuple[float, float]):
        """Efecto especial en eventos"""
        if tipo == "exito":
            for _ in range(2):
                self.particulas.generar_felicidad(posicion[0], posicion[1])
        elif tipo == "dano":
            self.particulas.generar_dolor(posicion[0], posicion[1])

    def limpiar(self):
        self.particulas.limpiar()
        self.tiempo = 0
        self.ultimo_efecto = 0

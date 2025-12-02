"""
Sistema de Efectos Visuales Emocionales - Fase 5
Filtros, partículas y efectos de post-procesamiento por emoción
"""

import pygame
import math
import random
from typing import List, Tuple
from config.constantes import (
    NEON_BLUE,
    NEON_PINK,
    NEON_YELLOW,
    NEON_GREEN,
    NEON_ORANGE,
    PURPLE,
    RED,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


class Particula:
    """Partícula visual individual"""

    def __init__(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int],
        velocidad: Tuple[float, float],
        vida: float,
        tamano: float = 3,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocidad
        self.vida = vida
        self.vida_max = vida
        self.tamano = tamano
        self.alpha = 255

    def actualizar(self, dt: float):
        """Actualiza posición y estado"""
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vida -= dt
        # Alpha decrece con la vida
        self.alpha = int(255 * (self.vida / self.vida_max))

    def dibujar(self, superficie: pygame.Surface):
        """Dibuja la partícula con transparencia"""
        if self.vida <= 0:
            return

        color_alpha = (*self.color[:3], max(0, min(255, self.alpha)))
        radio = int(self.tamano * (self.vida / self.vida_max))

        if radio > 0:
            surf_temp = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf_temp, color_alpha, (radio, radio), radio)
            superficie.blit(surf_temp, (int(self.x - radio), int(self.y - radio)))

    def esta_viva(self) -> bool:
        """Verifica si la partícula sigue activa"""
        return self.vida > 0


class SistemaParticulas:
    """Generador y administrador de partículas emocionales"""

    def __init__(self):
        self.particulas: List[Particula] = []

    def generar_explosion_felicidad(self, x: float, y: float):
        """Explosión de partículas amarillas brillantes"""
        for _ in range(15):
            angulo = random.uniform(0, 2 * math.pi)
            velocidad_mag = random.uniform(2, 5)
            vx = math.cos(angulo) * velocidad_mag
            vy = math.sin(angulo) * velocidad_mag

            particula = Particula(
                x,
                y,
                NEON_YELLOW,
                (vx, vy),
                vida=random.uniform(0.5, 1.0),
                tamano=random.uniform(4, 8),
            )
            self.particulas.append(particula)

    def generar_lluvia_tristeza(self, ancho: int, alto: int):
        """Gotas de tristeza cayendo (azules)"""
        if random.random() < 0.1:  # 10% de probabilidad por frame
            x = random.uniform(0, ancho)
            particula = Particula(
                x,
                -10,
                NEON_BLUE,
                (0, random.uniform(3, 6)),
                vida=random.uniform(2, 3),
                tamano=random.uniform(2, 4),
            )
            self.particulas.append(particula)

    def generar_chispas_miedo(self, x: float, y: float):
        """Chispas erráticas de miedo (púrpuras)"""
        for _ in range(3):
            vx = random.uniform(-4, 4)
            vy = random.uniform(-4, 4)

            particula = Particula(
                x,
                y,
                PURPLE,
                (vx, vy),
                vida=random.uniform(0.3, 0.7),
                tamano=random.uniform(2, 5),
            )
            self.particulas.append(particula)

    def generar_pulso_dolor(self, x: float, y: float):
        """Ondas pulsantes de dolor (rojas)"""
        for i in range(8):
            angulo = (i / 8) * 2 * math.pi
            vx = math.cos(angulo) * 3
            vy = math.sin(angulo) * 3

            particula = Particula(x, y, RED, (vx, vy), vida=0.8, tamano=6)
            self.particulas.append(particula)

    def generar_estela_determinacion(self, x: float, y: float):
        """Estela brillante de determinación (naranja neón)"""
        for _ in range(2):
            particula = Particula(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                NEON_ORANGE,
                (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
                vida=random.uniform(0.4, 0.8),
                tamano=random.uniform(3, 6),
            )
            self.particulas.append(particula)

    def actualizar(self, dt: float):
        """Actualiza todas las partículas"""
        for particula in self.particulas:
            particula.actualizar(dt)

        # Eliminar partículas muertas
        self.particulas = [p for p in self.particulas if p.esta_viva()]

    def dibujar(self, superficie: pygame.Surface):
        """Dibuja todas las partículas"""
        for particula in self.particulas:
            particula.dibujar(superficie)

    def limpiar(self):
        """Elimina todas las partículas"""
        self.particulas.clear()


class FiltroEmocional:
    """Filtros de pantalla completa según emoción"""

    @staticmethod
    def aplicar_overlay_felicidad(superficie: pygame.Surface, intensidad: float = 0.15):
        """Overlay amarillo cálido brillante"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        alpha = int(255 * intensidad)
        overlay.fill((*NEON_YELLOW[:3], alpha))
        superficie.blit(overlay, (0, 0))

    @staticmethod
    def aplicar_overlay_tristeza(superficie: pygame.Surface, intensidad: float = 0.25):
        """Overlay azul oscuro apagado"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        alpha = int(255 * intensidad)
        # Azul más oscuro
        color_tristeza = (20, 40, 80, alpha)
        overlay.fill(color_tristeza)
        superficie.blit(overlay, (0, 0))

    @staticmethod
    def aplicar_temblor_miedo(
        superficie: pygame.Surface, tiempo: float, intensidad: int = 3
    ):
        """Efecto de temblor en la pantalla"""
        offset_x = int(math.sin(tiempo * 30) * intensidad)
        offset_y = int(math.cos(tiempo * 25) * intensidad)
        return offset_x, offset_y

    @staticmethod
    def aplicar_pulso_dolor(
        superficie: pygame.Surface, tiempo: float, intensidad: float = 0.3
    ):
        """Pulso rojo palpitante"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        # Pulso sinusoidal
        pulso = (math.sin(tiempo * 8) + 1) / 2  # 0 a 1
        alpha = int(255 * intensidad * pulso)
        overlay.fill((*RED[:3], alpha))
        superficie.blit(overlay, (0, 0))

    @staticmethod
    def aplicar_brillo_determinacion(
        superficie: pygame.Surface, intensidad: float = 0.2
    ):
        """Brillo naranja energético"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        alpha = int(255 * intensidad)
        overlay.fill((*NEON_ORANGE[:3], alpha))
        superficie.blit(overlay, (0, 0))


class EfectosEmocionales:
    """Sistema principal de efectos visuales emocionales"""

    def __init__(self):
        self.sistema_particulas = SistemaParticulas()
        self.tiempo_acumulado = 0
        self.ultimo_efecto_particulas = 0
        self.emociones_config = {
            "feliz": {
                "particulas_continuas": True,
                "intervalo_particulas": 0.5,
                "overlay": True,
                "intensidad_overlay": 0.12,
            },
            "triste": {
                "lluvia_activa": True,
                "overlay": True,
                "intensidad_overlay": 0.2,
            },
            "miedo": {
                "particulas_continuas": True,
                "intervalo_particulas": 0.3,
                "temblor": True,
                "intensidad_temblor": 4,
            },
            "dolor": {"pulso_activo": True, "intensidad_pulso": 0.25},
            "determinado": {
                "particulas_continuas": True,
                "intervalo_particulas": 0.2,
                "overlay": True,
                "intensidad_overlay": 0.15,
            },
        }

    def actualizar(
        self, dt: float, emocion_actual: str, posicion_cubo: Tuple[float, float]
    ):
        """Actualiza efectos según emoción"""
        self.tiempo_acumulado += dt
        self.sistema_particulas.actualizar(dt)

        config = self.emociones_config.get(emocion_actual, {})

        # Generar partículas continuas
        if config.get("particulas_continuas", False):
            intervalo = config.get("intervalo_particulas", 0.5)
            if self.tiempo_acumulado - self.ultimo_efecto_particulas >= intervalo:
                self._generar_particulas_emocion(emocion_actual, posicion_cubo)
                self.ultimo_efecto_particulas = self.tiempo_acumulado

        # Lluvia de tristeza
        if config.get("lluvia_activa", False):
            self.sistema_particulas.generar_lluvia_tristeza(WINDOW_WIDTH, WINDOW_HEIGHT)

    def _generar_particulas_emocion(self, emocion: str, pos: Tuple[float, float]):
        """Genera partículas según tipo de emoción"""
        x, y = pos

        if emocion == "feliz":
            self.sistema_particulas.generar_explosion_felicidad(x, y)
        elif emocion == "miedo":
            self.sistema_particulas.generar_chispas_miedo(x, y)
        elif emocion == "determinado":
            self.sistema_particulas.generar_estela_determinacion(x, y)

    def aplicar_efectos_pantalla(
        self, superficie: pygame.Surface, emocion_actual: str
    ) -> Tuple[int, int]:
        """Aplica filtros y efectos de pantalla. Retorna offset (x, y) para temblor"""
        config = self.emociones_config.get(emocion_actual, {})
        offset_x, offset_y = 0, 0

        # Overlays
        if config.get("overlay", False):
            intensidad = config.get("intensidad_overlay", 0.15)

            if emocion_actual == "feliz":
                FiltroEmocional.aplicar_overlay_felicidad(superficie, intensidad)
            elif emocion_actual == "triste":
                FiltroEmocional.aplicar_overlay_tristeza(superficie, intensidad)
            elif emocion_actual == "determinado":
                FiltroEmocional.aplicar_brillo_determinacion(superficie, intensidad)

        # Temblor (miedo)
        if config.get("temblor", False):
            intensidad_temblor = config.get("intensidad_temblor", 3)
            offset_x, offset_y = FiltroEmocional.aplicar_temblor_miedo(
                superficie, self.tiempo_acumulado, intensidad_temblor
            )

        # Pulso (dolor)
        if config.get("pulso_activo", False):
            intensidad_pulso = config.get("intensidad_pulso", 0.25)
            FiltroEmocional.aplicar_pulso_dolor(
                superficie, self.tiempo_acumulado, intensidad_pulso
            )

        return offset_x, offset_y

    def dibujar_particulas(self, superficie: pygame.Surface):
        """Dibuja todas las partículas"""
        self.sistema_particulas.dibujar(superficie)

    def evento_especial(self, tipo: str, posicion: Tuple[float, float]):
        """Genera efecto especial en eventos (completar nivel, daño, etc)"""
        x, y = posicion

        if tipo == "exito":
            for _ in range(3):
                self.sistema_particulas.generar_explosion_felicidad(x, y)
        elif tipo == "dano":
            self.sistema_particulas.generar_pulso_dolor(x, y)
        elif tipo == "powerup":
            for _ in range(2):
                self.sistema_particulas.generar_explosion_felicidad(x, y)

    def limpiar(self):
        """Limpia todos los efectos"""
        self.sistema_particulas.limpiar()
        self.tiempo_acumulado = 0
        self.ultimo_efecto_particulas = 0

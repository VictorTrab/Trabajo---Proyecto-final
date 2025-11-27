"""
Entidades del juego: Zonas, Obstáculos y Efectos Visuales.
Este módulo mantiene la estructura orientada a objetos separando la lógica de las entidades
de la lógica principal del juego.
"""

import pygame
import numpy as np
from constantes import *


class GameEntity:
    """Clase base para cualquier entidad en el juego"""

    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)

    def update(self):
        pass

    def draw(self, screen):
        pass


class Zone(GameEntity):
    """
    Clase base para áreas especiales en el nivel.
    Define una región (Rectángulo o Círculo) que afecta al jugador.
    """

    def __init__(self, x, y, width, height, zone_type):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.type = zone_type
        self.active = True
        self.animation_offset = 0

    def is_inside(self, point):
        """Verifica si un punto (x, y) está dentro de la zona"""
        return self.rect.collidepoint(point)

    def check_collision_polygon(self, vertices):
        """
        Verifica si algún vértice del polígono entra en la zona.
        Retorna True si hay colisión.
        """
        for v in vertices:
            if self.rect.collidepoint(v[0], v[1]):
                return True
        return False

    def apply_effect(self, player):
        """Método virtual para aplicar efectos al jugador"""
        pass

    def update(self):
        self.animation_offset += 0.1


class ObstacleZone(Zone):
    """
    Zona prohibida. Si el jugador la toca, se marca como inválido o falla.
    Visualmente: Rojo semitransparente con borde de advertencia.
    """

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, ZONE_TYPE_OBSTACLE)

    def draw(self, screen):
        # Efecto pulsante
        alpha = int(100 + 50 * np.sin(self.animation_offset))

        # Superficie transparente
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((*COLOR_DANGER, alpha))
        screen.blit(s, (self.position[0], self.position[1]))

        # Borde estilo "Peligro"
        pygame.draw.rect(screen, COLOR_DANGER, self.rect, 2)

        # Líneas diagonales (estilo zona de construcción)
        for i in range(0, self.width + self.height, 20):
            start_pos = (self.position[0] + i, self.position[1])
            end_pos = (self.position[0] + i - 20, self.position[1] + 20)
            # Recorte simple para mantener dentro del rect (opcional, simplificado aquí)
            if i < self.width:
                pygame.draw.line(
                    screen,
                    (255, 100, 100),
                    (self.position[0] + i, self.position[1]),
                    (
                        self.position[0] + i - self.height,
                        self.position[1] + self.height,
                    ),
                    1,
                )

    def apply_effect(self, player):
        # En este diseño, tocar un obstáculo invalida el movimiento o causa fallo
        # Retornamos True para indicar colisión crítica
        return True


class DistortionZone(Zone):
    """
    Campo de distorsión. Altera la escala o rotación del jugador temporalmente.
    Visualmente: Ondas o color púrpura/azul.
    """

    def __init__(self, x, y, width, height, intensity=0.02):
        super().__init__(x, y, width, height, ZONE_TYPE_DISTORTION)
        self.intensity = intensity

    def draw(self, screen):
        # Efecto de onda
        alpha = int(50 + 30 * np.sin(self.animation_offset * 2))
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((*NEON_PURPLE, alpha))
        screen.blit(s, (self.position[0], self.position[1]))
        pygame.draw.rect(screen, NEON_PURPLE, self.rect, 1)

    def apply_effect(self, player):
        # Efecto: Escala pulsante forzada
        distortion = np.sin(self.animation_offset * 5) * self.intensity
        player.scale = max(0.1, min(3.0, player.scale + distortion))
        # Efecto visual en el jugador
        player.in_distortion = True


class GravityZone(Zone):
    """
    Zona de gravedad. Arrastra al jugador en una dirección.
    """

    def __init__(self, x, y, width, height, force_vector):
        super().__init__(x, y, width, height, ZONE_TYPE_GRAVITY)
        self.force = np.array(force_vector, dtype=float)

    def draw(self, screen):
        # Flechas indicando dirección
        alpha = 80
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((*NEON_BLUE, alpha))
        screen.blit(s, (self.position[0], self.position[1]))

        # Dibujar flechas simples
        center = self.rect.center
        end_pos = (center[0] + self.force[0] * 10, center[1] + self.force[1] * 10)
        pygame.draw.line(screen, NEON_CYAN, center, end_pos, 2)

    def apply_effect(self, player):
        player.position[0] += self.force[0]
        player.position[1] += self.force[1]

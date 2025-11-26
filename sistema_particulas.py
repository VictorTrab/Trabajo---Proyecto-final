"""
Sistema de partículas para efectos visuales Cyberpunk
"""

import pygame
import numpy as np
from constantes import *
import random


class Particle:
    """Clase para una partícula individual"""

    def __init__(self, x, y, color, velocity=None, lifetime=60, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.initial_size = size

        # Velocidad aleatoria si no se especifica
        if velocity is None:
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(1, 3)
            self.vx = np.cos(angle) * speed
            self.vy = np.sin(angle) * speed
        else:
            self.vx, self.vy = velocity

        # Efecto de gravedad/aceleración
        self.gravity = 0.1
        self.alpha = 255

    def update(self):
        """Actualiza la posición y estado de la partícula"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # Agregar efecto de caída

        # Reducir tamaño y transparencia con el tiempo
        self.lifetime -= 1
        life_ratio = self.lifetime / self.max_lifetime
        self.size = max(1, self.initial_size * life_ratio)
        self.alpha = int(255 * life_ratio)

        return self.lifetime > 0

    def draw(self, screen):
        """Dibuja la partícula con efecto glow"""
        if self.lifetime <= 0:
            return

        # Color con alpha
        color_with_alpha = tuple(
            int(min(255, max(0, c * (self.alpha / 255)))) for c in self.color
        )

        # Dibujar capas de glow
        for layer in range(3):
            glow_size = int(self.size + layer * 2)
            glow_alpha = self.alpha // (layer + 1)
            glow_color = tuple(int(c * (glow_alpha / 255)) for c in self.color)

            pygame.draw.circle(
                screen, glow_color, (int(self.x), int(self.y)), glow_size
            )


class ParticleSystem:
    """Sistema para manejar múltiples partículas"""

    def __init__(self, screen):
        self.screen = screen
        self.particles = []

    def add_particle(self, x, y, color, velocity=None, lifetime=60, size=3):
        """Agrega una partícula al sistema"""
        particle = Particle(x, y, color, velocity, lifetime, size)
        self.particles.append(particle)

    def emit_burst(self, x, y, color, count=10, spread=2.0):
        """Emite una ráfaga de partículas desde un punto"""
        for _ in range(count):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(0.5, spread)
            velocity = (np.cos(angle) * speed, np.sin(angle) * speed)
            lifetime = random.randint(30, 60)
            size = random.randint(2, 5)
            self.add_particle(x, y, color, velocity, lifetime, size)

    def emit_trail(self, x, y, color, direction=None):
        """Emite partículas en forma de rastro"""
        if direction is None:
            velocity = None
        else:
            # Agregar variación aleatoria a la dirección
            angle_variation = random.uniform(-0.5, 0.5)
            speed = random.uniform(0.5, 2.0)
            vx = direction[0] * speed + random.uniform(-1, 1)
            vy = direction[1] * speed + random.uniform(-1, 1)
            velocity = (vx, vy)

        lifetime = random.randint(20, 40)
        size = random.randint(2, 4)
        self.add_particle(x, y, color, velocity, lifetime, size)

    def emit_glow(self, x, y, color, radius=50, count=5):
        """Emite partículas que brillan alrededor de un punto"""
        for _ in range(count):
            # Partículas en posiciones aleatorias alrededor del punto
            angle = random.uniform(0, 2 * np.pi)
            distance = random.uniform(0, radius)
            px = x + np.cos(angle) * distance
            py = y + np.sin(angle) * distance

            # Velocidad hacia afuera lenta
            velocity = (
                np.cos(angle) * random.uniform(0.1, 0.5),
                np.sin(angle) * random.uniform(0.1, 0.5),
            )

            lifetime = random.randint(40, 80)
            size = random.randint(3, 6)
            self.add_particle(px, py, color, velocity, lifetime, size)

    def emit_spark(self, x, y, color, velocity_base=(0, 0)):
        """Emite chispas (partículas rápidas y pequeñas)"""
        for _ in range(random.randint(3, 7)):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(3, 6)
            vx = np.cos(angle) * speed + velocity_base[0]
            vy = np.sin(angle) * speed + velocity_base[1]
            velocity = (vx, vy)

            lifetime = random.randint(15, 30)
            size = random.randint(1, 3)
            self.add_particle(x, y, color, velocity, lifetime, size)

    def update(self):
        """Actualiza todas las partículas"""
        # Actualizar y filtrar partículas muertas
        self.particles = [p for p in self.particles if p.update()]

    def draw(self):
        """Dibuja todas las partículas"""
        for particle in self.particles:
            particle.draw(self.screen)

    def clear(self):
        """Limpia todas las partículas"""
        self.particles.clear()

    def get_particle_count(self):
        """Retorna el número de partículas activas"""
        return len(self.particles)


class MovementTrailEffect:
    """Efecto especial de rastro para movimiento de figuras sobre el teselado"""

    def __init__(self, particle_system):
        self.particle_system = particle_system
        self.last_position = None
        self.color = NEON_CYAN
        self.emit_counter = 0
        self.emit_rate = 2  # Emitir cada N frames

    def update_position(self, x, y, color=None):
        """Actualiza la posición y emite partículas según movimiento"""
        if color is not None:
            self.color = color

        current_pos = np.array([x, y])

        if self.last_position is not None:
            # Calcular distancia y dirección del movimiento
            delta = current_pos - self.last_position
            distance = np.linalg.norm(delta)

            # Solo emitir si hay movimiento significativo
            if distance > 3:
                self.emit_counter += 1

                if self.emit_counter >= self.emit_rate:
                    self.emit_counter = 0

                    # Dirección normalizada inversa (hacia atrás)
                    if distance > 0:
                        direction = -delta / distance
                    else:
                        direction = np.array([0, 0])

                    # Emitir rastro con variaciones de color
                    trail_colors = [
                        self.color,
                        tuple(min(255, int(c * 1.2)) for c in self.color),
                        tuple(max(0, int(c * 0.8)) for c in self.color),
                    ]

                    for _ in range(random.randint(2, 4)):
                        color_choice = random.choice(trail_colors)
                        self.particle_system.emit_trail(
                            x + random.uniform(-5, 5),
                            y + random.uniform(-5, 5),
                            color_choice,
                            direction,
                        )

        self.last_position = current_pos.copy()

    def emit_contact_effect(self, x, y, color=None):
        """Emite efecto cuando la figura toca el teselado"""
        if color is None:
            color = self.color

        # Ráfaga de partículas
        self.particle_system.emit_burst(x, y, color, count=15, spread=3.0)

        # Chispas adicionales
        self.particle_system.emit_spark(x, y, NEON_YELLOW)

    def reset(self):
        """Resetea el rastro"""
        self.last_position = None
        self.emit_counter = 0

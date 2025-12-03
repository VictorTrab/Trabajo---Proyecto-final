"""
CUBO: Protagonista del juego - Arquitecto del Caos
Entidad robótica geométrica con 4 zonas de atracción
"""

import pygame
import numpy as np
from config.constantes import *


class Cubo:
    """Clase principal del protagonista CUBO"""

    # Estados emocionales
    EMOCION_NEUTRAL = "neutral"
    EMOCION_FELIZ = "feliz"
    EMOCION_TRISTE = "triste"
    EMOCION_MIEDO = "miedo"
    EMOCION_DOLOR = "dolor"
    EMOCION_DETERMINADO = "determinado"

    def __init__(self, x, y):
        # Posición y física
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.size = 40  # Tamaño del cubo

        # Zonas de atracción (arriba, abajo, izquierda, derecha)
        self.zonas_atraccion = {
            "arriba": {
                "offset": (0, -self.size / 2 - 15),
                "ocupada": False,
                "pieza": None,
            },
            "abajo": {
                "offset": (0, self.size / 2 + 15),
                "ocupada": False,
                "pieza": None,
            },
            "izquierda": {
                "offset": (-self.size / 2 - 15, 0),
                "ocupada": False,
                "pieza": None,
            },
            "derecha": {
                "offset": (self.size / 2 + 15, 0),
                "ocupada": False,
                "pieza": None,
            },
        }

        # Estado emocional
        self.emocion_actual = self.EMOCION_NEUTRAL
        self.emocion_timer = 0
        self.emocion_duracion = 1.0  # Duración de emociones temporales

        # Animación
        self.animation_offset = 0
        self.bounce_offset = 0
        self.rotation_angle = 0

        # Estado de CUBO
        self.invulnerable = False
        self.invulnerabilidad_timer = 0
        self.respawn_timer = 0
        self.impactos_recibidos = 0  # Contador de impactos directos
        self.max_impactos = 2  # Máximo de impactos antes de ser destruido

        # Piezas transportadas
        self.pieza_sostenida = None
        self.zona_pieza = None

    @property
    def x(self):
        """Propiedad para acceso compatible a coordenada X"""
        return self.position[0]

    @property
    def y(self):
        """Propiedad para acceso compatible a coordenada Y"""
        return self.position[1]

    @x.setter
    def x(self, value):
        """Setter para coordenada X"""
        self.position[0] = value

    @y.setter
    def y(self, value):
        """Setter para coordenada Y"""
        self.position[1] = value

    def mover(self, direccion):
        """Mueve a CUBO en la dirección especificada"""
        speed = 5.0

        if direccion == "arriba":
            self.velocity[1] = -speed
        elif direccion == "abajo":
            self.velocity[1] = speed
        elif direccion == "izquierda":
            self.velocity[0] = -speed
        elif direccion == "derecha":
            self.velocity[0] = speed

    def detener(self):
        """Detiene el movimiento de CUBO"""
        self.velocity = np.array([0.0, 0.0])

    def puede_atraer_pieza(self):
        """Verifica si CUBO tiene alguna zona libre para atraer una pieza"""
        return any(not zona["ocupada"] for zona in self.zonas_atraccion.values())

    def atraer_pieza(self, pieza, zona_nombre):
        """Atrae una pieza a una zona específica de CUBO"""
        # Validar que la zona exista
        if zona_nombre not in self.zonas_atraccion:
            return False

        if not self.zonas_atraccion[zona_nombre]["ocupada"]:
            self.zonas_atraccion[zona_nombre]["ocupada"] = True
            self.zonas_atraccion[zona_nombre]["pieza"] = pieza
            self.pieza_sostenida = pieza
            self.zona_pieza = zona_nombre
            self.cambiar_emocion(self.EMOCION_FELIZ, 0.5)
            return True
        return False

    def soltar_pieza(self, zona_nombre=None):
        """Suelta la pieza de una zona específica o de la zona actual"""
        # Si no se especifica zona, usar la zona actual (compatibilidad con código anterior)
        if zona_nombre is None:
            zona_nombre = self.zona_pieza

        # Validar que la zona exista y esté ocupada
        if (
            zona_nombre
            and zona_nombre in self.zonas_atraccion
            and self.zonas_atraccion[zona_nombre]["ocupada"]
        ):

            pieza = self.zonas_atraccion[zona_nombre]["pieza"]
            self.zonas_atraccion[zona_nombre]["ocupada"] = False
            self.zonas_atraccion[zona_nombre]["pieza"] = None

            # Si es la pieza principal sostenida, limpiar referencias
            if self.zona_pieza == zona_nombre:
                self.pieza_sostenida = None
                self.zona_pieza = None

            return pieza
        return None

    def recibir_dano(self):
        """CUBO recibe daño (de meteoro, obstáculo, etc.)"""
        if not self.invulnerable:
            self.cambiar_emocion(self.EMOCION_DOLOR, 1.0)
            self.invulnerable = True
            self.invulnerabilidad_timer = 2.0  # 2 segundos de invulnerabilidad

            # Soltar pieza si la tiene
            pieza_soltada = self.soltar_pieza()

            return pieza_soltada
        return None

    def cambiar_emocion(self, nueva_emocion, duracion=None):
        """Cambia la emoción de CUBO"""
        self.emocion_actual = nueva_emocion
        self.emocion_timer = duracion if duracion else self.emocion_duracion

    def recibir_impacto(self):
        """
        Registra un impacto directo de meteoro

        Returns:
            bool: True si el cubo fue destruido, False si aún puede resistir
        """
        self.impactos_recibidos += 1
        return self.impactos_recibidos >= self.max_impactos

    def esta_destruido(self):
        """
        Verifica si el cubo ha sido destruido

        Returns:
            bool: True si recibió el máximo de impactos
        """
        return self.impactos_recibidos >= self.max_impactos

    def resetear_impactos(self):
        """Resetea el contador de impactos (para reiniciar nivel)"""
        self.impactos_recibidos = 0

    def get_zona_mas_cercana(self, punto):
        """Devuelve la zona de atracción más cercana a un punto dado"""
        # Validar que punto sea válido
        if punto is None or len(punto) < 2:
            return None, float("inf")

        min_dist = float("inf")
        zona_cercana = None

        for nombre, zona in self.zonas_atraccion.items():
            if not zona["ocupada"]:
                try:
                    zona_pos = self.position + np.array(zona["offset"])
                    punto_array = np.array(punto)
                    dist = np.linalg.norm(zona_pos - punto_array)
                    if dist < min_dist:
                        min_dist = dist
                        zona_cercana = nombre
                except (ValueError, TypeError):
                    continue

        return zona_cercana, min_dist

    def update(self, delta_time=0.016):
        """Actualiza el estado de CUBO"""
        # Aplicar velocidad
        self.position += self.velocity

        # Mantener dentro de los límites
        self.position[0] = max(
            self.size / 2, min(SCREEN_WIDTH - self.size / 2, self.position[0])
        )
        self.position[1] = max(
            self.size / 2, min(SCREEN_HEIGHT - self.size / 2, self.position[1])
        )

        # Actualizar animaciones
        self.animation_offset += 0.1
        self.bounce_offset = np.sin(self.animation_offset) * 3

        # Rotación sutil
        if np.linalg.norm(self.velocity) > 0:
            self.rotation_angle += 2

        # Actualizar timers
        if self.emocion_timer > 0:
            self.emocion_timer -= delta_time
            if self.emocion_timer <= 0:
                self.emocion_actual = self.EMOCION_NEUTRAL

        if self.invulnerable:
            self.invulnerabilidad_timer -= delta_time
            if self.invulnerabilidad_timer <= 0:
                self.invulnerable = False

        # Actualizar posición de pieza sostenida
        if self.pieza_sostenida and self.zona_pieza:
            zona = self.zonas_atraccion[self.zona_pieza]
            pieza_pos = self.position + np.array(zona["offset"])
            self.pieza_sostenida.position = pieza_pos

    def draw(self, screen):
        """Dibuja a CUBO en pantalla"""
        x, y = int(self.position[0]), int(self.position[1] + self.bounce_offset)

        # Determinar color según emoción
        color_map = {
            self.EMOCION_NEUTRAL: NEON_CYAN,
            self.EMOCION_FELIZ: NEON_GREEN,
            self.EMOCION_TRISTE: NEON_BLUE,
            self.EMOCION_MIEDO: NEON_PURPLE,
            self.EMOCION_DOLOR: COLOR_DANGER,
            self.EMOCION_DETERMINADO: NEON_YELLOW,
        }

        color = color_map.get(self.emocion_actual, NEON_CYAN)

        # Parpadeo si está invulnerable
        if self.invulnerable and int(self.animation_offset * 10) % 2 == 0:
            alpha = 128
        else:
            alpha = 255

        # Superficie del cubo con transparencia
        cubo_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Dibujar cuerpo principal
        pygame.draw.rect(cubo_surface, (*color, alpha), (0, 0, self.size, self.size))
        pygame.draw.rect(
            cubo_surface, (*NEON_YELLOW, alpha), (0, 0, self.size, self.size), 3
        )

        # Dibujar cara/expresión
        self._dibujar_expresion(cubo_surface, alpha)

        # Dibujar zonas de atracción
        self._dibujar_zonas_atraccion(screen)

        # Blit del cubo
        cubo_rect = cubo_surface.get_rect(center=(x, y))
        screen.blit(cubo_surface, cubo_rect)

        # Efecto de brillo
        for i in range(3):
            glow_surface = pygame.Surface(
                (self.size + i * 4, self.size + i * 4), pygame.SRCALPHA
            )
            glow_color = (*color, int(alpha * 0.2 / (i + 1)))
            pygame.draw.rect(
                glow_surface,
                glow_color,
                (0, 0, self.size + i * 4, self.size + i * 4),
                2,
            )
            glow_rect = glow_surface.get_rect(center=(x, y))
            screen.blit(glow_surface, glow_rect)

    def _dibujar_expresion(self, surface, alpha):
        """Dibuja la expresión facial de CUBO"""
        # Ojos
        ojo_izq_x = self.size * 0.3
        ojo_der_x = self.size * 0.7
        ojo_y = self.size * 0.35
        ojo_size = 6

        # Color de ojos
        ojo_color = (255, 255, 255, alpha)

        if self.emocion_actual == self.EMOCION_MIEDO:
            # Ojos grandes asustados
            pygame.draw.circle(
                surface, ojo_color, (int(ojo_izq_x), int(ojo_y)), ojo_size + 2
            )
            pygame.draw.circle(
                surface, ojo_color, (int(ojo_der_x), int(ojo_y)), ojo_size + 2
            )
        else:
            pygame.draw.circle(
                surface, ojo_color, (int(ojo_izq_x), int(ojo_y)), ojo_size
            )
            pygame.draw.circle(
                surface, ojo_color, (int(ojo_der_x), int(ojo_y)), ojo_size
            )

        # Boca
        boca_y = self.size * 0.65

        if self.emocion_actual == self.EMOCION_FELIZ:
            # Sonrisa
            pygame.draw.arc(
                surface,
                ojo_color,
                (self.size * 0.25, boca_y - 5, self.size * 0.5, 15),
                np.pi,
                2 * np.pi,
                3,
            )
        elif self.emocion_actual == self.EMOCION_TRISTE:
            # Tristeza
            pygame.draw.arc(
                surface,
                ojo_color,
                (self.size * 0.25, boca_y - 10, self.size * 0.5, 15),
                0,
                np.pi,
                3,
            )
        elif self.emocion_actual == self.EMOCION_DOLOR:
            # X en la boca
            pygame.draw.line(
                surface,
                ojo_color,
                (self.size * 0.35, boca_y - 3),
                (self.size * 0.65, boca_y + 3),
                3,
            )
            pygame.draw.line(
                surface,
                ojo_color,
                (self.size * 0.35, boca_y + 3),
                (self.size * 0.65, boca_y - 3),
                3,
            )
        elif self.emocion_actual == self.EMOCION_MIEDO:
            # O pequeña
            pygame.draw.circle(
                surface, ojo_color, (int(self.size * 0.5), int(boca_y)), 5
            )
        elif self.emocion_actual == self.EMOCION_DETERMINADO:
            # Línea recta determinada
            pygame.draw.line(
                surface,
                ojo_color,
                (self.size * 0.3, boca_y),
                (self.size * 0.7, boca_y),
                3,
            )
        else:
            # Neutral: línea pequeña
            pygame.draw.line(
                surface,
                ojo_color,
                (self.size * 0.35, boca_y),
                (self.size * 0.65, boca_y),
                2,
            )

    def _dibujar_zonas_atraccion(self, screen):
        """Dibuja las zonas de atracción de CUBO"""
        for nombre, zona in self.zonas_atraccion.items():
            zona_pos = self.position + np.array(zona["offset"])
            x, y = int(zona_pos[0]), int(zona_pos[1])

            # Color según estado
            if zona["ocupada"]:
                color = NEON_GREEN
                size = 8
            else:
                color = NEON_PURPLE
                size = 6

            # Dibujar zona
            alpha = int(128 + 127 * np.sin(self.animation_offset * 2))
            zona_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(zona_surface, (*color, alpha), (size, size), size)
            pygame.draw.circle(zona_surface, color, (size, size), size, 2)

            zona_rect = zona_surface.get_rect(center=(x, y))
            screen.blit(zona_surface, zona_rect)

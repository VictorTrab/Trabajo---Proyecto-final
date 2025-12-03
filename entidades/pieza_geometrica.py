"""
Sistema de piezas geométricas para CUBO: Arquitecto del Caos
Piezas que pueden ser recogidas, transportadas y ensambladas
"""

import pygame
import math
from config.constantes import *


class PiezaGeometrica:
    """Representa una pieza geométrica que puede ser recogida y ensamblada"""

    # Tipos de piezas disponibles
    CUADRADO = "cuadrado"
    TRIANGULO = "triangulo"
    CIRCULO = "circulo"
    ROMBO = "rombo"
    RECTANGULO = "rectangulo"

    # Tamaño base de las piezas
    TAMANO_BASE = 40

    # Colores por tipo de pieza
    COLORES = {
        CUADRADO: (100, 200, 255),  # Azul claro
        TRIANGULO: (255, 150, 100),  # Naranja
        CIRCULO: (150, 255, 150),  # Verde claro
        ROMBO: (255, 200, 100),  # Amarillo
        RECTANGULO: (200, 150, 255),  # Púrpura
    }

    def __init__(self, x, y, tipo, grid_size=40):
        """
        Inicializa una pieza geométrica

        Args:
            x, y: Posición inicial
            tipo: Tipo de pieza (CUADRADO, TRIANGULO, etc.)
            grid_size: Tamaño de la cuadrícula para snap
        """
        self.x = x
        self.y = y
        self.tipo = tipo
        self.grid_size = grid_size

        # Posición en la grilla (para snap-to-grid)
        self.grid_x = x // grid_size
        self.grid_y = y // grid_size

        # Estado de la pieza
        self.siendo_arrastrada = False
        self.colocada = False  # Si está colocada en una zona de atracción
        self.zona_asignada = None  # Zona de atracción donde está colocada

        # Propiedades visuales
        self.color = self.COLORES.get(tipo, (200, 200, 200))
        self.color_outline = tuple(max(0, c - 50) for c in self.color)
        self.tamano = self.TAMANO_BASE

        # Animación
        self.angulo_rotacion = 0
        self.escala_pulso = 1.0
        self.tiempo_pulso = 0
        self.brillo_colocada = 0  # Brillo cuando se coloca correctamente
        self.tiempo_brillo = 0
        self.offset_flotante = 0  # Para efecto de flotación
        self.tiempo_flotante = 0

        # Física
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.friccion = 0.9

        # Área de colisión (rect para detección)
        self.actualizar_rect()

    def actualizar_rect(self):
        """Actualiza el rectángulo de colisión"""
        self.rect = pygame.Rect(
            self.x - self.tamano // 2,
            self.y - self.tamano // 2,
            self.tamano,
            self.tamano,
        )

    def snap_to_grid(self):
        """Ajusta la posición a la grilla más cercana"""
        self.grid_x = round(self.x / self.grid_size)
        self.grid_y = round(self.y / self.grid_size)
        self.x = self.grid_x * self.grid_size
        self.y = self.grid_y * self.grid_size
        self.actualizar_rect()

    def mover_a(self, x, y):
        """Mueve la pieza a una posición específica"""
        self.x = x
        self.y = y
        self.actualizar_rect()

    def aplicar_velocidad(self, vx, vy):
        """Aplica velocidad a la pieza"""
        self.velocidad_x = vx
        self.velocidad_y = vy

    def update(self, dt):
        """Actualiza el estado de la pieza"""
        # Animación de pulso si está siendo arrastrada
        if self.siendo_arrastrada:
            self.tiempo_pulso += dt * 5
            self.escala_pulso = 1.0 + math.sin(self.tiempo_pulso) * 0.15
            # Rotación suave mientras se arrastra
            self.angulo_rotacion += dt * 3
        else:
            self.escala_pulso = 1.0
            self.tiempo_pulso = 0
            self.angulo_rotacion *= 0.9  # Desacelerar rotación gradualmente

        # Efecto de brillo cuando se coloca correctamente
        if self.colocada:
            self.tiempo_brillo += dt * 4
            self.brillo_colocada = abs(math.sin(self.tiempo_brillo)) * 50
            # Efecto de flotación sutil
            self.tiempo_flotante += dt * 2
            self.offset_flotante = math.sin(self.tiempo_flotante) * 3
        else:
            self.brillo_colocada = 0
            self.tiempo_brillo = 0
            self.offset_flotante = 0
            self.tiempo_flotante = 0

            # Física simple si no está siendo arrastrada
        if not self.siendo_arrastrada and not self.colocada:
            # Validar valores numéricos antes de operar
            if isinstance(self.velocidad_x, (int, float)) and isinstance(
                self.velocidad_y, (int, float)
            ):
                self.x += self.velocidad_x
                self.y += self.velocidad_y
                self.velocidad_x *= self.friccion
                self.velocidad_y *= self.friccion

                # Límites de pantalla con validación de tamaño
                mitad_tamano = max(1, self.tamano // 2)

                if self.x < mitad_tamano:
                    self.x = mitad_tamano
                    self.velocidad_x *= -0.5
                elif self.x > SCREEN_WIDTH - mitad_tamano:
                    self.x = SCREEN_WIDTH - mitad_tamano
                    self.velocidad_x *= -0.5

                if self.y < mitad_tamano:
                    self.y = mitad_tamano
                    self.velocidad_y *= -0.5
                elif self.y > SCREEN_HEIGHT - mitad_tamano:
                    self.y = SCREEN_HEIGHT - mitad_tamano
                    self.velocidad_y *= -0.5

                self.actualizar_rect()

    def draw(self, screen):
        """Dibuja la pieza en pantalla"""
        tamano_actual = int(self.tamano * self.escala_pulso)

        # Posición con efecto de flotación si está colocada
        pos_y = int(self.y + self.offset_flotante)
        pos_x = int(self.x)

        # Dibujar halo/glow si está siendo arrastrada o colocada
        if self.siendo_arrastrada or self.colocada:
            glow_color = (
                (255, 255, 255, 40)
                if self.siendo_arrastrada
                else (0, 255, 0, int(50 + self.brillo_colocada))
            )
            glow_radius = tamano_actual + 10
            glow_surface = pygame.Surface(
                (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow_surface, glow_color, (glow_radius, glow_radius), glow_radius
            )
            screen.blit(glow_surface, (pos_x - glow_radius, pos_y - glow_radius))

        # Crear superficie para la pieza con transparencia
        superficie = pygame.Surface(
            (tamano_actual * 2, tamano_actual * 2), pygame.SRCALPHA
        )

        # Color con brillo si está colocada
        color_pieza = self.color
        if self.colocada:
            color_pieza = tuple(
                min(255, c + int(self.brillo_colocada)) for c in self.color
            )

        if self.tipo == self.CUADRADO:
            self._dibujar_cuadrado(superficie, tamano_actual, color_pieza)
        elif self.tipo == self.TRIANGULO:
            self._dibujar_triangulo(superficie, tamano_actual, color_pieza)
        elif self.tipo == self.CIRCULO:
            self._dibujar_circulo(superficie, tamano_actual, color_pieza)
        elif self.tipo == self.ROMBO:
            self._dibujar_rombo(superficie, tamano_actual, color_pieza)
        elif self.tipo == self.RECTANGULO:
            self._dibujar_rectangulo(superficie, tamano_actual, color_pieza)

        # Rotar si está siendo arrastrada
        if self.siendo_arrastrada or abs(self.angulo_rotacion) > 0.01:
            superficie = pygame.transform.rotate(
                superficie, math.degrees(self.angulo_rotacion)
            )

        # Dibujar en pantalla
        rect_superficie = superficie.get_rect(center=(pos_x, pos_y))
        screen.blit(superficie, rect_superficie)

        # Indicador visual si está colocada correctamente
        if self.colocada:
            # Círculo pulsante verde
            radio_check = 8 + int(math.sin(self.tiempo_brillo) * 2)
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (pos_x, pos_y - tamano_actual // 2 - 15),
                radio_check,
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (pos_x, pos_y - tamano_actual // 2 - 15),
                radio_check,
                2,
            )
            # Checkmark
            check_points = [
                (pos_x - 3, pos_y - tamano_actual // 2 - 15),
                (pos_x - 1, pos_y - tamano_actual // 2 - 12),
                (pos_x + 4, pos_y - tamano_actual // 2 - 18),
            ]
            pygame.draw.lines(screen, (255, 255, 255), False, check_points, 2)

    def _dibujar_cuadrado(self, superficie, tamano, color=None):
        """Dibuja un cuadrado"""
        if color is None:
            color = self.color
        centro = tamano
        puntos = [
            (centro - tamano // 2, centro - tamano // 2),
            (centro + tamano // 2, centro - tamano // 2),
            (centro + tamano // 2, centro + tamano // 2),
            (centro - tamano // 2, centro + tamano // 2),
        ]
        pygame.draw.polygon(superficie, color, puntos)
        pygame.draw.polygon(superficie, self.color_outline, puntos, 3)

    def _dibujar_triangulo(self, superficie, tamano, color=None):
        """Dibuja un triángulo equilátero"""
        if color is None:
            color = self.color
        centro = tamano
        altura = tamano * 0.866  # altura de triángulo equilátero
        puntos = [
            (centro, centro - altura * 0.66),
            (centro - tamano // 2, centro + altura * 0.33),
            (centro + tamano // 2, centro + altura * 0.33),
        ]
        pygame.draw.polygon(superficie, color, puntos)
        pygame.draw.polygon(superficie, self.color_outline, puntos, 3)

    def _dibujar_circulo(self, superficie, tamano, color=None):
        """Dibuja un círculo"""
        if color is None:
            color = self.color
        centro = tamano
        pygame.draw.circle(superficie, color, (centro, centro), tamano // 2)
        pygame.draw.circle(
            superficie, self.color_outline, (centro, centro), tamano // 2, 3
        )

    def _dibujar_rombo(self, superficie, tamano, color=None):
        """Dibuja un rombo"""
        if color is None:
            color = self.color
        centro = tamano
        puntos = [
            (centro, centro - tamano // 2),
            (centro + tamano // 2, centro),
            (centro, centro + tamano // 2),
            (centro - tamano // 2, centro),
        ]
        pygame.draw.polygon(superficie, color, puntos)
        pygame.draw.polygon(superficie, self.color_outline, puntos, 3)

    def _dibujar_rectangulo(self, superficie, tamano, color=None):
        """Dibuja un rectángulo"""
        if color is None:
            color = self.color
        centro = tamano
        ancho = tamano
        alto = tamano // 2
        puntos = [
            (centro - ancho // 2, centro - alto // 2),
            (centro + ancho // 2, centro - alto // 2),
            (centro + ancho // 2, centro + alto // 2),
            (centro - ancho // 2, centro + alto // 2),
        ]
        pygame.draw.polygon(superficie, color, puntos)
        pygame.draw.polygon(superficie, self.color_outline, puntos, 3)

    def contiene_punto(self, x, y):
        """Verifica si un punto está dentro de la pieza"""
        return self.rect.collidepoint(x, y)

    def distancia_a(self, x, y):
        """Calcula la distancia al punto dado"""
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(dx * dx + dy * dy)


class FiguraObjetivo:
    """Representa la figura objetivo que debe construirse"""

    def __init__(self, x, y, definicion):
        """
        Inicializa una figura objetivo

        Args:
            x, y: Posición central de la figura
            definicion: Lista de diccionarios con estructura:
                [
                    {"tipo": "cuadrado", "posicion": "arriba"},
                    {"tipo": "triangulo", "posicion": "derecha"},
                    ...
                ]
        """
        self.x = x
        self.y = y
        self.definicion = definicion

        # Espaciado entre piezas (reducido para que se vean más unidas)
        self.espaciado = PiezaGeometrica.TAMANO_BASE - 5

        # Mapa de posiciones relativas
        self.posiciones = {
            "arriba": (0, -self.espaciado),
            "abajo": (0, self.espaciado),
            "izquierda": (-self.espaciado, 0),
            "derecha": (self.espaciado, 0),
            "centro": (0, 0),
        }

        # Crear lista de piezas esperadas
        self.piezas_esperadas = []
        for pieza_def in definicion:
            tipo = pieza_def["tipo"]
            posicion = pieza_def["posicion"]
            offset_x, offset_y = self.posiciones[posicion]
            self.piezas_esperadas.append(
                {
                    "tipo": tipo,
                    "x": self.x + offset_x,
                    "y": self.y + offset_y,
                    "posicion": posicion,
                }
            )

    def draw(self, screen, alpha=100):
        """Dibuja la figura objetivo como silueta semitransparente"""
        # Dibujar cada pieza esperada como silueta
        for pieza_esperada in self.piezas_esperadas:
            tipo = pieza_esperada["tipo"]
            px = pieza_esperada["x"]
            py = pieza_esperada["y"]

            # Color semitransparente
            color_base = PiezaGeometrica.COLORES.get(tipo, (200, 200, 200))
            color = (*color_base, alpha)

            # Crear superficie temporal
            superficie = pygame.Surface(
                (PiezaGeometrica.TAMANO_BASE * 2, PiezaGeometrica.TAMANO_BASE * 2),
                pygame.SRCALPHA,
            )

            # Dibujar según tipo
            centro = PiezaGeometrica.TAMANO_BASE
            tamano = PiezaGeometrica.TAMANO_BASE

            if tipo == PiezaGeometrica.CUADRADO:
                puntos = [
                    (centro - tamano // 2, centro - tamano // 2),
                    (centro + tamano // 2, centro - tamano // 2),
                    (centro + tamano // 2, centro + tamano // 2),
                    (centro - tamano // 2, centro + tamano // 2),
                ]
                pygame.draw.polygon(superficie, color, puntos)
                pygame.draw.polygon(superficie, (*color_base, 255), puntos, 2)

            elif tipo == PiezaGeometrica.TRIANGULO:
                altura = tamano * 0.866
                puntos = [
                    (centro, centro - altura * 0.66),
                    (centro - tamano // 2, centro + altura * 0.33),
                    (centro + tamano // 2, centro + altura * 0.33),
                ]
                pygame.draw.polygon(superficie, color, puntos)
                pygame.draw.polygon(superficie, (*color_base, 255), puntos, 2)

            elif tipo == PiezaGeometrica.CIRCULO:
                pygame.draw.circle(superficie, color, (centro, centro), tamano // 2)
                pygame.draw.circle(
                    superficie, (*color_base, 255), (centro, centro), tamano // 2, 2
                )

            elif tipo == PiezaGeometrica.ROMBO:
                puntos = [
                    (centro, centro - tamano // 2),
                    (centro + tamano // 2, centro),
                    (centro, centro + tamano // 2),
                    (centro - tamano // 2, centro),
                ]
                pygame.draw.polygon(superficie, color, puntos)
                pygame.draw.polygon(superficie, (*color_base, 255), puntos, 2)

            elif tipo == PiezaGeometrica.RECTANGULO:
                ancho = tamano
                alto = tamano // 2
                puntos = [
                    (centro - ancho // 2, centro - alto // 2),
                    (centro + ancho // 2, centro - alto // 2),
                    (centro + ancho // 2, centro + alto // 2),
                    (centro - ancho // 2, centro + alto // 2),
                ]
                pygame.draw.polygon(superficie, color, puntos)
                pygame.draw.polygon(superficie, (*color_base, 255), puntos, 2)

            # Dibujar en pantalla
            rect = superficie.get_rect(center=(int(px), int(py)))
            screen.blit(superficie, rect)

    def verificar_completitud(self, piezas_colocadas):
        """
        Verifica si las piezas colocadas coinciden con el objetivo

        Args:
            piezas_colocadas: Lista de piezas que están en zonas de atracción

        Returns:
            (bool, float): (¿está completa?, porcentaje de completitud)
        """
        if not piezas_colocadas:
            return False, 0.0

        total_esperadas = len(self.piezas_esperadas)
        coincidencias = 0

        for pieza_esperada in self.piezas_esperadas:
            for pieza in piezas_colocadas:
                # Verificar tipo y proximidad
                if pieza.tipo == pieza_esperada["tipo"]:
                    distancia = pieza.distancia_a(
                        pieza_esperada["x"], pieza_esperada["y"]
                    )
                    if distancia < 30:  # Tolerancia de 30 píxeles
                        coincidencias += 1
                        break

        porcentaje = (coincidencias / total_esperadas) * 100
        completa = coincidencias == total_esperadas

        return completa, porcentaje

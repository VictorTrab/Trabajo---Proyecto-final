"""
Sistema de Portales - Fase 4
Portales de teletransportación
"""

import pygame
import random
import math
import time
from config.constantes import *


class Portal:
    """Clase para un portal individual"""

    def __init__(self, x, y, tipo="entrada", color=NEON_CYAN):
        """
        Inicializa un portal

        Args:
            x: Posición X
            y: Posición Y
            tipo: "entrada" o "salida"
            color: Color del portal
        """
        self.x = x
        self.y = y
        self.tipo = tipo
        self.color = color
        self.radio = 40

        # Portal pareado
        self.portal_destino = None

        # Efectos visuales
        self.rotacion = 0
        self.pulso = 0
        self.particulas_orbita = []

        # Cooldown para evitar teletransportaciones infinitas
        self.cooldown = 0
        self.cooldown_duracion = 1.0  # 1 segundo
        self.objetos_en_cooldown = set()  # IDs de objetos

        # Animación
        self.tiempo_animacion = 0

    def vincular_con(self, otro_portal):
        """Vincula este portal con otro portal"""
        self.portal_destino = otro_portal
        otro_portal.portal_destino = self

    def update(self, dt):
        """Actualiza el portal"""
        self.rotacion += 180 * dt  # Rotar 180 grados por segundo
        if self.rotacion >= 360:
            self.rotacion -= 360

        self.pulso = abs(math.sin(time.time() * 3)) * 10
        self.tiempo_animacion += dt

        # Actualizar cooldown
        if self.cooldown > 0:
            self.cooldown -= dt
            if self.cooldown <= 0:
                self.objetos_en_cooldown.clear()

    def draw(self, screen):
        """Dibuja el portal"""
        # Anillos exteriores giratorios
        num_anillos = 3
        for i in range(num_anillos):
            radio_anillo = self.radio + i * 12 + self.pulso
            grosor = 3 - i
            alpha = max(0, min(255, 150 - i * 40))  # Clamping para evitar overflow

            # Crear superficie con alpha
            anillo_surf = pygame.Surface(
                (radio_anillo * 2, radio_anillo * 2), pygame.SRCALPHA
            )

            # Color con transparencia
            color_anillo = (*self.color[:3], alpha)

            # Dibujar anillo rotado
            pygame.draw.circle(
                anillo_surf,
                color_anillo,
                (radio_anillo, radio_anillo),
                radio_anillo,
                grosor,
            )

            screen.blit(anillo_surf, (self.x - radio_anillo, self.y - radio_anillo))

        # Núcleo central con vórtice
        num_rayos = 8
        for i in range(num_rayos):
            angulo = (i / num_rayos) * 2 * math.pi + math.radians(self.rotacion)

            # Punto inicial (cerca del centro)
            x1 = self.x + math.cos(angulo) * 10
            y1 = self.y + math.sin(angulo) * 10

            # Punto final (en el borde)
            x2 = self.x + math.cos(angulo) * self.radio
            y2 = self.y + math.sin(angulo) * self.radio

            pygame.draw.line(screen, self.color, (x1, y1), (x2, y2), 2)

        # Centro brillante
        centro_radio = int(15 + self.pulso // 2)
        pygame.draw.circle(
            screen, (255, 255, 255), (int(self.x), int(self.y)), centro_radio
        )
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), centro_radio, 2
        )

        # Etiqueta de tipo
        font = pygame.font.Font(None, 20)
        texto = font.render(
            "↑" if self.tipo == "entrada" else "↓", True, (255, 255, 255)
        )
        screen.blit(texto, (self.x - 5, self.y - 10))

    def puede_teletransportar(self, objeto):
        """
        Verifica si un objeto puede ser teletransportado

        Args:
            objeto: Objeto a verificar

        Returns:
            bool: True si puede teletransportarse
        """
        if not self.portal_destino:
            return False

        if self.cooldown > 0:
            objeto_id = id(objeto)
            if objeto_id in self.objetos_en_cooldown:
                return False

        return True

    def teletransportar(self, objeto):
        """
        Teletransporta un objeto al portal destino

        Args:
            objeto: Objeto con atributos x, y

        Returns:
            bool: True si la teletransportación fue exitosa
        """
        if not self.puede_teletransportar(objeto):
            return False

        # Mover objeto al destino
        objeto.x = self.portal_destino.x
        objeto.y = self.portal_destino.y

        # Activar cooldown en ambos portales
        self.cooldown = self.cooldown_duracion
        self.portal_destino.cooldown = self.cooldown_duracion

        # Agregar objeto a cooldown
        objeto_id = id(objeto)
        self.objetos_en_cooldown.add(objeto_id)
        self.portal_destino.objetos_en_cooldown.add(objeto_id)

        return True

    def esta_dentro(self, objeto):
        """
        Verifica si un objeto está dentro del portal

        Args:
            objeto: Objeto con atributos x, y

        Returns:
            bool: True si está dentro
        """
        dx = self.x - objeto.x
        dy = self.y - objeto.y
        distancia = math.sqrt(dx * dx + dy * dy)

        return distancia < self.radio


class SistemaPortales:
    """Gestiona múltiples pares de portales"""

    def __init__(self, num_pares=2):
        """
        Inicializa el sistema de portales

        Args:
            num_pares: Número de pares de portales a crear
        """
        self.pares_portales = []
        self.colores_disponibles = [
            NEON_CYAN,
            NEON_PURPLE,
            NEON_GREEN,
            NEON_PINK,
            NEON_YELLOW,
        ]

        # Generar pares de portales
        for i in range(num_pares):
            color = self.colores_disponibles[i % len(self.colores_disponibles)]
            entrada, salida = self._crear_par_portal(color)
            self.pares_portales.append((entrada, salida))

    def _crear_par_portal(self, color):
        """
        Crea un par de portales vinculados

        Args:
            color: Color para ambos portales

        Returns:
            tuple: (portal_entrada, portal_salida)
        """
        # Generar posiciones aleatorias que no estén muy cerca ni muy lejos
        margen = 100
        intentos = 0
        max_intentos = 50

        while intentos < max_intentos:
            x1 = random.randint(margen, SCREEN_WIDTH - margen)
            y1 = random.randint(margen, SCREEN_HEIGHT - margen)

            x2 = random.randint(margen, SCREEN_WIDTH - margen)
            y2 = random.randint(margen, SCREEN_HEIGHT - margen)

            # Verificar distancia mínima y máxima
            dx = x2 - x1
            dy = y2 - y1
            distancia = math.sqrt(dx * dx + dy * dy)

            if 200 < distancia < 600:  # Distancia óptima
                # Verificar que no estén muy cerca de otros portales
                muy_cerca = False
                for entrada, salida in self.pares_portales:
                    if self._distancia_entre_puntos(x1, y1, entrada.x, entrada.y) < 150:
                        muy_cerca = True
                        break
                    if self._distancia_entre_puntos(x2, y2, salida.x, salida.y) < 150:
                        muy_cerca = True
                        break

                if not muy_cerca:
                    break

            intentos += 1

        # Crear portales
        entrada = Portal(x1, y1, "entrada", color)
        salida = Portal(x2, y2, "salida", color)

        # Vincularlos
        entrada.vincular_con(salida)

        return entrada, salida

    def _distancia_entre_puntos(self, x1, y1, x2, y2):
        """Calcula distancia entre dos puntos"""
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)

    def update(self, dt):
        """Actualiza todos los portales"""
        for entrada, salida in self.pares_portales:
            entrada.update(dt)
            salida.update(dt)

    def draw(self, screen):
        """Dibuja todos los portales"""
        for entrada, salida in self.pares_portales:
            # Dibujar línea de conexión sutil
            self._dibujar_conexion(screen, entrada, salida)
            entrada.draw(screen)
            salida.draw(screen)

    def _dibujar_conexion(self, screen, portal1, portal2):
        """Dibuja una línea de conexión entre portales pareados"""
        # Línea punteada sutil
        pulso = abs(math.sin(time.time() * 2)) * 50 + 50
        color_conexion = (*portal1.color[:3], int(pulso))

        # Crear superficie para la línea con alpha
        superficie = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Dibujar línea punteada
        dx = portal2.x - portal1.x
        dy = portal2.y - portal1.y
        distancia = math.sqrt(dx * dx + dy * dy)
        num_puntos = int(distancia // 20)

        for i in range(num_puntos):
            if i % 2 == 0:  # Solo puntos pares (efecto punteado)
                t = i / num_puntos
                x = portal1.x + dx * t
                y = portal1.y + dy * t
                pygame.draw.circle(superficie, color_conexion, (int(x), int(y)), 2)

        screen.blit(superficie, (0, 0))

    def verificar_teletransportaciones(self, objetos):
        """
        Verifica y ejecuta teletransportaciones de objetos

        Args:
            objetos: Lista de objetos a verificar

        Returns:
            list: Lista de tuplas (objeto, portal_entrada, portal_salida) teletransportados
        """
        teletransportados = []

        for entrada, salida in self.pares_portales:
            for portal in [entrada, salida]:
                for objeto in objetos:
                    if portal.esta_dentro(objeto) and portal.puede_teletransportar(
                        objeto
                    ):
                        if portal.teletransportar(objeto):
                            teletransportados.append(
                                (objeto, portal, portal.portal_destino)
                            )

        return teletransportados

    def limpiar(self):
        """Elimina todos los portales"""
        self.pares_portales.clear()

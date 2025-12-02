"""
Sistema de Meteoros - Fase 4
Obstáculos dinámicos que caen desde el cielo
"""

import pygame
import random
import math
from config.constantes import *


class Meteoro:
    """Clase para meteoros que caen como obstáculos"""

    def __init__(self, x, y, velocidad=200, tamano=30):
        """
        Inicializa un meteoro

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            velocidad: Velocidad de caída (píxeles por segundo)
            tamano: Tamaño del meteoro
        """
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.tamano = tamano
        self.radio = tamano // 2

        # Estado
        self.activo = True
        self.impactado = False

        # Efectos visuales
        self.rotacion = random.uniform(0, 360)
        self.velocidad_rotacion = random.uniform(180, 360)  # grados por segundo
        self.trail_particles = []  # Estela de partículas

        # Advertencia visual
        self.advertencia_activa = True
        self.advertencia_timer = 1.0  # 1 segundo de advertencia

        # Animación de impacto
        self.explosion_timer = 0
        self.explosion_duration = 0.5  # Duración de la explosión

        # Color dinámico (rojo ardiente)
        self.color_base = NEON_ORANGE
        self.color_brillo = (255, 100, 0)

    def update(self, dt):
        """Actualiza el estado del meteoro"""
        if not self.activo:
            return

        # Actualizar advertencia
        if self.advertencia_activa:
            self.advertencia_timer -= dt
            if self.advertencia_timer <= 0:
                self.advertencia_activa = False

        # Si está en advertencia, no moverse aún
        if self.advertencia_activa:
            return

        # Mover hacia abajo
        self.y += self.velocidad * dt

        # Rotar
        self.rotacion += self.velocidad_rotacion * dt
        if self.rotacion >= 360:
            self.rotacion -= 360

        # Actualizar explosión si impactó
        if self.impactado:
            self.explosion_timer += dt
            if self.explosion_timer >= self.explosion_duration:
                self.activo = False

        # Desactivar si sale de la pantalla
        if self.y > SCREEN_HEIGHT + 50:
            self.activo = False

    def draw(self, screen):
        """Dibuja el meteoro"""
        if not self.activo:
            return

        # Dibujar advertencia
        if self.advertencia_activa:
            self._dibujar_advertencia(screen)
            return

        # Dibujar explosión si impactó
        if self.impactado:
            self._dibujar_explosion(screen)
            return

        # Dibujar estela
        self._dibujar_estela(screen)

        # Cuerpo principal del meteoro
        # Crear superficie con alpha para efectos
        superficie = pygame.Surface((self.tamano * 2, self.tamano * 2), pygame.SRCALPHA)

        # Núcleo brillante
        pygame.draw.circle(
            superficie, self.color_brillo, (self.tamano, self.tamano), self.radio // 2
        )

        # Cuerpo exterior con forma irregular (simulando roca)
        puntos = []
        num_puntos = 8
        for i in range(num_puntos):
            angulo = (i / num_puntos) * 2 * math.pi + math.radians(self.rotacion)
            # Variación aleatoria en el radio para forma irregular
            variacion = random.uniform(0.7, 1.0)
            r = self.radio * variacion
            px = self.tamano + r * math.cos(angulo)
            py = self.tamano + r * math.sin(angulo)
            puntos.append((px, py))

        if len(puntos) >= 3:
            pygame.draw.polygon(superficie, self.color_base, puntos)
            pygame.draw.polygon(superficie, (150, 50, 0), puntos, 2)  # Contorno

        # Blit con efecto de brillo
        screen.blit(superficie, (self.x - self.tamano, self.y - self.tamano))

        # Efecto de glow exterior
        for i in range(3):
            radio_glow = self.radio + (3 - i) * 5
            alpha = 30 - i * 10
            glow_surf = pygame.Surface(
                (radio_glow * 2, radio_glow * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow_surf,
                (*self.color_base[:3], alpha),
                (radio_glow, radio_glow),
                radio_glow,
            )
            screen.blit(glow_surf, (self.x - radio_glow, self.y - radio_glow))

    def _dibujar_advertencia(self, screen):
        """Dibuja la advertencia visual antes de que caiga el meteoro"""
        # Pulso visual
        pulso = abs(math.sin(self.advertencia_timer * 10)) * 20 + 10

        # Línea vertical de advertencia
        pygame.draw.line(
            screen,
            (255, 255, 0, 150),
            (self.x, 0),
            (self.x, SCREEN_HEIGHT),
            int(pulso // 2),
        )

        # Zona de impacto
        zona_radio = self.tamano + pulso
        pygame.draw.circle(
            screen, (255, 255, 0), (int(self.x), SCREEN_HEIGHT - 50), int(zona_radio), 3
        )

        # Símbolo de peligro en la parte superior
        font = pygame.font.Font(None, 40)
        texto = font.render("⚠", True, (255, 255, 0))
        screen.blit(texto, (self.x - 10, 20))

    def _dibujar_estela(self, screen):
        """Dibuja la estela de fuego detrás del meteoro"""
        # Efecto de estela simple
        for i in range(5):
            offset_y = -i * 15
            alpha = 200 - i * 40
            radio = self.radio - i * 3

            if radio > 0 and alpha > 0:
                estela_surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
                color_estela = (*self.color_brillo[:3], alpha)
                pygame.draw.circle(estela_surf, color_estela, (radio, radio), radio)
                screen.blit(estela_surf, (self.x - radio, self.y + offset_y - radio))

    def _dibujar_explosion(self, screen):
        """Dibuja la animación de explosión al impactar"""
        progreso = self.explosion_timer / self.explosion_duration

        # Radio creciente
        radio_explosion = int(self.tamano * (1 + progreso * 3))

        # Alpha decreciente
        alpha = int(255 * (1 - progreso))

        # Anillos de explosión
        for i in range(3):
            radio = radio_explosion - i * 10
            if radio > 0:
                explosion_surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
                # Asegurar que alpha esté en rango válido [0, 255]
                alpha_anillo = max(0, min(255, alpha - i * 50))
                color = (*NEON_ORANGE[:3], alpha_anillo)
                pygame.draw.circle(explosion_surf, color, (radio, radio), radio, 5)
                screen.blit(explosion_surf, (self.x - radio, self.y - radio))

        # Núcleo brillante
        nucleo_radio = int(self.radio * (1.5 - progreso))
        if nucleo_radio > 0:
            pygame.draw.circle(
                screen, (255, 255, 255), (int(self.x), int(self.y)), nucleo_radio
            )

    def colisiona_con(self, objeto):
        """
        Verifica colisión con otro objeto (CUBO o pieza)

        Args:
            objeto: Objeto con atributos x, y y (radio o tamano)

        Returns:
            bool: True si hay colisión
        """
        if not self.activo or self.advertencia_activa or self.impactado:
            return False

        # Obtener radio del objeto
        if hasattr(objeto, "radio"):
            radio_obj = objeto.radio
        elif hasattr(objeto, "tamano"):
            radio_obj = objeto.tamano // 2
        else:
            radio_obj = 20  # Radio por defecto

        # Distancia entre centros
        dx = self.x - objeto.x
        dy = self.y - objeto.y
        distancia = math.sqrt(dx * dx + dy * dy)

        # Verificar si hay colisión
        return distancia < (self.radio + radio_obj)

    def impactar(self):
        """Marca el meteoro como impactado e inicia animación de explosión"""
        if not self.impactado:
            self.impactado = True
            self.explosion_timer = 0


class GeneradorMeteoros:
    """Genera meteoros periódicamente"""

    def __init__(self):
        """Inicializa el generador de meteoros"""
        self.meteoros = []
        self.posiciones_prohibidas = []  # Lista de (x, y, radio) para evitar

        # Configurar frecuencia
        self.intervalo_min = 5.0  # segundos
        self.intervalo_max = 8.0
        self.velocidad_min = 200
        self.velocidad_max = 300

        self.tiempo_siguiente = random.uniform(self.intervalo_min, self.intervalo_max)
        self.tiempo_acumulado = 0

    def establecer_zonas_prohibidas(self, posiciones):
        """
        Establece zonas donde no deben aparecer meteoros (ej: sobre portales)

        Args:
            posiciones: Lista de tuplas (x, y, radio) que definen zonas a evitar
        """
        self.posiciones_prohibidas = posiciones

    def update(self, dt):
        """Actualiza el generador y crea nuevos meteoros"""
        self.tiempo_acumulado += dt

        # Generar nuevo meteoro si es tiempo
        if self.tiempo_acumulado >= self.tiempo_siguiente:
            self._generar_meteoro()
            self.tiempo_acumulado = 0
            self.tiempo_siguiente = random.uniform(
                self.intervalo_min, self.intervalo_max
            )

        # Actualizar meteoros existentes
        for meteoro in self.meteoros[:]:
            meteoro.update(dt)
            if not meteoro.activo:
                self.meteoros.remove(meteoro)

    def _generar_meteoro(self):
        """Genera un nuevo meteoro en posición aleatoria, evitando zonas prohibidas"""
        intentos = 0
        max_intentos = 50

        while intentos < max_intentos:
            x = random.randint(50, SCREEN_WIDTH - 50)

            # Verificar si está en zona prohibida
            posicion_valida = True
            for px, py, radio in self.posiciones_prohibidas:
                # Verificar distancia horizontal (ya que el meteoro cae desde arriba)
                distancia = abs(x - px)
                if distancia < radio:
                    posicion_valida = False
                    break

            if posicion_valida:
                break

            intentos += 1

        # Si no se encontró posición válida después de intentos, usar una aleatoria
        if intentos >= max_intentos:
            x = random.randint(50, SCREEN_WIDTH - 50)

        y = -50  # Fuera de la pantalla arriba
        velocidad = random.uniform(self.velocidad_min, self.velocidad_max)
        tamano = random.randint(25, 40)

        meteoro = Meteoro(x, y, velocidad, tamano)
        self.meteoros.append(meteoro)

    def draw(self, screen):
        """Dibuja todos los meteoros"""
        for meteoro in self.meteoros:
            meteoro.draw(screen)

    def verificar_colisiones(self, objetos):
        """
        Verifica colisiones entre meteoros y objetos

        Args:
            objetos: Lista de objetos para verificar colisiones

        Returns:
            list: Lista de tuplas (meteoro, objeto) que colisionaron
        """
        colisiones = []

        for meteoro in self.meteoros:
            for objeto in objetos:
                if meteoro.colisiona_con(objeto):
                    meteoro.impactar()
                    colisiones.append((meteoro, objeto))

        return colisiones

    def limpiar(self):
        """Elimina todos los meteoros"""
        self.meteoros.clear()

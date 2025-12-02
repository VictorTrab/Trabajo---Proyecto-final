"""
Sistema de Power-ups - Fase 4
Potenciadores temporales que mejoran las habilidades de CUBO
"""

import pygame
import random
import math
import time
from config.constantes import *


class PowerUp:
    """Clase base para power-ups"""

    TIPO_ESCUDO = "escudo"
    TIPO_VELOCIDAD = "velocidad"
    TIPO_MAGNETISMO = "magnetismo"

    def __init__(self, x, y, tipo):
        """
        Inicializa un power-up

        Args:
            x: Posición X
            y: Posición Y
            tipo: Tipo de power-up (escudo, velocidad, magnetismo)
        """
        self.x = x
        self.y = y
        self.tipo = tipo
        self.tamano = 30
        self.radio = self.tamano // 2

        # Estado
        self.activo = True
        self.recogido = False

        # Efectos visuales
        self.rotacion = 0
        self.pulso = 0
        self.tiempo_vida = 15.0  # Desaparece después de 15 segundos
        self.tiempo_transcurrido = 0

        # Configuración por tipo
        self._configurar_por_tipo()

    def _configurar_por_tipo(self):
        """Configura color y símbolo según el tipo"""
        if self.tipo == self.TIPO_ESCUDO:
            self.color = NEON_CYAN
            self.simbolo = "🛡"
            self.duracion_efecto = 8.0  # 8 segundos de escudo
        elif self.tipo == self.TIPO_VELOCIDAD:
            self.color = NEON_YELLOW
            self.simbolo = "⚡"
            self.duracion_efecto = 6.0  # 6 segundos de velocidad
        elif self.tipo == self.TIPO_MAGNETISMO:
            self.color = NEON_PURPLE
            self.simbolo = "🧲"
            self.duracion_efecto = 10.0  # 10 segundos de magnetismo mejorado
        else:
            self.color = NEON_GREEN
            self.simbolo = "?"
            self.duracion_efecto = 5.0

    def update(self, dt):
        """Actualiza el power-up"""
        if not self.activo or self.recogido:
            return

        # Actualizar tiempo de vida
        self.tiempo_transcurrido += dt
        if self.tiempo_transcurrido >= self.tiempo_vida:
            self.activo = False
            return

        # Efectos visuales
        self.rotacion += 120 * dt  # Rotar 120 grados por segundo
        if self.rotacion >= 360:
            self.rotacion -= 360

        self.pulso = abs(math.sin(time.time() * 4)) * 8

    def draw(self, screen):
        """Dibuja el power-up"""
        if not self.activo or self.recogido:
            return

        # Advertencia de desaparición (últimos 3 segundos)
        tiempo_restante = self.tiempo_vida - self.tiempo_transcurrido
        if tiempo_restante < 3.0:
            # Parpadeo
            if int(tiempo_restante * 4) % 2 == 0:
                return

        # Anillo exterior pulsante
        radio_anillo = self.radio + 10 + self.pulso
        for i in range(2):
            radio = radio_anillo - i * 5
            grosor = 3 - i
            alpha = 150 - i * 50

            anillo_surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            color_alpha = (*self.color[:3], alpha)
            pygame.draw.circle(anillo_surf, color_alpha, (radio, radio), radio, grosor)
            screen.blit(anillo_surf, (self.x - radio, self.y - radio))

        # Forma del power-up según tipo
        if self.tipo == self.TIPO_ESCUDO:
            self._dibujar_escudo(screen)
        elif self.tipo == self.TIPO_VELOCIDAD:
            self._dibujar_rayo(screen)
        elif self.tipo == self.TIPO_MAGNETISMO:
            self._dibujar_iman(screen)

        # Centro brillante
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 8)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 8, 2)

    def _dibujar_escudo(self, screen):
        """Dibuja icono de escudo"""
        puntos = []
        num_puntos = 6
        for i in range(num_puntos):
            angulo = (i / num_puntos) * 2 * math.pi + math.radians(self.rotacion)
            r = self.radio if i % 2 == 0 else self.radio * 0.7
            px = self.x + r * math.cos(angulo)
            py = self.y + r * math.sin(angulo)
            puntos.append((px, py))

        if len(puntos) >= 3:
            pygame.draw.polygon(screen, self.color, puntos, 3)

    def _dibujar_rayo(self, screen):
        """Dibuja icono de rayo"""
        # Rayo zigzag
        puntos_rayo = [
            (self.x, self.y - self.radio),
            (self.x + 5, self.y - 5),
            (self.x - 3, self.y),
            (self.x + 3, self.y + 5),
            (self.x, self.y + self.radio),
            (self.x - 5, self.y),
        ]
        pygame.draw.lines(screen, self.color, False, puntos_rayo, 3)

    def _dibujar_iman(self, screen):
        """Dibuja icono de imán"""
        # Forma de U (imán)
        rect_izq = pygame.Rect(
            self.x - self.radio, self.y - self.radio // 2, 5, self.radio
        )
        rect_der = pygame.Rect(
            self.x + self.radio - 5, self.y - self.radio // 2, 5, self.radio
        )
        rect_base = pygame.Rect(
            self.x - self.radio, self.y + self.radio // 2 - 5, self.radio * 2, 5
        )

        pygame.draw.rect(screen, self.color, rect_izq)
        pygame.draw.rect(screen, self.color, rect_der)
        pygame.draw.rect(screen, self.color, rect_base)

    def colisiona_con(self, objeto):
        """
        Verifica colisión con un objeto

        Args:
            objeto: Objeto con atributos x, y

        Returns:
            bool: True si hay colisión
        """
        if not self.activo or self.recogido:
            return False

        dx = self.x - objeto.x
        dy = self.y - objeto.y
        distancia = math.sqrt(dx * dx + dy * dy)

        return distancia < (self.radio + 30)  # Radio generoso

    def recoger(self):
        """Marca el power-up como recogido"""
        self.recogido = True
        self.activo = False


class SistemaPowerUps:
    """Gestiona la generación y estado de power-ups"""

    def __init__(self):
        """Inicializa el sistema de power-ups"""
        self.power_ups = []
        self.power_ups_activos_jugador = {}  # {tipo: tiempo_restante}

        # Configuración de generación
        self.intervalo_spawn = 20.0  # Generar cada 20 segundos
        self.tiempo_siguiente_spawn = self.intervalo_spawn
        self.tiempo_acumulado = 0

    def update(self, dt):
        """Actualiza el sistema"""
        self.tiempo_acumulado += dt

        # Generar nuevo power-up si es tiempo
        if self.tiempo_acumulado >= self.tiempo_siguiente_spawn:
            self._generar_power_up()
            self.tiempo_acumulado = 0
            # Variar el intervalo
            self.tiempo_siguiente_spawn = random.uniform(15.0, 25.0)

        # Actualizar power-ups en el mapa
        for powerup in self.power_ups[:]:
            powerup.update(dt)
            if not powerup.activo:
                self.power_ups.remove(powerup)

        # Actualizar duración de power-ups activos del jugador
        for tipo in list(self.power_ups_activos_jugador.keys()):
            self.power_ups_activos_jugador[tipo] -= dt
            if self.power_ups_activos_jugador[tipo] <= 0:
                del self.power_ups_activos_jugador[tipo]

    def _generar_power_up(self):
        """Genera un nuevo power-up en posición aleatoria"""
        margen = 80
        x = random.randint(margen, SCREEN_WIDTH - margen)
        y = random.randint(margen, SCREEN_HEIGHT - margen)

        # Elegir tipo aleatorio
        tipos = [PowerUp.TIPO_ESCUDO, PowerUp.TIPO_VELOCIDAD, PowerUp.TIPO_MAGNETISMO]
        tipo = random.choice(tipos)

        powerup = PowerUp(x, y, tipo)
        self.power_ups.append(powerup)

    def draw(self, screen):
        """Dibuja todos los power-ups"""
        for powerup in self.power_ups:
            powerup.draw(screen)

    def verificar_colisiones(self, cubo):
        """
        Verifica si CUBO recogió algún power-up

        Args:
            cubo: Objeto CUBO

        Returns:
            list: Lista de power-ups recogidos
        """
        recogidos = []

        for powerup in self.power_ups:
            if powerup.colisiona_con(cubo):
                powerup.recoger()
                self.activar_power_up(powerup.tipo, powerup.duracion_efecto)
                recogidos.append(powerup)

        return recogidos

    def activar_power_up(self, tipo, duracion):
        """
        Activa un power-up para el jugador

        Args:
            tipo: Tipo de power-up
            duracion: Duración en segundos
        """
        # Si ya existe, extender la duración
        if tipo in self.power_ups_activos_jugador:
            self.power_ups_activos_jugador[tipo] += duracion
        else:
            self.power_ups_activos_jugador[tipo] = duracion

    def tiene_escudo_activo(self):
        """Verifica si el escudo está activo"""
        return PowerUp.TIPO_ESCUDO in self.power_ups_activos_jugador

    def tiene_velocidad_activa(self):
        """Verifica si la velocidad está activa"""
        return PowerUp.TIPO_VELOCIDAD in self.power_ups_activos_jugador

    def tiene_magnetismo_activo(self):
        """Verifica si el magnetismo mejorado está activo"""
        return PowerUp.TIPO_MAGNETISMO in self.power_ups_activos_jugador

    def get_multiplicador_velocidad(self):
        """Retorna el multiplicador de velocidad actual"""
        return 1.5 if self.tiene_velocidad_activa() else 1.0

    def get_multiplicador_magnetismo(self):
        """Retorna el multiplicador de magnetismo actual"""
        return 1.5 if self.tiene_magnetismo_activo() else 1.0

    def dibujar_indicadores(self, screen):
        """Dibuja indicadores de power-ups activos en UI"""
        if not self.power_ups_activos_jugador:
            return

        # Posición inicial
        x_inicio = SCREEN_WIDTH - 200
        y_inicio = 70

        font = pygame.font.Font(None, 24)

        # Fondo
        altura_panel = len(self.power_ups_activos_jugador) * 35 + 10
        panel_rect = pygame.Rect(x_inicio - 10, y_inicio - 5, 190, altura_panel)
        panel_surf = pygame.Surface(
            (panel_rect.width, panel_rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            panel_surf, (0, 0, 0, 180), panel_surf.get_rect(), border_radius=10
        )
        screen.blit(panel_surf, panel_rect.topleft)

        y_offset = y_inicio

        for tipo, tiempo_restante in self.power_ups_activos_jugador.items():
            # Icono y nombre
            if tipo == PowerUp.TIPO_ESCUDO:
                icono = "🛡"
                nombre = "Escudo"
                color = NEON_CYAN
            elif tipo == PowerUp.TIPO_VELOCIDAD:
                icono = "⚡"
                nombre = "Velocidad"
                color = NEON_YELLOW
            else:  # MAGNETISMO
                icono = "🧲"
                nombre = "Magnetismo"
                color = NEON_PURPLE

            # Texto
            texto = font.render(
                f"{icono} {nombre}: {tiempo_restante:.1f}s", True, color
            )
            screen.blit(texto, (x_inicio, y_offset))

            y_offset += 35

    def limpiar(self):
        """Limpia todos los power-ups"""
        self.power_ups.clear()
        self.power_ups_activos_jugador.clear()

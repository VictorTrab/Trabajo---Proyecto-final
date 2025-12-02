"""
Lógica del juego CUBO: Arquitecto del Caos - Fase 4
Meteoros, portales y power-ups
"""

import pygame
import time
from core.logica_cubo_fase3 import GameCuboFase3
from entidades.meteoro import GeneradorMeteoros
from entidades.portal import SistemaPortales
from entidades.powerup import SistemaPowerUps
from entidades.cubo import Cubo
from config.constantes import *


class GameCuboFase4(GameCuboFase3):
    """Clase principal del juego CUBO - Fase 4: Meteoros y Portales"""

    def __init__(self, screen, level_number, difficulty, player, config=None):
        """
        Inicializa el juego Fase 4

        Args:
            screen: Pantalla de pygame
            level_number: Número de nivel (1-10)
            difficulty: Dificultad ("Fácil", "Medio", "Difícil")
            player: Objeto Player
            config: Configuración del juego
        """
        # Inicializar fase 3
        super().__init__(screen, level_number, difficulty, player, config)

        # Sistemas de Fase 4
        self.generador_meteoros = GeneradorMeteoros(difficulty)
        self.sistema_portales = SistemaPortales(num_pares=2)  # 2 pares de portales
        self.sistema_powerups = SistemaPowerUps()

        # Estado de Fase 4
        self.meteoros_esquivados = 0
        self.daño_recibido = 0
        self.portales_usados = 0
        self.powerups_recogidos = 0

    def handle_input(self, keys, event=None):
        """Maneja la entrada del jugador (heredado de Fase 3)"""
        super().handle_input(keys, event)

    def update(self, dt=None):
        """Actualiza el estado del juego"""
        # Actualizar lógica de Fase 3 primero
        resultado_fase3 = super().update(dt)

        # Si el juego terminó, no actualizar Fase 4
        if resultado_fase3:
            return resultado_fase3

        # Actualizar sistemas de Fase 4
        self._actualizar_fase4(dt if dt else 0.016)

        return False

    def _actualizar_fase4(self, dt):
        """Actualiza los sistemas específicos de Fase 4"""
        # Actualizar generador de meteoros
        self.generador_meteoros.update(dt)

        # Actualizar sistema de portales
        self.sistema_portales.update(dt)

        # Actualizar sistema de power-ups
        self.sistema_powerups.update(dt)

        # Verificar colisiones con meteoros
        self._verificar_colisiones_meteoros()

        # Verificar teletransportaciones por portales
        self._verificar_teletransportaciones()

        # Verificar recolección de power-ups
        self._verificar_powerups()

        # Aplicar efectos de power-ups
        self._aplicar_efectos_powerups()

    def _verificar_colisiones_meteoros(self):
        """Verifica colisiones de meteoros con CUBO y piezas"""
        # Crear lista de objetos a verificar
        objetos = [self.cubo] + self.piezas

        # Verificar colisiones
        colisiones = self.generador_meteoros.verificar_colisiones(objetos)

        for meteoro, objeto in colisiones:
            if objeto == self.cubo:
                # Impacto en CUBO
                if self.sistema_powerups.tiene_escudo_activo():
                    # Escudo protege del daño
                    self.cubo.cambiar_emocion(Cubo.EMOCION_DETERMINADO, 1.0)
                    # Efecto visual de escudo
                    self.particle_system.emit_burst(
                        self.cubo.x, self.cubo.y, color=NEON_CYAN, count=20, spread=3.0
                    )
                else:
                    # Recibir daño
                    self.daño_recibido += 1
                    self.cubo.cambiar_emocion(Cubo.EMOCION_DOLOR, 2.0)

                    # Soltar pieza si la tiene
                    for zona in self.cubo.zonas_atraccion.values():
                        if zona["ocupada"]:
                            pieza = zona["pieza"]
                            pieza.siendo_arrastrada = False
                            zona["ocupada"] = False
                            zona["pieza"] = None

                    # Efecto visual de impacto
                    self.particle_system.emit_burst(
                        self.cubo.x,
                        self.cubo.y,
                        color=NEON_ORANGE,
                        count=30,
                        spread=4.0,
                    )
            else:
                # Impacto en pieza
                if not objeto.colocada:
                    # Empujar pieza
                    dx = objeto.x - meteoro.x
                    dy = objeto.y - meteoro.y
                    objeto.aplicar_velocidad(dx * 2, dy * 2)

                    # Efecto de impacto
                    self.particle_system.emit_burst(
                        objeto.x, objeto.y, color=GRAY, count=10, spread=2.0
                    )

    def _verificar_teletransportaciones(self):
        """Verifica y ejecuta teletransportaciones a través de portales"""
        # Lista de objetos que pueden teletransportarse
        objetos = [self.cubo]

        # Solo incluir piezas que no estén colocadas
        for pieza in self.piezas:
            if not pieza.colocada:
                objetos.append(pieza)

        # Verificar teletransportaciones
        teletransportados = self.sistema_portales.verificar_teletransportaciones(
            objetos
        )

        for objeto, portal_entrada, portal_salida in teletransportados:
            if objeto == self.cubo:
                self.portales_usados += 1
                self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 0.5)

            # Efectos visuales de teletransportación
            self.particle_system.emit_burst(
                portal_entrada.x,
                portal_entrada.y,
                color=portal_entrada.color,
                count=20,
                spread=3.0,
            )
            self.particle_system.emit_burst(
                portal_salida.x,
                portal_salida.y,
                color=portal_salida.color,
                count=20,
                spread=3.0,
            )

    def _verificar_powerups(self):
        """Verifica si CUBO recogió algún power-up"""
        recogidos = self.sistema_powerups.verificar_colisiones(self.cubo)

        for powerup in recogidos:
            self.powerups_recogidos += 1
            self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 1.5)

            # Efecto visual de recolección
            self.particle_system.emit_burst(
                powerup.x, powerup.y, color=powerup.color, count=25, spread=3.5
            )
            self.particle_system.emit_glow(
                powerup.x, powerup.y, color=powerup.color, radius=50, count=15
            )

    def _aplicar_efectos_powerups(self):
        """Aplica los efectos de power-ups activos"""
        # Modificar velocidad del CUBO si tiene power-up de velocidad
        # (Ya se aplica en el método de movimiento del cubo)

        # Modificar radio de magnetismo si tiene power-up
        if self.sistema_powerups.tiene_magnetismo_activo():
            self.radio_atraccion = 120  # Aumentado de 80
        else:
            self.radio_atraccion = 80  # Normal

    def draw(self):
        """Dibuja el juego con elementos de Fase 4"""
        # Dibujar Fase 3 primero (fondo, piezas, CUBO, UI, etc.)
        super().draw()

        # Dibujar sistemas de Fase 4
        self.sistema_portales.draw(self.screen)
        self.generador_meteoros.draw(self.screen)
        self.sistema_powerups.draw(self.screen)

        # Dibujar indicadores de power-ups activos
        self.sistema_powerups.dibujar_indicadores(self.screen)

        # Dibujar escudo visual si está activo
        if self.sistema_powerups.tiene_escudo_activo():
            self._dibujar_escudo_visual()

    def _dibujar_escudo_visual(self):
        """Dibuja un escudo visual alrededor de CUBO"""
        import math

        # Anillo de escudo pulsante
        pulso = abs(math.sin(time.time() * 5)) * 10
        radio_escudo = 60 + pulso

        # Efecto de glow
        for i in range(3):
            radio = radio_escudo - i * 5
            grosor = 3 - i
            alpha = 100 - i * 30

            escudo_surf = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            color = (*NEON_CYAN[:3], alpha)
            pygame.draw.circle(escudo_surf, color, (radio, radio), radio, grosor)
            self.screen.blit(escudo_surf, (self.cubo.x - radio, self.cubo.y - radio))

    def get_resultado_nivel(self):
        """Retorna el resultado del nivel con estadísticas de Fase 4"""
        resultado = super().get_resultado_nivel()

        # Agregar estadísticas de Fase 4
        resultado["fase4_stats"] = {
            "meteoros_esquivados": self.meteoros_esquivados,
            "daño_recibido": self.daño_recibido,
            "portales_usados": self.portales_usados,
            "powerups_recogidos": self.powerups_recogidos,
        }

        # Bonus por esquivar meteoros (si no recibió daño)
        if self.daño_recibido == 0 and hasattr(resultado, "puntos"):
            resultado["puntos"] += 150  # Bonus por esquiva perfecta

        return resultado

"""
Lógica del juego CUBO: Arquitecto del Caos - Fase 4
Meteoros, portales y power-ups
"""

import pygame
import time
import random
import math
from core.logica_cubo_fase3 import GameCuboFase3
from entidades.meteoro import GeneradorMeteoros
from entidades.portal import SistemaPortales
from entidades.powerup import SistemaPowerUps
from entidades.cubo import Cubo
from entidades.pieza_geometrica import PiezaGeometrica
from config.constantes import *


class GameCuboFase4(GameCuboFase3):
    """Clase principal del juego CUBO - Fase 4: Meteoros y Portales"""

    def __init__(self, screen, level_number, player, config=None, audio=None):
        """
        Inicializa el juego Fase 4

        Args:
            screen: Pantalla de pygame
            level_number: Número de nivel (1-3)
            player: Objeto Player
            config: Configuración del juego
            audio: Sistema de audio
        """
        # Crear sistemas de Fase 4 ANTES de llamar a super().__init__()
        # porque _generar_piezas_para_objetivo() se llama en Fase2.__init__()
        self.generador_meteoros = GeneradorMeteoros(nivel=level_number)
        self.sistema_portales = SistemaPortales(num_pares=2)  # 2 pares de portales
        self.sistema_powerups = SistemaPowerUps()

        # Inicializar fase 3 (que llama a Fase2, que llama a _generar_piezas_para_objetivo)
        super().__init__(screen, level_number, player, config, audio)

        # Configurar zonas prohibidas para meteoros (sobre portales)
        posiciones_portales = []
        for entrada, salida in self.sistema_portales.pares_portales:
            posiciones_portales.append((entrada.x, entrada.y, entrada.radio + 30))
            posiciones_portales.append((salida.x, salida.y, salida.radio + 30))
        self.generador_meteoros.establecer_zonas_prohibidas(posiciones_portales)

        # Estado de Fase 4
        self.meteoros_esquivados = 0
        self.daño_recibido = 0
        self.portales_usados = 0
        self.powerups_recogidos = 0

    def _generar_piezas_para_objetivo(self):
        """
        Sobrescribe el método de Fase 3 para evitar generar piezas sobre portales
        """
        # Obtener posiciones de todos los portales
        posiciones_portales = []
        for entrada, salida in self.sistema_portales.pares_portales:
            posiciones_portales.append((entrada.x, entrada.y, entrada.radio + 50))
            posiciones_portales.append((salida.x, salida.y, salida.radio + 50))

        # Calcular número de distractores
        num_distractores = self.generador_niveles.calcular_piezas_distractor(
            self.nivel_numero
        )

        margen = 100
        posiciones_usadas = []

        def obtener_posicion_libre():
            intentos = 0
            while intentos < 150:  # Más intentos para considerar portales
                x = random.randint(margen, SCREEN_WIDTH - margen - 200)
                y = random.randint(margen, SCREEN_HEIGHT - margen)

                muy_cerca = False

                # Verificar distancia con otras piezas
                for px, py in posiciones_usadas:
                    distancia = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                    if distancia < 60:
                        muy_cerca = True
                        break

                # Verificar distancia con portales para evitar bucle de teletransportación
                if not muy_cerca:
                    for portal_x, portal_y, portal_radio in posiciones_portales:
                        distancia = math.sqrt((x - portal_x) ** 2 + (y - portal_y) ** 2)
                        if (
                            distancia < portal_radio
                        ):  # Zona de seguridad alrededor del portal
                            muy_cerca = True
                            break

                if not muy_cerca:
                    posiciones_usadas.append((x, y))
                    return x, y

                intentos += 1

            # Si no se encuentra posición después de muchos intentos, usar posición aleatoria
            x = random.randint(margen, SCREEN_WIDTH - margen - 200)
            y = random.randint(margen, SCREEN_HEIGHT - margen)
            posiciones_usadas.append((x, y))
            return x, y

        # Generar piezas necesarias
        for definicion in self.figura_objetivo.definicion:
            x, y = obtener_posicion_libre()
            pieza = PiezaGeometrica(x, y, definicion["tipo"])
            self.piezas.append(pieza)

        # Generar piezas distractor
        tipos_disponibles = [
            PiezaGeometrica.CUADRADO,
            PiezaGeometrica.TRIANGULO,
            PiezaGeometrica.CIRCULO,
            PiezaGeometrica.ROMBO,
            PiezaGeometrica.RECTANGULO,
        ]

        for _ in range(num_distractores):
            x, y = obtener_posicion_libre()
            tipo = random.choice(tipos_disponibles)
            pieza = PiezaGeometrica(x, y, tipo)
            self.piezas.append(pieza)

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

        # Verificar teletransporte por portales
        self._verificar_teletransportaciones()

        # Verificar recolección de power-ups
        self._verificar_powerups()

        # Aplicar efectos de power-ups
        self._aplicar_efectos_powerups()

    def _verificar_colisiones_meteoros(self):
        """Verifica colisiones de meteoros con CUBO y piezas"""
        # Validar que existan los objetos necesarios
        if not hasattr(self, "cubo") or not hasattr(self, "piezas"):
            return

        if not hasattr(self, "generador_meteoros"):
            return

        # Crear lista de objetos a verificar
        objetos = [self.cubo] + self.piezas

        # Verificar colisiones
        colisiones = self.generador_meteoros.verificar_colisiones(objetos)

        for meteoro, objeto in colisiones:
            # Reproducir efecto de explosión
            if self.audio:
                self.audio.reproducir_efecto("explosion")

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

                    # Validar que cubo tenga el método recibir_impacto
                    if hasattr(self.cubo, "recibir_impacto"):
                        cubo_destruido = self.cubo.recibir_impacto()
                    else:
                        cubo_destruido = False

                    if cubo_destruido:
                        # CUBO destruido - Game Over
                        self.cubo.cambiar_emocion(Cubo.EMOCION_DOLOR, 3.0)
                        self.failed = True

                        # Efecto visual de destrucción masiva
                        for i in range(5):
                            self.particle_system.emit_burst(
                                self.cubo.x,
                                self.cubo.y,
                                color=NEON_PINK if i % 2 == 0 else NEON_ORANGE,
                                count=50,
                                spread=5.0,
                            )
                    else:
                        # Aún puede resistir
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
                if hasattr(objeto, "colocada") and not objeto.colocada:
                    # Empujar pieza
                    if hasattr(objeto, "x") and hasattr(objeto, "y"):
                        dx = objeto.x - meteoro.x
                        dy = objeto.y - meteoro.y

                        # Validar que tenga método aplicar_velocidad
                        if hasattr(objeto, "aplicar_velocidad"):
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

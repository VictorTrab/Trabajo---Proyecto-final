"""
Lógica del juego CUBO: Arquitecto del Caos - Fase 5
Sistema Emocional Avanzado con efectos visuales y narrativa
"""

import pygame
from core.logica_cubo_fase4 import GameCuboFase4
from entidades.efectos_emocionales import EfectosEmocionales
from entidades.animaciones_emocionales import AnimadorEmocional, AnimacionContinua
from entidades.ambiente_emocional import AmbienteEmocional
from config.constantes import *


class GameCuboFase5(GameCuboFase4):
    """Clase principal del juego CUBO - Fase 5: Sistema Emocional Avanzado"""

    def __init__(self, screen, level_number, player, config=None, audio=None):
        """
        Inicializa el juego Fase 5

        Args:
            screen: Pantalla de pygame
            level_number: Número de nivel (1-3)
            player: Objeto Player
            config: Configuración del juego
            audio: Sistema de audio
        """
        # Inicializar fase 4
        super().__init__(screen, level_number, player, config, audio)

        # Sistemas de Fase 5
        self.efectos_emocionales = EfectosEmocionales()
        self.animador = AnimadorEmocional()
        self.animacion_continua = AnimacionContinua()
        self.ambiente = AmbienteEmocional()

        # Fuentes para narrativa
        self.fuente_narrativa = pygame.font.Font(None, 32)

        # Estado emocional anterior para detectar cambios
        self.emocion_anterior = None

    def update(self, dt=None):
        """Actualiza el estado del juego"""
        if dt is None:
            dt = 0.016

        # Actualizar lógica de Fase 4 primero
        resultado_fase4 = super().update(dt)

        # Si el juego terminó, manejar eventos finales
        if resultado_fase4:
            self._manejar_finalizacion(resultado_fase4)
            return resultado_fase4

        # Actualizar sistemas de Fase 5
        self._actualizar_fase5(dt)

        return False

    def _actualizar_fase5(self, dt: float):
        """Actualiza todos los sistemas emocionales de Fase 5"""
        # Obtener emoción actual del cubo
        emocion_actual = (
            self.cubo.emocion if hasattr(self.cubo, "emocion") else "neutral"
        )

        # Detectar cambio de emoción
        if emocion_actual != self.emocion_anterior:
            self._on_cambio_emocion(emocion_actual)
            self.emocion_anterior = emocion_actual

        # Actualizar sistemas
        self.efectos_emocionales.actualizar(
            dt, emocion_actual, (self.cubo.x, self.cubo.y)
        )
        self.animador.actualizar(dt)
        self.animacion_continua.actualizar(dt)
        self.ambiente.actualizar(dt, emocion_actual)

    def _on_cambio_emocion(self, nueva_emocion: str):
        """Maneja el cambio de emoción"""
        # Animación especial al cambiar a determinación
        if nueva_emocion == "determinado":
            self.animador.iniciar_animacion("pulso_determinado")

    def _manejar_finalizacion(self, resultado: str):
        """Maneja eventos al finalizar el nivel"""
        if resultado == "completado":
            # Nivel completado
            self.animador.iniciar_animacion("celebracion_exito")
            self.efectos_emocionales.evento_especial(
                "exito", (self.cubo.x, self.cubo.y)
            )
        elif resultado == "fallido":
            # Nivel fallido
            self.animador.iniciar_animacion("abatimiento_fracaso")

    def _manejar_evento_meteoro(self, impacto: bool):
        """Maneja eventos relacionados con meteoros (override de Fase 4)"""
        if impacto:
            # Daño recibido
            self.efectos_emocionales.evento_especial("dano", (self.cubo.x, self.cubo.y))
            self.animador.iniciar_animacion("sacudida_dolor")

    def _manejar_evento_powerup(self, tipo_powerup: str):
        """Maneja eventos al recoger power-ups (override de Fase 4)"""
        self.efectos_emocionales.evento_especial("powerup", (self.cubo.x, self.cubo.y))

    def draw(self):
        """Dibuja todo el estado del juego con efectos emocionales"""
        emocion_actual = (
            self.cubo.emocion if hasattr(self.cubo, "emocion") else "neutral"
        )

        # 1. Dibujar fondo dinámico emocional
        self.ambiente.dibujar_fondo(self.screen, emocion_actual)

        # 2. Dibujar partículas de ambiente de fondo
        self.ambiente.dibujar_particulas(self.screen)

        # 3. Dibujar elementos del juego (Fase 4 y anteriores) usando el método heredado
        super().draw()

        # 4. Dibujar partículas emocionales del jugador (encima de todo lo demás)
        self.efectos_emocionales.dibujar_particulas(self.screen)

        # 5. Aplicar filtros emocionales de pantalla
        offset_x, offset_y = self.efectos_emocionales.aplicar_efectos_pantalla(
            self.screen, emocion_actual
        )

    def _dibujar_elementos_juego(self):
        """Dibuja los elementos del juego de fases anteriores"""
        # No podemos llamar a super().draw() porque crearía recursión
        # En su lugar, llamaremos a los métodos de dibujo específicos de Fase 3

        # Para evitar duplicación, simplemente llamamos al draw de Fase 4
        # pero sin los efectos emocionales adicionales
        # La forma correcta es NO sobrescribir draw sino extenderlo
        pass  # Este método ya no es necesario

    def _dibujar_cubo_con_animaciones(self):
        """Dibuja el cubo con animaciones emocionales aplicadas"""
        # Ya no es necesario, el cubo se dibuja en super().draw()
        pass

    def _dibujar_ui_mejorada(self, offset_x: float, offset_y: float):
        """Dibuja la UI con posibles offsets por efectos emocionales"""
        # Ya no es necesario, la UI se dibuja en super().draw()
        pass

    def on_pieza_colocada(self):
        """Callback cuando se coloca una pieza correctamente"""
        pass

    def reiniciar_nivel(self):
        """Reinicia el nivel actual (limpia sistemas emocionales)"""
        super().reiniciar_nivel() if hasattr(super(), "reiniciar_nivel") else None

        # Limpiar sistemas de Fase 5
        self.efectos_emocionales.limpiar()
        self.ambiente.limpiar()
        self.animador.detener()

    def limpiar(self):
        """Limpia recursos al salir del nivel"""
        super().limpiar() if hasattr(super(), "limpiar") else None

        # Limpiar otros sistemas
        self.efectos_emocionales.limpiar()
        self.ambiente.limpiar()

    def obtener_estadisticas_fase5(self) -> dict:
        """Obtiene estadísticas de la fase 5"""
        return {
            "emocion_actual": (
                self.cubo.emocion if hasattr(self.cubo, "emocion") else "neutral"
            ),
        }

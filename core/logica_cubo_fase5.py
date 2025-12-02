"""
Lógica del juego CUBO: Arquitecto del Caos - Fase 5
Sistema Emocional Avanzado con efectos visuales, audio y narrativa
"""

import pygame
from core.logica_cubo_fase4 import GameCuboFase4
from entidades.efectos_emocionales import EfectosEmocionales
from entidades.audio_emocional import AudioEmocional
from entidades.animaciones_emocionales import AnimadorEmocional, AnimacionContinua
from entidades.narrativa_dinamica import NarrativaDinamica
from entidades.combo_emocional import ComboEmocional, VisualizadorCombo
from entidades.ambiente_emocional import AmbienteEmocional, FondoDinamico
from config.constantes import *


class GameCuboFase5(GameCuboFase4):
    """Clase principal del juego CUBO - Fase 5: Sistema Emocional Avanzado"""

    def __init__(self, screen, level_number, difficulty, player, config=None):
        """
        Inicializa el juego Fase 5

        Args:
            screen: Pantalla de pygame
            level_number: Número de nivel (1-10)
            difficulty: Dificultad ("Fácil", "Medio", "Difícil")
            player: Objeto Player
            config: Configuración del juego (puede incluir habilitar_audio)
        """
        # Inicializar fase 4
        super().__init__(screen, level_number, difficulty, player, config)

        # Configuración de audio
        habilitar_audio = True
        if config and isinstance(config, dict):
            habilitar_audio = config.get("habilitar_audio", True)

        # Sistemas de Fase 5
        self.efectos_emocionales = EfectosEmocionales()
        self.audio_emocional = AudioEmocional(habilitar_audio=habilitar_audio)
        self.animador = AnimadorEmocional()
        self.animacion_continua = AnimacionContinua()
        self.narrativa = NarrativaDinamica()
        self.combo = ComboEmocional()
        self.visualizador_combo = VisualizadorCombo()
        self.ambiente = AmbienteEmocional()
        self.fondo_dinamico = FondoDinamico()

        # Fuentes para narrativa
        self.fuente_narrativa = pygame.font.Font(None, 32)
        self.fuente_combo_grande = pygame.font.Font(None, 48)
        self.fuente_combo_pequena = pygame.font.Font(None, 24)

        # Estado emocional anterior para detectar cambios
        self.emocion_anterior = None

        # Guardar dificultad para música
        self.difficulty = difficulty

        # Iniciar música según dificultad del nivel
        self.audio_emocional.reproducir_musica_por_dificultad(difficulty)

        # Mensaje de bienvenida
        self.narrativa.mostrar_dialogo("tutorial_emociones", "sistema", duracion=4.0)

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
        self.narrativa.actualizar(dt)
        self.combo.actualizar(dt, emocion_actual)
        self.ambiente.actualizar(dt, emocion_actual)

        # Aplicar bonos de combo a puntuación
        bonus = self.combo.obtener_bonus_acumulado()
        if bonus > 0:
            self.player.add_score(bonus)
            self.narrativa.reaccionar_evento("combo_alcanzado")
            self.audio_emocional.evento_juego("combo_alcanzado")

    def _on_cambio_emocion(self, nueva_emocion: str):
        """Maneja el cambio de emoción"""
        # Actualizar música
        self.audio_emocional.actualizar_emocion(nueva_emocion)

        # Mostrar diálogo contextual
        if nueva_emocion in ["feliz", "determinado"]:
            self.narrativa.reaccionar_emocion(nueva_emocion, "inicio")
        elif nueva_emocion in ["triste", "miedo", "dolor"]:
            self.narrativa.reaccionar_emocion(nueva_emocion, "inicio")

        # Animación especial al cambiar a determinación
        if nueva_emocion == "determinado":
            self.animador.iniciar_animacion("pulso_determinado")

    def _manejar_finalizacion(self, resultado: str):
        """Maneja eventos al finalizar el nivel"""
        if resultado == "completado":
            # Nivel completado
            self.animador.iniciar_animacion("celebracion_exito")
            self.narrativa.reaccionar_evento("nivel_completado")
            self.audio_emocional.evento_juego("nivel_completado")
            self.efectos_emocionales.evento_especial(
                "exito", (self.cubo.x, self.cubo.y)
            )
        elif resultado == "fallido":
            # Nivel fallido
            self.animador.iniciar_animacion("abatimiento_fracaso")
            self.narrativa.reaccionar_evento("nivel_fallido")
            self.audio_emocional.evento_juego("nivel_fallido")

    def _manejar_evento_meteoro(self, impacto: bool):
        """Maneja eventos relacionados con meteoros (override de Fase 4)"""
        if impacto:
            # Daño recibido
            self.narrativa.reaccionar_emocion("dolor", "inicio")
            self.audio_emocional.evento_juego("dano_recibido")
            self.efectos_emocionales.evento_especial("dano", (self.cubo.x, self.cubo.y))
            self.animador.iniciar_animacion("sacudida_dolor")
        else:
            # Meteoro esquivado
            if self.meteoros_esquivados > 0 and self.meteoros_esquivados % 5 == 0:
                self.narrativa.reaccionar_evento("meteoro_esquivado")

    def _manejar_evento_powerup(self, tipo_powerup: str):
        """Maneja eventos al recoger power-ups (override de Fase 4)"""
        self.narrativa.reaccionar_evento("powerup_obtenido")
        self.audio_emocional.evento_juego("powerup_obtenido")
        self.efectos_emocionales.evento_especial("powerup", (self.cubo.x, self.cubo.y))

    def _manejar_evento_portal(self):
        """Maneja eventos al usar portales (override de Fase 4)"""
        self.narrativa.reaccionar_evento("portal_usado")
        self.audio_emocional.evento_juego("portal_usado")

    def _manejar_uso_pista(self):
        """Maneja el uso de pistas (override de Fase 3)"""
        super()._usar_pista() if hasattr(super(), "_usar_pista") else None
        self.narrativa.reaccionar_evento("pista_usada")
        self.audio_emocional.evento_juego("pista_usada")

    def draw(self):
        """Dibuja todo el estado del juego con efectos emocionales"""
        emocion_actual = (
            self.cubo.emocion if hasattr(self.cubo, "emocion") else "neutral"
        )

        # 1. Dibujar fondo dinámico emocional
        self.fondo_dinamico.dibujar_fondo_gradiente(self.screen, emocion_actual)

        # 2. Dibujar partículas de ambiente de fondo
        self.ambiente.dibujar_particulas_ambiente(self.screen)

        # 3. Dibujar elementos del juego (Fase 4 y anteriores) usando el método heredado
        super().draw()

        # 4. Dibujar partículas emocionales del jugador (encima de todo lo demás)
        self.efectos_emocionales.dibujar_particulas(self.screen)

        # 5. Aplicar filtros emocionales de pantalla
        offset_x, offset_y = self.efectos_emocionales.aplicar_efectos_pantalla(
            self.screen, emocion_actual
        )

        # 6. Aplicar clima emocional
        self.ambiente.generar_efecto_clima(self.screen, emocion_actual)

        # 7. Dibujar narrativa (diálogos)
        self.narrativa.dibujar(self.screen, self.fuente_narrativa)

        # 8. Dibujar combo
        if self.combo.combo_activo:
            pos_combo = (WINDOW_WIDTH - 100, 100)
            self.visualizador_combo.dibujar(
                self.screen,
                self.combo,
                pos_combo,
                self.fuente_combo_grande,
                self.fuente_combo_pequena,
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
        self.audio_emocional.evento_juego("pieza_colocada")
        # Multiplicar puntos por combo
        puntos_base = 10  # Puntos por pieza
        puntos_con_combo = self.combo.aplicar_multiplicador(puntos_base)
        # Agregar diferencia de bonus
        if puntos_con_combo > puntos_base:
            self.player.add_score(puntos_con_combo - puntos_base)

    def reiniciar_nivel(self):
        """Reinicia el nivel actual (limpia sistemas emocionales)"""
        super().reiniciar_nivel() if hasattr(super(), "reiniciar_nivel") else None

        # Limpiar sistemas de Fase 5
        self.efectos_emocionales.limpiar()
        self.narrativa.limpiar()
        self.combo.reiniciar()
        self.visualizador_combo.reiniciar()
        self.ambiente.limpiar()
        self.animador.detener()

    def limpiar(self):
        """Limpia recursos al salir del nivel"""
        super().limpiar() if hasattr(super(), "limpiar") else None

        # Detener audio
        self.audio_emocional.limpiar()

        # Limpiar otros sistemas
        self.efectos_emocionales.limpiar()
        self.narrativa.limpiar()
        self.combo.reiniciar()
        self.ambiente.limpiar()

    def pausar(self):
        """Pausa el juego"""
        self.audio_emocional.pausar_musica()

    def reanudar(self):
        """Reanuda el juego"""
        self.audio_emocional.reanudar_musica()

    def obtener_estadisticas_fase5(self) -> dict:
        """Obtiene estadísticas de la fase 5"""
        return {
            "combo_maximo": self.combo.combo_maximo_alcanzado,
            "bonus_total_combos": self.combo.total_bonus_obtenido,
            "audio_habilitado": self.audio_emocional.habilitado,
            "emocion_actual": (
                self.cubo.emocion if hasattr(self.cubo, "emocion") else "neutral"
            ),
        }

"""
Sistema de Combos Emocionales - Fase 5
Recompensas por mantener estados emocionales positivos
"""

import pygame
from typing import Optional, Dict
from config.constantes import NEON_YELLOW, NEON_ORANGE, NEON_GREEN, WHITE


class ComboEmocional:
    """Gestiona combos y multiplicadores basados en emociones"""

    def __init__(self):
        # Estado del combo
        self.contador_combo = 0
        self.emocion_combo = None
        self.tiempo_en_emocion = 0
        self.combo_activo = False

        # Multiplicadores
        self.multiplicador_puntos = 1.0
        self.bonus_acumulado = 0

        # Umbrales de combo
        self.umbrales_combo = {
            "inicio": 3.0,  # 3 segundos para iniciar combo
            "nivel_2": 8.0,  # 8 segundos para nivel 2
            "nivel_3": 15.0,  # 15 segundos para nivel 3
            "nivel_max": 25.0,  # 25 segundos para nivel máximo
        }

        # Multiplicadores por nivel de combo
        self.multiplicadores = {
            0: 1.0,  # Sin combo
            1: 1.2,  # Combo inicial
            2: 1.5,  # Combo medio
            3: 2.0,  # Combo alto
            4: 2.5,  # Combo máximo
        }

        # Emociones que generan combo positivo
        self.emociones_positivas = ["feliz", "determinado"]

        # Emociones neutras (mantienen combo pero no lo aumentan)
        self.emociones_neutras = ["neutral"]

        # Emociones negativas (rompen combo)
        self.emociones_negativas = ["triste", "miedo", "dolor"]

        # Bonus por combo
        self.bonus_por_nivel = {1: 10, 2: 25, 3: 50, 4: 100}

        # Estadísticas
        self.combo_maximo_alcanzado = 0
        self.total_bonus_obtenido = 0

    def actualizar(self, dt: float, emocion_actual: str):
        """Actualiza el estado del combo"""
        # Verificar si la emoción actual es positiva
        if emocion_actual in self.emociones_positivas:
            if self.emocion_combo == emocion_actual or self.emocion_combo is None:
                # Continuar o iniciar combo
                self.tiempo_en_emocion += dt
                self.emocion_combo = emocion_actual
            else:
                # Cambio a otra emoción positiva - mantener tiempo parcial
                self.tiempo_en_emocion *= 0.5
                self.emocion_combo = emocion_actual

        elif emocion_actual in self.emociones_neutras:
            # Mantener combo pero decrecer lentamente
            self.tiempo_en_emocion = max(0, self.tiempo_en_emocion - dt * 0.5)

        else:
            # Emoción negativa - romper combo
            if self.combo_activo:
                self._romper_combo()
            self.tiempo_en_emocion = 0
            self.emocion_combo = None

        # Actualizar nivel de combo y multiplicador
        self._actualizar_nivel_combo()

    def _actualizar_nivel_combo(self):
        """Actualiza el nivel del combo según tiempo acumulado"""
        nivel_anterior = self.contador_combo

        if self.tiempo_en_emocion >= self.umbrales_combo["nivel_max"]:
            self.contador_combo = 4
        elif self.tiempo_en_emocion >= self.umbrales_combo["nivel_3"]:
            self.contador_combo = 3
        elif self.tiempo_en_emocion >= self.umbrales_combo["nivel_2"]:
            self.contador_combo = 2
        elif self.tiempo_en_emocion >= self.umbrales_combo["inicio"]:
            self.contador_combo = 1
        else:
            self.contador_combo = 0

        # Actualizar multiplicador
        self.multiplicador_puntos = self.multiplicadores.get(self.contador_combo, 1.0)

        # Activar combo si alcanza nivel 1
        if self.contador_combo > 0:
            self.combo_activo = True
        else:
            self.combo_activo = False

        # Registrar combo máximo
        if self.contador_combo > self.combo_maximo_alcanzado:
            self.combo_maximo_alcanzado = self.contador_combo

        # Bonus por subir de nivel
        if self.contador_combo > nivel_anterior and self.contador_combo > 0:
            bonus = self.bonus_por_nivel.get(self.contador_combo, 0)
            self.bonus_acumulado += bonus
            self.total_bonus_obtenido += bonus
            return True  # Indica que subió de nivel

        return False

    def _romper_combo(self):
        """Rompe el combo actual"""
        self.combo_activo = False
        # No resetear contador_combo inmediatamente para mostrar el último valor

    def aplicar_multiplicador(self, puntos_base: int) -> int:
        """Aplica el multiplicador actual a los puntos"""
        return int(puntos_base * self.multiplicador_puntos)

    def obtener_bonus_acumulado(self) -> int:
        """Obtiene y resetea el bonus acumulado"""
        bonus = self.bonus_acumulado
        self.bonus_acumulado = 0
        return bonus

    def obtener_nivel_combo(self) -> int:
        """Obtiene el nivel actual del combo"""
        return self.contador_combo

    def obtener_multiplicador(self) -> float:
        """Obtiene el multiplicador actual"""
        return self.multiplicador_puntos

    def obtener_progreso_siguiente_nivel(self) -> float:
        """Obtiene el progreso hacia el siguiente nivel (0.0 a 1.0)"""
        if self.contador_combo >= 4:
            return 1.0  # Nivel máximo alcanzado

        nivel_actual = self.contador_combo

        # Determinar umbrales
        if nivel_actual == 0:
            umbral_inicio = 0
            umbral_fin = self.umbrales_combo["inicio"]
        elif nivel_actual == 1:
            umbral_inicio = self.umbrales_combo["inicio"]
            umbral_fin = self.umbrales_combo["nivel_2"]
        elif nivel_actual == 2:
            umbral_inicio = self.umbrales_combo["nivel_2"]
            umbral_fin = self.umbrales_combo["nivel_3"]
        else:  # nivel_actual == 3
            umbral_inicio = self.umbrales_combo["nivel_3"]
            umbral_fin = self.umbrales_combo["nivel_max"]

        # Calcular progreso
        rango = umbral_fin - umbral_inicio
        progreso = (self.tiempo_en_emocion - umbral_inicio) / rango if rango > 0 else 0

        return max(0.0, min(1.0, progreso))

    def reiniciar(self):
        """Reinicia el sistema de combos"""
        self.contador_combo = 0
        self.emocion_combo = None
        self.tiempo_en_emocion = 0
        self.combo_activo = False
        self.multiplicador_puntos = 1.0
        self.bonus_acumulado = 0

    def obtener_estado(self) -> Dict:
        """Obtiene el estado completo del combo"""
        return {
            "nivel_combo": self.contador_combo,
            "multiplicador": self.multiplicador_puntos,
            "combo_activo": self.combo_activo,
            "tiempo_en_emocion": self.tiempo_en_emocion,
            "emocion_combo": self.emocion_combo,
            "progreso": self.obtener_progreso_siguiente_nivel(),
            "bonus_pendiente": self.bonus_acumulado,
            "combo_maximo": self.combo_maximo_alcanzado,
            "total_bonus": self.total_bonus_obtenido,
        }


class VisualizadorCombo:
    """Renderiza el estado del combo en pantalla"""

    def __init__(self):
        self.animacion_subida = 0
        self.ultimo_nivel = 0

    def dibujar(
        self,
        superficie: pygame.Surface,
        combo: ComboEmocional,
        posicion: tuple,
        fuente_grande: pygame.font.Font,
        fuente_pequena: pygame.font.Font,
    ):
        """Dibuja el indicador de combo"""
        if not combo.combo_activo:
            return

        x, y = posicion
        nivel = combo.obtener_nivel_combo()
        multiplicador = combo.obtener_multiplicador()
        progreso = combo.obtener_progreso_siguiente_nivel()

        # Animación de subida de nivel
        if nivel > self.ultimo_nivel:
            self.animacion_subida = 0.5
            self.ultimo_nivel = nivel

        if self.animacion_subida > 0:
            self.animacion_subida -= 0.016  # Aproximadamente 60 FPS

        # Color según nivel
        colores = {
            1: NEON_YELLOW,
            2: NEON_GREEN,
            3: NEON_ORANGE,
            4: (255, 50, 255),  # Magenta brillante
        }
        color = colores.get(nivel, WHITE)

        # Texto de multiplicador
        texto_multi = f"x{multiplicador:.1f}"
        surf_multi = fuente_grande.render(texto_multi, True, color)

        # Efecto de escala por animación
        if self.animacion_subida > 0:
            escala = 1.0 + self.animacion_subida * 0.5
            ancho_nuevo = int(surf_multi.get_width() * escala)
            alto_nuevo = int(surf_multi.get_height() * escala)
            surf_multi = pygame.transform.scale(surf_multi, (ancho_nuevo, alto_nuevo))

        rect_multi = surf_multi.get_rect(center=(x, y))
        superficie.blit(surf_multi, rect_multi)

        # Barra de progreso
        barra_ancho = 100
        barra_alto = 8
        barra_x = x - barra_ancho // 2
        barra_y = y + 30

        # Fondo de barra
        pygame.draw.rect(
            superficie, (50, 50, 50), (barra_x, barra_y, barra_ancho, barra_alto)
        )

        # Progreso
        progreso_ancho = int(barra_ancho * progreso)
        pygame.draw.rect(
            superficie, color, (barra_x, barra_y, progreso_ancho, barra_alto)
        )

        # Texto de combo nivel
        if nivel < 4:
            texto_nivel = f"COMBO LVL {nivel}"
        else:
            texto_nivel = "COMBO MAX!"

        surf_nivel = fuente_pequena.render(texto_nivel, True, color)
        rect_nivel = surf_nivel.get_rect(center=(x, y - 35))
        superficie.blit(surf_nivel, rect_nivel)

    def reiniciar(self):
        """Reinicia el estado del visualizador"""
        self.animacion_subida = 0
        self.ultimo_nivel = 0

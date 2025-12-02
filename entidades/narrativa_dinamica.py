"""
Sistema de Narrativa Dinámica - Fase 5
Diálogos, mensajes y frases que responden al contexto emocional
"""

import random
from typing import List, Optional, Tuple
import pygame
from config.constantes import NEON_YELLOW, NEON_BLUE, PURPLE, RED, NEON_ORANGE, WHITE


class Dialogo:
    """Representa un diálogo o mensaje individual"""

    def __init__(
        self, texto: str, duracion: float = 3.0, color: Tuple[int, int, int] = WHITE
    ):
        self.texto = texto
        self.duracion = duracion
        self.tiempo_restante = duracion
        self.color = color
        self.alpha = 255

    def actualizar(self, dt: float) -> bool:
        """Actualiza el diálogo. Retorna False cuando expira"""
        self.tiempo_restante -= dt

        # Fade out en el último segundo
        if self.tiempo_restante < 1.0:
            self.alpha = int(255 * self.tiempo_restante)

        return self.tiempo_restante > 0

    def obtener_color_alpha(self) -> Tuple[int, int, int, int]:
        """Obtiene color con transparencia"""
        return (*self.color[:3], max(0, min(255, self.alpha)))


class NarrativaDinamica:
    """Sistema de narrativa que responde a emociones y eventos"""

    def __init__(self):
        self.dialogo_actual: Optional[Dialogo] = None
        self.cola_dialogos: List[Dialogo] = []
        self.cooldown_dialogo = 0

        # Biblioteca de frases por contexto
        self.frases = {
            # Emociones positivas
            "feliz_inicio": [
                "¡Qué bien me siento hoy!",
                "Esto va a ser divertido",
                "¡Vamos allá!",
                "Me encanta este desafío",
            ],
            "feliz_progreso": [
                "¡Excelente! Voy bien",
                "Esto es genial",
                "¡Sigue así!",
                "Me siento imparable",
            ],
            # Emociones negativas
            "triste_inicio": [
                "Esto se ve difícil...",
                "No estoy seguro de esto",
                "Qué complicado...",
                "Ojalá pueda lograrlo",
            ],
            "triste_progreso": [
                "Sigo intentándolo",
                "Poco a poco...",
                "No me rendiré",
                "Aunque sea difícil, seguiré",
            ],
            # Miedo
            "miedo_peligro": [
                "¡Cuidado con eso!",
                "Esto da miedo...",
                "¡Viene hacia mí!",
                "¡Tengo que esquivarlo!",
            ],
            "miedo_escape": [
                "¡Por poco!",
                "Eso estuvo cerca",
                "¡Qué susto!",
                "Casi no lo cuento",
            ],
            # Dolor
            "dolor_dano": [
                "¡Auch! Eso dolió",
                "¡No de nuevo!",
                "Esto duele...",
                "¡Ay! Me lastimé",
            ],
            "dolor_persistente": [
                "Aguanta un poco más",
                "Puedo superarlo",
                "El dolor pasará",
                "Debo resistir",
            ],
            # Determinación
            "determinado_inicio": [
                "¡Esta vez lo lograré!",
                "Nada me detendrá",
                "¡Voy con todo!",
                "Estoy listo para esto",
            ],
            "determinado_esfuerzo": [
                "¡No me rendiré!",
                "¡Puedo hacerlo!",
                "¡Casi lo tengo!",
                "¡Un esfuerzo más!",
            ],
            # Eventos de juego
            "nivel_completado": [
                "¡Lo logré!",
                "¡Nivel superado!",
                "¡Sí! ¡Lo hice!",
                "¡Éxito total!",
            ],
            "nivel_fallido": [
                "La próxima vez será mejor",
                "Aprenderé de esto",
                "No importa, lo intentaré de nuevo",
                "Puedo mejorar",
            ],
            "powerup_obtenido": [
                "¡Genial! Un poder extra",
                "Esto me ayudará",
                "¡Justo lo que necesitaba!",
                "¡Perfecto!",
            ],
            "combo_alto": [
                "¡Combo increíble!",
                "¡Estoy en racha!",
                "¡Imparable!",
                "¡Esto es asombroso!",
            ],
            "pista_usada": [
                "Veamos... esto podría ayudar",
                "Una pequeña ayuda no está mal",
                "A ver si esto aclara las cosas",
                "Necesito orientación",
            ],
            "meteoro_esquivado": [
                "¡Eso estuvo cerca!",
                "¡Justo a tiempo!",
                "Reflejos perfectos",
                "¡Ni me tocó!",
            ],
            "portal_usado": [
                "¡Qué sensación extraña!",
                "¡Teletransportación exitosa!",
                "Esto es fascinante",
                "¡Viaje dimensional!",
            ],
            # Motivación general
            "motivacion_generica": [
                "Tú puedes con esto",
                "Confía en ti mismo",
                "Cada intento cuenta",
                "El esfuerzo vale la pena",
                "Sigue adelante",
            ],
            # Tutoriales contextuales
            "tutorial_movimiento": [
                "Usa las flechas o WASD para mover",
                "Explora el espacio con cuidado",
            ],
            "tutorial_piezas": [
                "Arrastra las piezas a su lugar",
                "Cada pieza tiene su espacio perfecto",
            ],
            "tutorial_emociones": [
                "Tus emociones afectan el juego",
                "Mantén la calma para mejores resultados",
            ],
        }

        # Colores por tipo de mensaje
        self.colores_mensaje = {
            "feliz": NEON_YELLOW,
            "triste": NEON_BLUE,
            "miedo": PURPLE,
            "dolor": RED,
            "determinado": NEON_ORANGE,
            "sistema": WHITE,
            "exito": NEON_YELLOW,
            "fracaso": NEON_BLUE,
        }

    def mostrar_dialogo(
        self, clave_frase: str, tipo_color: str = "sistema", duracion: float = 3.0
    ):
        """Muestra un diálogo aleatorio de una categoría"""
        if self.cooldown_dialogo > 0:
            return

        frases_disponibles = self.frases.get(clave_frase, [])
        if not frases_disponibles:
            return

        texto = random.choice(frases_disponibles)
        color = self.colores_mensaje.get(tipo_color, WHITE)

        dialogo = Dialogo(texto, duracion, color)

        # Si hay diálogo activo, agregar a cola
        if self.dialogo_actual and self.dialogo_actual.tiempo_restante > 0.5:
            self.cola_dialogos.append(dialogo)
        else:
            self.dialogo_actual = dialogo

        # Cooldown de 2 segundos entre diálogos
        self.cooldown_dialogo = 2.0

    def reaccionar_emocion(self, emocion: str, contexto: str = "inicio"):
        """Muestra diálogo según emoción y contexto"""
        clave = f"{emocion}_{contexto}"

        # Determinar tipo de color según emoción
        tipo_color = emocion if emocion in self.colores_mensaje else "sistema"

        self.mostrar_dialogo(clave, tipo_color, duracion=2.5)

    def reaccionar_evento(self, evento: str):
        """Muestra diálogo para un evento específico"""
        tipo_color = "sistema"

        # Determinar color según evento
        if evento in ["nivel_completado", "combo_alto", "powerup_obtenido"]:
            tipo_color = "exito"
        elif evento in ["nivel_fallido"]:
            tipo_color = "fracaso"

        self.mostrar_dialogo(evento, tipo_color, duracion=3.0)

    def actualizar(self, dt: float):
        """Actualiza el estado de los diálogos"""
        # Actualizar cooldown
        if self.cooldown_dialogo > 0:
            self.cooldown_dialogo -= dt

        # Actualizar diálogo actual
        if self.dialogo_actual:
            if not self.dialogo_actual.actualizar(dt):
                # Diálogo expirado, pasar al siguiente en cola
                if self.cola_dialogos:
                    self.dialogo_actual = self.cola_dialogos.pop(0)
                else:
                    self.dialogo_actual = None

    def dibujar(
        self,
        superficie: pygame.Surface,
        fuente: pygame.font.Font,
        posicion: Tuple[int, int] = None,
    ):
        """Dibuja el diálogo actual"""
        if not self.dialogo_actual:
            return

        # Posición por defecto (centro superior)
        if posicion is None:
            posicion = (superficie.get_width() // 2, 80)

        # Renderizar texto con transparencia
        texto_surf = fuente.render(self.dialogo_actual.texto, True, WHITE)
        texto_rect = texto_surf.get_rect(center=posicion)

        # Fondo semi-transparente
        padding = 15
        fondo_rect = texto_rect.inflate(padding * 2, padding)
        fondo_surf = pygame.Surface(
            (fondo_rect.width, fondo_rect.height), pygame.SRCALPHA
        )
        fondo_surf.fill((0, 0, 0, 180))
        superficie.blit(fondo_surf, fondo_rect.topleft)

        # Texto con color emocional
        color_alpha = self.dialogo_actual.obtener_color_alpha()
        texto_color_surf = fuente.render(
            self.dialogo_actual.texto, True, color_alpha[:3]
        )

        # Aplicar alpha al texto
        texto_color_surf.set_alpha(color_alpha[3])

        superficie.blit(texto_color_surf, texto_rect)

    def limpiar(self):
        """Limpia todos los diálogos"""
        self.dialogo_actual = None
        self.cola_dialogos.clear()
        self.cooldown_dialogo = 0

    def tiene_dialogo_activo(self) -> bool:
        """Verifica si hay un diálogo mostrándose"""
        return self.dialogo_actual is not None

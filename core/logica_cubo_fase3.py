"""
Lógica del juego CUBO: Arquitecto del Caos - Fase 3
Sistema de puntuación, múltiples niveles y pistas
"""

import pygame
import random
import time
import math
import json
import os
from config.constantes import *
from entidades.cubo import Cubo
from entidades.pieza_geometrica import PiezaGeometrica, FiguraObjetivo
from entidades.sistema_particulas import ParticleSystem
from core.logica_cubo_fase2 import GameCuboFase2


class SistemaPuntuacion:
    """Sistema de puntuación basado en tiempo y precisión"""

    def __init__(self, tiempo_limite):
        self.tiempo_limite = tiempo_limite
        self.puntos_base = 1000
        self.bonus_tiempo_max = 500
        self.bonus_precision_max = 300
        self.bonus_sin_errores = 200

    def calcular_puntuacion(
        self, tiempo_usado, intentos_fallidos, piezas_usadas, piezas_necesarias
    ):
        """
        Calcula la puntuación final basada en múltiples factores

        Args:
            tiempo_usado: Tiempo que tomó completar el nivel (segundos)
            intentos_fallidos: Número de intentos fallidos de colocación
            piezas_usadas: Número de piezas utilizadas
            piezas_necesarias: Número mínimo de piezas necesarias

        Returns:
            dict con desglose de puntuación
        """
        puntos = self.puntos_base

        # Bonus por tiempo (más rápido = más puntos)
        tiempo_restante = max(0, self.tiempo_limite - tiempo_usado)
        porcentaje_tiempo = tiempo_restante / self.tiempo_limite
        bonus_tiempo = int(self.bonus_tiempo_max * porcentaje_tiempo)

        # Bonus por precisión (usar solo las piezas necesarias)
        piezas_extra = max(0, piezas_usadas - piezas_necesarias)
        precision = max(0, 1 - (piezas_extra * 0.2))  # -20% por cada pieza extra
        bonus_precision = int(self.bonus_precision_max * precision)

        # Bonus por no cometer errores
        bonus_sin_errores = 0 if intentos_fallidos > 0 else self.bonus_sin_errores

        # Penalización por intentos fallidos
        penalizacion_intentos = intentos_fallidos * 25

        puntos_total = int(
            puntos
            + bonus_tiempo
            + bonus_precision
            + bonus_sin_errores
            - penalizacion_intentos
        )
        puntos_total = max(0, puntos_total)  # No permitir puntuación negativa

        return {
            "puntos_base": puntos,
            "bonus_tiempo": bonus_tiempo,
            "bonus_precision": bonus_precision,
            "bonus_sin_errores": bonus_sin_errores,
            "penalizacion_intentos": penalizacion_intentos,
            "puntos_total": puntos_total,
            "tiempo_usado": tiempo_usado,
            "intentos_fallidos": intentos_fallidos,
        }


class SistemaPistas:
    """Sistema de pistas/ayudas para el jugador"""

    def __init__(self, max_pistas=3):
        self.max_pistas = max_pistas
        self.pistas_usadas = 0
        self.pista_activa = None
        self.tiempo_pista = 0
        self.duracion_pista = 5.0  # Segundos que dura visible una pista
        self.penalizacion_puntos = 100  # Puntos que cuesta usar una pista

    def puede_usar_pista(self):
        """Verifica si aún hay pistas disponibles"""
        return self.pistas_usadas < self.max_pistas

    def usar_pista_siguiente_pieza(self, piezas, figura_objetivo):
        """
        Muestra una pista sobre la siguiente pieza a colocar

        Returns:
            dict con información de la pista o None
        """
        if not self.puede_usar_pista():
            return None

        # Encontrar piezas ya colocadas
        piezas_colocadas = [p for p in piezas if p.colocada]

        # Determinar cuál es la siguiente pieza necesaria
        siguiente_pieza = None
        for definicion in figura_objetivo.definicion:
            # Verificar si ya hay una pieza de este tipo colocada
            tipo_necesario = definicion["tipo"]
            ya_colocada = any(p.tipo == tipo_necesario for p in piezas_colocadas)

            if not ya_colocada:
                # Buscar una pieza de este tipo que no esté colocada
                for pieza in piezas:
                    if pieza.tipo == tipo_necesario and not pieza.colocada:
                        siguiente_pieza = pieza
                        break
                break

        if siguiente_pieza:
            self.pistas_usadas += 1
            self.pista_activa = {
                "tipo": "siguiente_pieza",
                "pieza": siguiente_pieza,
                "mensaje": f"Intenta colocar el {self._nombre_tipo(siguiente_pieza.tipo)}",
            }
            self.tiempo_pista = self.duracion_pista
            return self.pista_activa

        return None

    def usar_pista_posicion(self, figura_objetivo):
        """Muestra la posición exacta donde debe ir la siguiente pieza"""
        if not self.puede_usar_pista():
            return None

        self.pistas_usadas += 1
        self.pista_activa = {
            "tipo": "posicion",
            "figura": figura_objetivo,
            "mensaje": "Posición objetivo resaltada",
        }
        self.tiempo_pista = self.duracion_pista
        return self.pista_activa

    def update(self, dt):
        """Actualiza el temporizador de la pista activa"""
        if self.tiempo_pista > 0:
            self.tiempo_pista -= dt
            if self.tiempo_pista <= 0:
                self.pista_activa = None

    def _nombre_tipo(self, tipo):
        """Convierte el tipo de pieza en nombre legible"""
        nombres = {
            PiezaGeometrica.CUADRADO: "cuadrado",
            PiezaGeometrica.TRIANGULO: "triángulo",
            PiezaGeometrica.CIRCULO: "círculo",
            PiezaGeometrica.ROMBO: "rombo",
            PiezaGeometrica.RECTANGULO: "rectángulo",
        }
        return nombres.get(tipo, "pieza")

    def get_penalizacion_total(self):
        """Retorna la penalización total por usar pistas"""
        return self.pistas_usadas * self.penalizacion_puntos


class GeneradorNiveles:
    """Genera configuraciones de niveles con complejidad creciente"""

    def __init__(self):
        """Carga los niveles desde el archivo JSON"""
        self.niveles_config = self._cargar_niveles()

    def _cargar_niveles(self):
        """Carga la configuración de niveles desde el JSON"""
        try:
            niveles_path = os.path.join("config", "niveles.json")
            with open(niveles_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["niveles"]
        except Exception as e:
            print(f"Error al cargar niveles.json: {e}")
            return {}

    def _convertir_tipo_pieza(self, tipo_str):
        """Convierte el string del tipo de pieza a la constante correspondiente"""
        tipos_mapa = {
            "CUADRADO": PiezaGeometrica.CUADRADO,
            "TRIANGULO": PiezaGeometrica.TRIANGULO,
            "CIRCULO": PiezaGeometrica.CIRCULO,
            "ROMBO": PiezaGeometrica.ROMBO,
            "RECTANGULO": PiezaGeometrica.RECTANGULO,
        }
        return tipos_mapa.get(tipo_str, PiezaGeometrica.CUADRADO)

    def obtener_definicion_nivel(self, nivel_numero):
        """
        Retorna la definición de figuras objetivo según el nivel

        Args:
            nivel_numero: Número del nivel (1-3)

        Returns:
            list de definiciones de piezas
        """
        nivel_key = str(nivel_numero)

        # Si el nivel existe en el JSON, usarlo
        if nivel_key in self.niveles_config:
            config = self.niveles_config[nivel_key]
            definicion = []
            for pieza_config in config["piezas"]:
                definicion.append(
                    {
                        "tipo": self._convertir_tipo_pieza(pieza_config["tipo"]),
                        "posicion": pieza_config["posicion"],
                    }
                )
            return definicion

        # Fallback: generar nivel aleatorio para niveles no definidos
        return self._generar_nivel_aleatorio(nivel_numero)

    def _generar_nivel_aleatorio(self, nivel_numero):
        """Genera un nivel aleatorio para niveles no definidos en el JSON"""
        num_piezas = min(3 + nivel_numero // 2, 8)  # Más piezas en niveles altos
        tipos_disponibles = [
            PiezaGeometrica.CUADRADO,
            PiezaGeometrica.TRIANGULO,
            PiezaGeometrica.CIRCULO,
            PiezaGeometrica.ROMBO,
            PiezaGeometrica.RECTANGULO,
        ]
        posiciones = ["centro", "arriba", "abajo", "izquierda", "derecha"]

        definicion = []

        # Para mayor variedad, crear una lista mezclada de tipos
        tipos_a_usar = []
        if num_piezas >= 5:
            tipos_a_usar = tipos_disponibles.copy()
            while len(tipos_a_usar) < num_piezas:
                tipos_a_usar.append(random.choice(tipos_disponibles))
        else:
            tipos_a_usar = [random.choice(tipos_disponibles) for _ in range(num_piezas)]

        random.shuffle(tipos_a_usar)

        for i in range(num_piezas):
            definicion.append(
                {
                    "tipo": tipos_a_usar[i],
                    "posicion": posiciones[i % len(posiciones)],
                }
            )

        return definicion

    def calcular_piezas_distractor(self, nivel_numero):
        """Calcula cuántas piezas distractor agregar según nivel"""
        base_distractors = 3

        # Agregar más distractores en niveles altos
        extra_por_nivel = nivel_numero // 2

        return base_distractors + extra_por_nivel


class GameCuboFase3(GameCuboFase2):
    """Fase 3: Validación avanzada, puntuación y múltiples niveles"""

    def __init__(self, screen, level_number, player, config=None, audio=None):
        # Inicializar generador de niveles
        self.generador_niveles = GeneradorNiveles()
        self.nivel_numero = level_number

        # Llamar al constructor padre
        super().__init__(screen, level_number, player, config, audio)

        # Sistema de puntuación
        self.sistema_puntuacion = SistemaPuntuacion(self.time_limit)

        # Sistema de pistas
        self.sistema_pistas = SistemaPistas(max_pistas=3)

        # Métricas de rendimiento
        self.intentos_fallidos = 0
        self.piezas_usadas_total = 0
        self.piezas_necesarias = len(self.figura_objetivo.definicion)

        # Resultados finales
        self.resultado_puntuacion = None

        # Estado de espera para confirmación
        self.esperando_confirmacion = False

        # Actualizar mensaje de fase
        self.fase_mensaje = f"FASE 3: NIVEL {level_number}"

    def _crear_figura_objetivo(self):
        """Crea la figura objetivo según el nivel actual"""
        definicion = self.generador_niveles.obtener_definicion_nivel(self.nivel_numero)

        # Posicionar objetivo en la esquina superior derecha
        objetivo_x = SCREEN_WIDTH - 150
        objetivo_y = 150
        return FiguraObjetivo(objetivo_x, objetivo_y, definicion)

    def _generar_piezas_para_objetivo(self):
        """Genera piezas con distractores según el nivel"""
        # Calcular número de distractores
        num_distractores = self.generador_niveles.calcular_piezas_distractor(
            self.nivel_numero
        )

        # Llamar al método padre pero con número personalizado de distractores
        margen = 100
        posiciones_usadas = []

        def obtener_posicion_libre():
            intentos = 0
            while intentos < 100:
                x = random.randint(margen, SCREEN_WIDTH - margen - 200)
                y = random.randint(margen, SCREEN_HEIGHT - margen)

                muy_cerca = False
                for px, py in posiciones_usadas:
                    distancia = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                    if distancia < 60:
                        muy_cerca = True
                        break

                if not muy_cerca:
                    posiciones_usadas.append((x, y))
                    return x, y

                intentos += 1

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
        """Maneja la entrada incluyendo las teclas de pistas"""
        # Llamar al método padre para movimiento básico
        super().handle_input(keys, event)

        # Eventos adicionales para pistas
        if event and event.type == pygame.KEYDOWN:
            # Pista de siguiente pieza (tecla H)
            if event.key == pygame.K_h:
                pista = self.sistema_pistas.usar_pista_siguiente_pieza(
                    self.piezas, self.figura_objetivo
                )
                if pista:
                    self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 1.0)

            # Pista de posición (tecla J)
            elif event.key == pygame.K_j:
                pista = self.sistema_pistas.usar_pista_posicion(self.figura_objetivo)
                if pista:
                    self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 1.0)

    def _intentar_soltar_pieza(self):
        """Sobrescribe el método para contar intentos fallidos"""
        # Guardar estado previo
        piezas_colocadas_antes = sum(1 for p in self.piezas if p.colocada)

        # Llamar al método padre
        super()._intentar_soltar_pieza()

        # Verificar si fue exitoso
        piezas_colocadas_despues = sum(1 for p in self.piezas if p.colocada)

        if piezas_colocadas_despues > piezas_colocadas_antes:
            # Éxito: se colocó una pieza
            self.piezas_usadas_total += 1
        else:
            # Fallo: no se pudo colocar
            self.intentos_fallidos += 1

    def update(self, dt=None):
        """Actualiza el juego y sistemas adicionales"""
        # Calcular dt si no se proporciona (necesario para sistema de pistas)
        if dt is None:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            dt = min(dt, 0.1)

        # Actualizar sistema de pistas siempre
        self.sistema_pistas.update(dt)

        # Si estamos esperando confirmación, solo actualizar animaciones
        if self.esperando_confirmacion:

            # Actualizar solo elementos visuales
            self.cubo.update(dt)
            for pieza in self.piezas:
                pieza.update(dt)
            self.particle_system.update()
            self.breathe_offset += dt
            return False  # No terminar el nivel

        # Llamar al método padre
        resultado = super().update(dt)

        # Si el nivel se completó, calcular puntuación
        if self.completed and self.resultado_puntuacion is None:
            # Restar penalización por pistas
            self.resultado_puntuacion = self.sistema_puntuacion.calcular_puntuacion(
                self.time_elapsed,
                self.intentos_fallidos,
                self.piezas_usadas_total,
                self.piezas_necesarias,
            )
            # Aplicar penalización de pistas
            penalizacion_pistas = self.sistema_pistas.get_penalizacion_total()
            self.resultado_puntuacion["puntos_total"] -= penalizacion_pistas
            self.resultado_puntuacion["puntos_total"] = max(
                0, self.resultado_puntuacion["puntos_total"]
            )
            self.resultado_puntuacion["pistas_usadas"] = (
                self.sistema_pistas.pistas_usadas
            )
            self.resultado_puntuacion["penalizacion_pistas"] = penalizacion_pistas

        return resultado

    def draw(self):
        """Dibuja el juego con información adicional"""
        # Llamar al método padre para dibujo básico
        super().draw()

        # Dibujar pista activa si existe
        if self.sistema_pistas.pista_activa:
            self._dibujar_pista_activa()

        # Dibujar métricas de rendimiento (incluye pistas)
        self._dibujar_metricas()

        # Dibujar resultado de puntuación si está disponible
        if self.resultado_puntuacion:
            self._dibujar_resultado_puntuacion()

    def _dibujar_pista_activa(self):
        """Dibuja la pista activa en pantalla"""
        pista = self.sistema_pistas.pista_activa

        if pista["tipo"] == "siguiente_pieza":
            # Resaltar la pieza con un brillo pulsante
            pieza = pista["pieza"]
            pulso = abs(math.sin(time.time() * 5)) * 20 + 10

            # Círculo brillante alrededor de la pieza
            pygame.draw.circle(
                self.screen,
                (255, 255, 0, 150),
                (int(pieza.x), int(pieza.y)),
                int(pieza.tamano + pulso),
                3,
            )

            # Flecha apuntando a la pieza
            flecha_y = int(pieza.y - pieza.tamano - 40)
            pygame.draw.polygon(
                self.screen,
                NEON_YELLOW,
                [
                    (int(pieza.x), int(pieza.y - pieza.tamano - 20)),
                    (int(pieza.x - 10), flecha_y),
                    (int(pieza.x + 10), flecha_y),
                ],
            )

        elif pista["tipo"] == "posicion":
            # Resaltar la zona objetivo completa
            figura = pista["figura"]
            pulso = abs(math.sin(time.time() * 4)) * 15 + 5

            # Dibujar contorno brillante alrededor del objetivo
            objetivo_rect = pygame.Rect(figura.x - 100, figura.y - 100, 200, 200)

            # Efecto de glow
            for i in range(3):
                grosor = 3 - i
                alfa = int(150 - i * 50)
                s = pygame.Surface(
                    (objetivo_rect.width + pulso * 2, objetivo_rect.height + pulso * 2),
                    pygame.SRCALPHA,
                )
                pygame.draw.rect(
                    s, (*NEON_GREEN[:3], alfa), s.get_rect(), grosor, border_radius=15
                )
                self.screen.blit(s, (objetivo_rect.x - pulso, objetivo_rect.y - pulso))

        # Mostrar mensaje de la pista
        mensaje = pista["mensaje"]
        texto_pista = self.font.render(mensaje, True, NEON_YELLOW)

        # Fondo para el mensaje
        padding = 20
        mensaje_rect = texto_pista.get_rect(center=(SCREEN_WIDTH // 2, 50))
        fondo_rect = mensaje_rect.inflate(padding * 2, padding)

        s = pygame.Surface((fondo_rect.width, fondo_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 200), s.get_rect(), border_radius=10)
        pygame.draw.rect(s, NEON_YELLOW, s.get_rect(), 2, border_radius=10)
        self.screen.blit(s, fondo_rect.topleft)
        self.screen.blit(texto_pista, mensaje_rect)

    def _dibujar_metricas(self):
        """Dibuja métricas de rendimiento en tiempo real"""
        # Posición en la parte superior izquierda
        y_offset = 100

        # Fondo semi-transparente - Aumentar altura para incluir pistas
        metricas_rect = pygame.Rect(10, y_offset, 280, 145)
        s = pygame.Surface((metricas_rect.width, metricas_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 180), s.get_rect(), border_radius=10)
        self.screen.blit(s, metricas_rect.topleft)

        # Título
        texto_titulo = self.font_small.render("RENDIMIENTO", True, NEON_CYAN)
        self.screen.blit(texto_titulo, (20, y_offset + 5))

        # Métricas
        y = y_offset + 35

        # Nivel
        texto_nivel = self.font_small.render(
            f"Nivel: {self.nivel_numero}", True, NEON_PURPLE
        )
        self.screen.blit(texto_nivel, (20, y))
        y += 25

        # Piezas usadas vs necesarias
        color_piezas = (
            NEON_GREEN
            if self.piezas_usadas_total <= self.piezas_necesarias
            else NEON_ORANGE
        )
        texto_piezas = self.font_small.render(
            f"Piezas: {self.piezas_usadas_total}/{self.piezas_necesarias}",
            True,
            color_piezas,
        )
        self.screen.blit(texto_piezas, (20, y))
        y += 25

        # Intentos fallidos
        color_intentos = NEON_GREEN if self.intentos_fallidos == 0 else NEON_ORANGE
        texto_intentos = self.font_small.render(
            f"Errores: {self.intentos_fallidos}", True, color_intentos
        )
        self.screen.blit(texto_intentos, (20, y))
        y += 25

        # Pistas restantes
        pistas_restantes = (
            self.sistema_pistas.max_pistas - self.sistema_pistas.pistas_usadas
        )
        color_pistas = NEON_GREEN if pistas_restantes > 0 else GRAY
        texto_pistas = self.font_small.render(
            f"Pistas: {pistas_restantes}/3 (H/J)", True, color_pistas
        )
        self.screen.blit(texto_pistas, (20, y))
        y += 25

        # Vida del cubo (si tiene el sistema de impactos)
        if hasattr(self.cubo, "impactos_recibidos"):
            vida_restante = self.cubo.max_impactos - self.cubo.impactos_recibidos
            color_vida = (
                NEON_GREEN
                if vida_restante >= 2
                else NEON_ORANGE if vida_restante == 1 else NEON_PINK
            )
            texto_vida = self.font_small.render(
                f"Vidas: {vida_restante}/{self.cubo.max_impactos}", True, color_vida
            )
            self.screen.blit(texto_vida, (20, y))

    def _dibujar_resultado_puntuacion(self):
        """Dibuja el resultado final de puntuación"""
        # Solo mostrar si hay resultado de puntuación
        if not self.resultado_puntuacion:
            return

        resultado = self.resultado_puntuacion

        # Panel central semi-transparente
        panel_width = 500
        panel_height = 400
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2

        # Fondo del panel (opaco para ocultar elementos del juego)
        s = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 255), s.get_rect(), border_radius=20)
        pygame.draw.rect(s, NEON_CYAN, s.get_rect(), 3, border_radius=20)
        self.screen.blit(s, (panel_x, panel_y))

        y = panel_y + 20

        # Título
        texto_titulo = self.font_large.render("¡NIVEL COMPLETADO!", True, NEON_GREEN)
        titulo_rect = texto_titulo.get_rect(center=(SCREEN_WIDTH // 2, y + 30))
        self.screen.blit(texto_titulo, titulo_rect)
        y += 80

        # Desglose de puntuación
        detalles = [
            (f"Puntos base:", f"+{resultado['puntos_base']}", GRAY),
            (f"Bonus tiempo:", f"+{resultado['bonus_tiempo']}", NEON_GREEN),
            (f"Bonus precisión:", f"+{resultado['bonus_precision']}", NEON_CYAN),
            (f"Sin errores:", f"+{resultado['bonus_sin_errores']}", NEON_PURPLE),
            (f"Penalización:", f"-{resultado['penalizacion_intentos']}", NEON_ORANGE),
        ]

        if resultado.get("pistas_usadas", 0) > 0:
            detalles.append(
                (f"Pistas usadas:", f"-{resultado['penalizacion_pistas']}", NEON_ORANGE)
            )

        for concepto, valor, color in detalles:
            texto_concepto = self.font_small.render(concepto, True, color)
            texto_valor = self.font_small.render(valor, True, color)
            self.screen.blit(texto_concepto, (panel_x + 30, y))
            valor_rect = texto_valor.get_rect(right=panel_x + panel_width - 30)
            valor_rect.y = y
            self.screen.blit(texto_valor, valor_rect)
            y += 30

        # Línea separadora
        pygame.draw.line(
            self.screen,
            NEON_CYAN,
            (panel_x + 30, y + 5),
            (panel_x + panel_width - 30, y + 5),
            2,
        )
        y += 20

        # Puntuación total
        texto_total = self.font.render("PUNTUACIÓN TOTAL:", True, NEON_CYAN)
        texto_puntos = self.font_large.render(
            str(resultado["puntos_total"]), True, NEON_GREEN
        )
        self.screen.blit(texto_total, (panel_x + 30, y))
        puntos_rect = texto_puntos.get_rect(right=panel_x + panel_width - 30)
        puntos_rect.y = y - 5
        self.screen.blit(texto_puntos, puntos_rect)

        # Mensaje para continuar (solo si está esperando confirmación)
        if self.esperando_confirmacion:
            y += 50
            # Efecto parpadeante
            import time

            alpha = int(128 + 127 * abs((time.time() * 2) % 2 - 1))
            texto_continuar = self.font_small.render(
                "Presiona ENTER para continuar", True, NEON_PINK
            )
            continuar_rect = texto_continuar.get_rect(center=(SCREEN_WIDTH // 2, y))

            # Crear superficie con alpha para efecto parpadeante
            continuar_surface = pygame.Surface(
                texto_continuar.get_size(), pygame.SRCALPHA
            )
            continuar_surface.fill((0, 0, 0, 0))
            temp_text = self.font_small.render(
                "Presiona ENTER para continuar", True, NEON_PINK
            )
            continuar_surface.blit(temp_text, (0, 0))
            continuar_surface.set_alpha(alpha)
            self.screen.blit(continuar_surface, continuar_rect)

    def get_resultado_nivel(self):
        """Retorna el resultado del nivel para guardarlo"""
        return {
            "nivel": self.nivel_numero,
            "completado": self.completed,
            "puntuacion": (
                self.resultado_puntuacion["puntos_total"]
                if self.resultado_puntuacion
                else 0
            ),
            "tiempo_usado": self.time_elapsed,
            "intentos_fallidos": self.intentos_fallidos,
            "pistas_usadas": self.sistema_pistas.pistas_usadas,
        }

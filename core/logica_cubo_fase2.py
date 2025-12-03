"""
Lógica del juego CUBO: Arquitecto del Caos - Fase 2
Sistema de piezas geométricas y magnetismo
"""

import pygame
import random
import time
import math
from config.constantes import *
from entidades.cubo import Cubo
from entidades.pieza_geometrica import PiezaGeometrica, FiguraObjetivo
from entidades.sistema_particulas import ParticleSystem


class GameCuboFase2:
    """Clase principal del juego CUBO - Fase 2: Piezas y magnetismo"""

    def __init__(self, screen, level_number, player, config=None, audio=None):
        self.screen = screen
        self.player = player
        self.config = config
        self.audio = audio
        self.level_number = level_number

        self.font = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        self.font_large = pygame.font.Font(None, 60)

        # Crear CUBO en posición inicial
        self.cubo = Cubo(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Sistema de partículas
        self.particle_system = ParticleSystem(screen)

        # Crear figura objetivo primero (para saber qué piezas necesitamos)
        self.figura_objetivo = self._crear_figura_objetivo()

        # Generar piezas basadas en el objetivo + piezas adicionales
        self.piezas = []
        self._generar_piezas_para_objetivo()

        # Sistema de magnetismo
        self.radio_atraccion = 80  # Radio de atracción magnética
        self.fuerza_magnetica = 5  # Intensidad del magnetismo

        # Estado del juego
        self.completed = False
        self.failed = False
        self.start_time = time.time()
        self.last_update_time = self.start_time  # Para calcular dt
        self.time_limit = TIME_LIMIT
        self.time_remaining = self.time_limit
        self.time_elapsed = 0  # Tiempo transcurrido desde el inicio

        # Progreso de construcción
        self.porcentaje_completitud = 0.0
        self.completion_delay = 0  # Retraso antes de terminar el nivel
        self.completion_delay_duration = (
            2.0  # 2 segundos para ver la construcción completa
        )

        # Animación de fondo
        self.breathe_offset = 0

    def _generar_piezas_para_objetivo(self):
        """Genera las piezas necesarias para el objetivo más piezas adicionales"""
        margen = 100
        posiciones_usadas = []

        # Función auxiliar para obtener una posición no ocupada
        def obtener_posicion_libre():
            intentos = 0
            while intentos < 500:  # Aumentado de 100 a 500 para mejor distribución
                x = random.randint(
                    margen, SCREEN_WIDTH - margen - 200
                )  # Evitar zona del objetivo
                y = random.randint(margen, SCREEN_HEIGHT - margen)

                # Verificar que no esté muy cerca de otras piezas
                muy_cerca = False
                for px, py in posiciones_usadas:
                    distancia = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                    if distancia < 60:  # Mínimo 60 píxeles de separación
                        muy_cerca = True
                        break

                if not muy_cerca:
                    posiciones_usadas.append((x, y))
                    return x, y

                intentos += 1

            # Si no se encuentra posición, retornar una aleatoria
            x = random.randint(margen, SCREEN_WIDTH - margen - 200)
            y = random.randint(margen, SCREEN_HEIGHT - margen)
            posiciones_usadas.append((x, y))
            return x, y

        # 1. Generar las piezas NECESARIAS para completar el objetivo
        piezas_necesarias = {}
        for pieza_esperada in self.figura_objetivo.piezas_esperadas:
            tipo = pieza_esperada["tipo"]
            piezas_necesarias[tipo] = piezas_necesarias.get(tipo, 0) + 1

        for tipo, cantidad in piezas_necesarias.items():
            for _ in range(cantidad):
                x, y = obtener_posicion_libre()
                pieza = PiezaGeometrica(x, y, tipo)
                self.piezas.append(pieza)

        # 2. Generar piezas ADICIONALES (distractores)
        num_distractores = 3  # Cantidad fija de distractores

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

    def _crear_figura_objetivo(self):
        """Crea la figura objetivo que debe construirse"""
        # Ejemplo: una casa simple (cuadrado + triángulo arriba)
        definicion = [
            {"tipo": PiezaGeometrica.CUADRADO, "posicion": "centro"},
            {"tipo": PiezaGeometrica.TRIANGULO, "posicion": "arriba"},
            {"tipo": PiezaGeometrica.RECTANGULO, "posicion": "abajo"},
        ]

        # Posicionar objetivo en la esquina superior derecha
        objetivo_x = SCREEN_WIDTH - 150
        objetivo_y = 150
        return FiguraObjetivo(objetivo_x, objetivo_y, definicion)

    def handle_input(self, keys, event=None):
        """Maneja la entrada del jugador para controlar a CUBO"""
        if self.completed or self.failed:
            return

        # Movimiento de CUBO (WASD o flechas) - solo si keys no es None
        if keys is not None:
            moving = False

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.cubo.mover("arriba")
                moving = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.cubo.mover("abajo")
                moving = True

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.cubo.mover("izquierda")
                moving = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.cubo.mover("derecha")
                moving = True

            # Si no hay teclas presionadas, detener
            if not moving:
                self.cubo.detener()

        # Eventos de teclado
        if event and event.type == pygame.KEYDOWN:
            # Recoger pieza más cercana (tecla E)
            if event.key == pygame.K_e:
                self._intentar_recoger_pieza()

            # Soltar pieza en zona de atracción (tecla Q)
            elif event.key == pygame.K_q:
                self._intentar_soltar_pieza()

            # Cambios de emoción para testing (teclas 1-5)
            elif event.key == pygame.K_1:
                self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 2.0)
            elif event.key == pygame.K_2:
                self.cubo.cambiar_emocion(Cubo.EMOCION_TRISTE, 2.0)
            elif event.key == pygame.K_3:
                self.cubo.cambiar_emocion(Cubo.EMOCION_MIEDO, 2.0)
            elif event.key == pygame.K_4:
                self.cubo.cambiar_emocion(Cubo.EMOCION_DOLOR, 2.0)
            elif event.key == pygame.K_5:
                self.cubo.cambiar_emocion(Cubo.EMOCION_DETERMINADO, 2.0)

    def _intentar_recoger_pieza(self):
        """Intenta recoger la pieza más cercana"""
        # Buscar zona de atracción libre
        zona_libre = None

        for nombre_zona, zona in self.cubo.zonas_atraccion.items():
            if not zona["ocupada"]:
                # Seleccionar la primera zona libre
                zona_libre = nombre_zona
                break

        if not zona_libre:
            self.cubo.cambiar_emocion(Cubo.EMOCION_TRISTE, 1.0)
            return

        # Buscar pieza más cercana a CUBO
        pieza_cercana = None
        distancia_minima = float("inf")

        for pieza in self.piezas:
            if not pieza.siendo_arrastrada and not pieza.colocada:
                distancia = pieza.distancia_a(
                    self.cubo.position[0], self.cubo.position[1]
                )
                if distancia < self.radio_atraccion and distancia < distancia_minima:
                    distancia_minima = distancia
                    pieza_cercana = pieza

        if pieza_cercana:
            # Recoger la pieza
            self.cubo.atraer_pieza(pieza_cercana, zona_libre)
            pieza_cercana.siendo_arrastrada = True

            # Efectos visuales mejorados al recoger
            # Ráfaga de partículas del color de la pieza
            self.particle_system.emit_burst(
                pieza_cercana.x,
                pieza_cercana.y,
                color=pieza_cercana.color,
                count=15,
                spread=3.0,
            )
            # Partículas blancas brillantes
            self.particle_system.emit_burst(
                pieza_cercana.x,
                pieza_cercana.y,
                color=(255, 255, 255),
                count=10,
                spread=2.0,
            )
            # Efecto de glow alrededor
            self.particle_system.emit_glow(
                pieza_cercana.x,
                pieza_cercana.y,
                color=pieza_cercana.color,
                radius=40,
                count=8,
            )

            # Emoción feliz
            self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 1.0)
        else:
            # No hay piezas cerca
            self.cubo.cambiar_emocion(Cubo.EMOCION_TRISTE, 0.5)

    def _intentar_soltar_pieza(self):
        """Intenta soltar una pieza en la zona objetivo"""
        # Verificar si hay piezas en las zonas de atracción
        for nombre_zona, zona in self.cubo.zonas_atraccion.items():
            if zona["ocupada"] and zona["pieza"] is not None:
                pieza = zona["pieza"]

                # Soltar la pieza
                self.cubo.soltar_pieza(nombre_zona)
                pieza.siendo_arrastrada = False

                # Verificar si está cerca de una posición objetivo
                colocada_correctamente = False
                for pieza_esperada in self.figura_objetivo.piezas_esperadas:
                    # Verificar tipo y distancia
                    if pieza.tipo == pieza_esperada["tipo"]:
                        distancia = pieza.distancia_a(
                            pieza_esperada["x"], pieza_esperada["y"]
                        )
                        if distancia < 50:  # Tolerancia generosa
                            # VALIDACIÓN: Verificar que no haya otra pieza ya colocada en esa posición
                            posicion_ocupada = False
                            for otra_pieza in self.piezas:
                                if otra_pieza != pieza and otra_pieza.colocada:
                                    dist_a_objetivo = otra_pieza.distancia_a(
                                        pieza_esperada["x"], pieza_esperada["y"]
                                    )
                                    if dist_a_objetivo < 30:  # Espacio ya ocupado
                                        posicion_ocupada = True
                                        break

                            if posicion_ocupada:
                                # Rechazar colocación - efecto de error
                                pieza.snap_to_grid()
                                self.particle_system.emit_burst(
                                    pieza.x,
                                    pieza.y,
                                    color=(255, 0, 0),
                                    count=10,
                                    spread=2.0,
                                )
                                self.cubo.cambiar_emocion(Cubo.EMOCION_TRISTE, 1.0)
                                colocada_correctamente = False
                                break

                            # Snap a la posición objetivo
                            pieza.mover_a(pieza_esperada["x"], pieza_esperada["y"])
                            pieza.colocada = True
                            colocada_correctamente = True

                            # Efectos visuales espectaculares al colocar correctamente
                            # Explosión de partículas verdes
                            self.particle_system.emit_burst(
                                pieza.x,
                                pieza.y,
                                color=(0, 255, 0),
                                count=30,
                                spread=4.0,
                            )
                            # Anillo de partículas doradas
                            for i in range(12):
                                angle = (i / 12) * 2 * math.pi
                                offset_x = math.cos(angle) * 30
                                offset_y = math.sin(angle) * 30
                                self.particle_system.emit_spark(
                                    pieza.x + offset_x,
                                    pieza.y + offset_y,
                                    color=(255, 215, 0),
                                    velocity_base=(offset_x * 0.1, offset_y * 0.1),
                                )
                            # Brillo intenso
                            self.particle_system.emit_glow(
                                pieza.x,
                                pieza.y,
                                color=(255, 255, 255),
                                radius=60,
                                count=15,
                            )
                            self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 1.5)
                            break

                if not colocada_correctamente:
                    # Pieza soltada fuera del objetivo - efecto sutil
                    pieza.snap_to_grid()
                    # Pequeño efecto de partículas grises
                    self.particle_system.emit_burst(
                        pieza.x, pieza.y, color=(150, 150, 150), count=5, spread=1.5
                    )
                    self.cubo.cambiar_emocion(Cubo.EMOCION_NEUTRAL, 0.5)

                # Solo soltar una pieza a la vez
                return

        # No hay piezas para soltar
        self.cubo.cambiar_emocion(Cubo.EMOCION_TRISTE, 0.5)

    def _aplicar_magnetismo(self):
        """Aplica fuerzas magnéticas entre piezas y zonas de atracción"""
        for pieza in self.piezas:
            if pieza.siendo_arrastrada:
                # Las piezas arrastradas siguen a CUBO
                for nombre_zona, zona in self.cubo.zonas_atraccion.items():
                    if zona["ocupada"] and zona["pieza"] == pieza:
                        # Calcular posición absoluta de la zona
                        zona_x = self.cubo.position[0] + zona["offset"][0]
                        zona_y = self.cubo.position[1] + zona["offset"][1]
                        # Mover pieza a la zona de atracción
                        pieza.mover_a(zona_x, zona_y)
                        break

    def update(self, dt=None):
        """Actualiza el estado del juego

        Args:
            dt: Delta time en segundos. Si es None, se calcula automáticamente.
        """
        # Calcular dt si no se proporciona
        if dt is None:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            # Limitar dt para evitar saltos grandes
            dt = min(dt, 0.1)

        # Si estamos en retraso de completitud, contar hacia abajo
        if self.completion_delay > 0:
            self.completion_delay -= dt
            if self.completion_delay <= 0:
                return True  # Terminar el nivel después del retraso
            # Seguir actualizando mientras esperamos para mostrar efectos
            self.cubo.update(dt)
            for pieza in self.piezas:
                pieza.update(dt)
            self.particle_system.update()
            return False

        if self.completed or self.failed:
            return True  # Retornar True para indicar que el juego terminó

        # Actualizar CUBO
        self.cubo.update(dt)

        # Actualizar piezas
        for pieza in self.piezas:
            pieza.update(dt)

        # Aplicar magnetismo
        self._aplicar_magnetismo()

        # Actualizar partículas
        self.particle_system.update()

        # Actualizar tiempo PRIMERO
        self.time_elapsed = time.time() - self.start_time
        self.time_remaining = self.time_limit - self.time_elapsed

        # Verificar si se acabó el tiempo
        if self.time_remaining <= 0 and not self.failed and not self.completed:
            self.failed = True
            self.time_remaining = 0  # Evitar valores negativos
            self.cubo.cambiar_emocion(Cubo.EMOCION_TRISTE, 5.0)
            # Activar delay también para fallos, para mostrar animación
            self.completion_delay = 1.5  # 1.5 segundos para ver el fallo

        # Solo verificar completitud si el juego no ha fallado
        if not self.failed:
            piezas_colocadas = [p for p in self.piezas if p.colocada]
            completa, porcentaje = self.figura_objetivo.verificar_completitud(
                piezas_colocadas
            )
            self.porcentaje_completitud = porcentaje

            if completa and not self.completed:
                self.completed = True
                self.completion_delay = (
                    self.completion_delay_duration
                )  # Iniciar retraso
                self.cubo.cambiar_emocion(Cubo.EMOCION_FELIZ, 5.0)

                # Guardar progreso del jugador
                self.player.complete_level(
                    self.nivel_numero,
                    0,  # attempts_used obsoleto, siempre 0
                    self.time_elapsed,
                )

        # Animación de fondo
        self.breathe_offset += dt

        # Retornar True si el juego terminó (completado o fallado)
        return self.completed or self.failed

    def draw(self):
        """Dibuja el juego en pantalla"""
        # Fondo con efecto de respiración
        self._draw_background()

        # Dibujar figura objetivo
        self.figura_objetivo.draw(self.screen, alpha=120)

        # Dibujar piezas
        for pieza in self.piezas:
            pieza.draw(self.screen)

        # Dibujar partículas
        self.particle_system.draw()

        # Dibujar CUBO (encima de todo)
        self.cubo.draw(self.screen)

        # UI
        self._draw_ui()

    def _draw_background(self):
        """Dibuja el fondo con grilla animada"""
        self.screen.fill(BG_DARK)

        # Grilla con efecto de respiración suave
        respiracion = int(10 * (0.5 + 0.5 * math.sin(self.breathe_offset)))

        grid_size = 40
        for x in range(0, SCREEN_WIDTH, grid_size):
            color = (30 + respiracion, 30 + respiracion, 40 + respiracion)
            pygame.draw.line(self.screen, color, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            color = (30 + respiracion, 30 + respiracion, 40 + respiracion)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y), 1)

    def _draw_ui(self):
        """Dibuja la interfaz de usuario"""
        # Barra superior con información
        info_height = 60
        pygame.draw.rect(self.screen, (20, 20, 30), (0, 0, SCREEN_WIDTH, info_height))
        pygame.draw.line(
            self.screen,
            (100, 100, 120),
            (0, info_height),
            (SCREEN_WIDTH, info_height),
            2,
        )

        # Tiempo restante
        minutos = int(self.time_remaining // 60)
        segundos = int(self.time_remaining % 60)
        tiempo_texto = f"Tiempo: {minutos:02d}:{segundos:02d}"
        texto_tiempo = self.font_small.render(tiempo_texto, True, (255, 255, 255))
        self.screen.blit(texto_tiempo, (20, 15))

        # Porcentaje de completitud
        completitud_texto = f"Progreso: {self.porcentaje_completitud:.0f}%"
        texto_completitud = self.font_small.render(completitud_texto, True, NEON_GREEN)
        self.screen.blit(texto_completitud, (SCREEN_WIDTH // 2 - 80, 15))

        # Emoción actual
        emocion_texto = f"Estado: {self.cubo.emocion_actual.upper()}"
        texto_emocion = self.font_small.render(emocion_texto, True, NEON_YELLOW)
        self.screen.blit(texto_emocion, (SCREEN_WIDTH - 200, 15))

        # Instrucciones (panel inferior)
        instrucciones = [
            "WASD/Flechas: Mover",
            "E: Recoger pieza",
            "Q: Soltar pieza",
        ]
        y_offset = SCREEN_HEIGHT - 100
        for i, instruccion in enumerate(instrucciones):
            texto = self.font_small.render(instruccion, True, (255, 255, 255))
            self.screen.blit(texto, (20, y_offset + i * 25))

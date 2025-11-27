"""
Lógica principal del juego y transformaciones
"""

import pygame
import numpy as np
import time
from constantes import *
from sistema_niveles import get_level
from sistema_particulas import ParticleSystem, MovementTrailEffect
from entidades_juego import ZONE_TYPE_OBSTACLE, ZONE_TYPE_DISTORTION, ZONE_TYPE_GRAVITY


class Game:
    """Clase principal del juego que maneja la lógica del puzzle"""

    def __init__(self, screen, level_number, difficulty, player):
        self.screen = screen
        self.level = get_level(level_number, difficulty)
        self.player = player
        self.font = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        self.font_large = pygame.font.Font(None, 60)

        # Estado de la forma del jugador
        self.shape_vertices = self.level.get_shape_vertices().copy()
        self.position = [300.0, 400.0]  # Posición inicial
        self.rotation = 0.0
        self.scale = 1.0

        # Estado de feedback visual
        self.shake_intensity = 0.0
        self.stress_level = 0.0  # 0.0 a 1.0, indica qué tan "forzada" está la figura
        self.in_distortion = False
        self.proximity_factor = 0.0  # 0.0 (lejos) a 1.0 (encaje perfecto)

        # Contador de movimientos
        self.moves_count = 0
        self.moves_remaining = self.player.global_moves
        self.last_transform = None

        # Temporizador
        self.start_time = time.time()
        self.time_remaining = self.level.time_limit
        self.time_elapsed = 0

        # Estado del juego
        self.completed = False
        self.failed = False
        self.fail_reason = ""  # "time", "moves", "obstacle"

        # Animación de respiración
        self.breathe_offset = 0

        # Sistema de partículas
        self.particle_system = ParticleSystem(screen)
        self.trail_effect = MovementTrailEffect(self.particle_system)
        self.last_particle_pos = self.position.copy()

    def draw_tessellation(self):
        """Dibuja el teselado de fondo con efecto respiración Cyberpunk"""
        pattern = self.level.grid_pattern

        # Calcular intensidad de respiración
        breathe = BREATHE_MIN + (BREATHE_MAX - BREATHE_MIN) * (
            0.5 + 0.5 * np.sin(self.breathe_offset)
        )

        if pattern == "square":
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                    is_even = (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0
                    base_color = BG_GRID_1 if is_even else BG_GRID_2

                    # Aplicar efecto respiración
                    color = tuple(int(c * breathe) for c in base_color)

                    pygame.draw.rect(self.screen, color, (x, y, TILE_SIZE, TILE_SIZE))
                    # Borde neón
                    pygame.draw.rect(
                        self.screen,
                        tuple(int(c * 0.3) for c in NEON_CYAN),
                        (x, y, TILE_SIZE, TILE_SIZE),
                        1,
                    )

        elif pattern == "hexagonal":
            hex_size = TILE_SIZE
            for row in range(-1, SCREEN_HEIGHT // hex_size + 2):
                for col in range(-1, SCREEN_WIDTH // hex_size + 2):
                    x = col * hex_size * 1.5
                    y = row * hex_size * np.sqrt(3) + (
                        hex_size * np.sqrt(3) / 2 if col % 2 else 0
                    )
                    is_even = (row + col) % 2 == 0
                    base_color = BG_GRID_1 if is_even else BG_GRID_2
                    color = tuple(int(c * breathe) for c in base_color)

                    self.draw_hexagon(x, y, hex_size * 0.5, color, NEON_PURPLE)

        elif pattern == "triangular":
            for x in range(0, SCREEN_WIDTH, TILE_SIZE):
                for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                    points1 = [(x, y), (x + TILE_SIZE, y), (x, y + TILE_SIZE)]
                    points2 = [
                        (x + TILE_SIZE, y),
                        (x + TILE_SIZE, y + TILE_SIZE),
                        (x, y + TILE_SIZE),
                    ]
                    color1 = tuple(int(c * breathe) for c in BG_GRID_1)
                    color2 = tuple(int(c * breathe) for c in BG_GRID_2)

                    pygame.draw.polygon(self.screen, color1, points1)
                    pygame.draw.polygon(self.screen, color2, points2)
                    pygame.draw.polygon(
                        self.screen, tuple(int(c * 0.3) for c in NEON_PINK), points1, 1
                    )
                    pygame.draw.polygon(
                        self.screen, tuple(int(c * 0.3) for c in NEON_PINK), points2, 1
                    )

    def draw_hexagon(self, cx, cy, radius, color, border_color):
        """Dibuja un hexágono con borde neón"""
        points = []
        for i in range(6):
            angle = i * np.pi / 3
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(
            self.screen, tuple(int(c * 0.3) for c in border_color), points, 1
        )

    def transform_shape(self, vertices, position, rotation, scale):
        """Aplica transformaciones a los vértices de la forma"""
        # Escalar
        scaled = vertices * scale

        # Rotar
        angle_rad = np.radians(rotation)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
        rotated = np.dot(scaled, rotation_matrix.T)

        # Trasladar
        translated = rotated + position

        return translated

    def draw_shape(self, vertices, position, rotation, scale, color, width=0):
        """Dibuja una forma con las transformaciones aplicadas y efecto 3D"""

        # Aplicar "Shake" (temblor) a la posición visual si hay intensidad
        visual_pos = list(position)
        if self.shake_intensity > 0.1:
            offset_x = (np.random.random() - 0.5) * self.shake_intensity
            offset_y = (np.random.random() - 0.5) * self.shake_intensity
            visual_pos[0] += offset_x
            visual_pos[1] += offset_y

        transformed = self.transform_shape(vertices, visual_pos, rotation, scale)
        points = [(int(p[0]), int(p[1])) for p in transformed]

        if width == 0:  # Forma rellena con profundidad
            # Modificar color basado en estrés o proximidad
            draw_color = list(color)

            # Si hay mucho estrés (rotación rápida/distorsión), mezclar con rojo/naranja
            if self.stress_level > 0.1:
                factor = min(1.0, self.stress_level)
                # Mezclar hacia COLOR_WARNING
                for i in range(3):
                    draw_color[i] = int(
                        draw_color[i] * (1 - factor) + COLOR_WARNING[i] * factor
                    )

            # Si está muy cerca del objetivo, mezclar con verde brillante
            if self.proximity_factor > 0.5:
                factor = (self.proximity_factor - 0.5) * 2  # 0 a 1
                for i in range(3):
                    draw_color[i] = int(
                        draw_color[i] * (1 - factor) + COLOR_SUCCESS_GLOW[i] * factor
                    )

            draw_color = tuple(draw_color)

            # Dibujar capas de sombra para efecto 3D
            for layer in range(GLOW_LAYERS, 0, -1):
                offset = layer * 3
                shadow_points = [(p[0] + offset, p[1] + offset) for p in points]
                shadow_color = tuple(
                    int(c * 0.2 * layer / GLOW_LAYERS) for c in draw_color
                )
                pygame.draw.polygon(self.screen, shadow_color, shadow_points)

            # Forma principal
            pygame.draw.polygon(self.screen, draw_color, points)

            # Borde brillante neón
            for glow in range(GLOW_LAYERS):
                glow_color = tuple(
                    min(255, int(c * (1 + glow * 0.3))) for c in draw_color
                )
                pygame.draw.polygon(self.screen, glow_color, points, GLOW_LAYERS - glow)
        else:
            # Solo contorno con glow
            for glow in range(GLOW_LAYERS):
                glow_color = tuple(min(255, int(c * (0.5 + glow * 0.3))) for c in color)
                pygame.draw.polygon(self.screen, glow_color, points, width + glow)

    def draw_target(self):
        """Dibuja la forma objetivo con efecto neón"""
        target_vertices = self.level.get_shape_vertices()
        self.draw_shape(
            target_vertices,
            self.level.target_position,
            self.level.target_rotation,
            self.level.target_scale,
            NEON_GREEN,
            width=3,
        )

        # Dibujar zonas del nivel (obstáculos, distorsiones, etc.)
        if hasattr(self.level, "zones"):
            for zone in self.level.zones:
                zone.draw(self.screen)

    def draw_player_shape(self):
        """Dibuja la forma del jugador con efecto 3D"""
        color = NEON_CYAN if not self.completed else NEON_YELLOW
        self.draw_shape(
            self.shape_vertices, self.position, self.rotation, self.scale, color
        )

    def draw_ui(self):
        """Dibuja la interfaz de usuario con estilo Cyberpunk"""
        # Información del nivel con glow
        level_text = self.font.render(
            f"NIVEL {self.level.level_number} - {self.level.difficulty.upper()}",
            True,
            NEON_PINK,
        )
        # Efecto glow en texto
        for offset in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            glow_text = self.font.render(
                f"NIVEL {self.level.level_number} - {self.level.difficulty.upper()}",
                True,
                tuple(int(c * 0.3) for c in NEON_PINK),
            )
            self.screen.blit(glow_text, (20 + offset[0], 20 + offset[1]))
        self.screen.blit(level_text, (20, 20))

        # Movimientos
        moves_color = NEON_ORANGE if self.moves_remaining < 5 else NEON_CYAN
        moves_text = self.font.render(
            f"MOVIMIENTOS: {self.moves_remaining}",
            True,
            moves_color,
        )
        self.screen.blit(moves_text, (20, 70))

        # Temporizador
        time_color = NEON_ORANGE if self.time_remaining < 20 else NEON_GREEN
        minutes = int(self.time_remaining) // 60
        seconds = int(self.time_remaining) % 60
        time_text = self.font.render(
            f"TIEMPO: {minutes:02d}:{seconds:02d}", True, time_color
        )
        self.screen.blit(time_text, (20, 120))

        # Instrucciones con estilo neón
        instructions = [
            "WASD: MOVER",
            "Q/E: ROTAR",
            "RUEDA/ZX: ESCALAR",
            "ESPACIO: VERIFICAR",
            "ESC: SALIR",
        ]

        for i, inst in enumerate(instructions):
            text = self.font_small.render(inst, True, NEON_PURPLE)
            self.screen.blit(text, (SCREEN_WIDTH - 220, 20 + i * 35))

        # Mensajes de estado
        if self.completed:
            for offset in range(5, 0, -1):
                glow = self.font_large.render(
                    "¡NIVEL COMPLETADO!", True, tuple(int(c * 0.2) for c in NEON_GREEN)
                )
                glow_rect = glow.get_rect(
                    center=(SCREEN_WIDTH // 2 + offset, SCREEN_HEIGHT - 100 + offset)
                )
                self.screen.blit(glow, glow_rect)

            msg = self.font_large.render("¡NIVEL COMPLETADO!", True, NEON_GREEN)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(msg, msg_rect)

            stats = self.font.render(
                f"Movimientos: {self.moves_count} | Tiempo: {self.time_elapsed:.1f}s",
                True,
                NEON_CYAN,
            )
            stats_rect = stats.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(stats, stats_rect)

        elif self.failed:
            msg_text = (
                "TIEMPO AGOTADO" if self.fail_reason == "time" else "SIN MOVIMIENTOS"
            )

            for offset in range(5, 0, -1):
                glow = self.font_large.render(
                    msg_text, True, tuple(int(c * 0.2) for c in NEON_PINK)
                )
                glow_rect = glow.get_rect(
                    center=(SCREEN_WIDTH // 2 + offset, SCREEN_HEIGHT - 100 + offset)
                )
                self.screen.blit(glow, glow_rect)

            msg = self.font_large.render(msg_text, True, NEON_PINK)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(msg, msg_rect)

            retry = self.font.render("Movimientos reiniciados", True, NEON_ORANGE)
            retry_rect = retry.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(retry, retry_rect)

    def handle_input(self, keys, event=None):
        """Maneja la entrada del jugador"""
        if self.completed or self.failed:
            return

        moved = False
        transform_type = None

        # Manejo de eventos discretos (Rueda del mouse)
        if event and event.type == pygame.MOUSEWHEEL:
            scale_factor = SCALE_SPEED * 2  # Doble velocidad para la rueda
            if event.y > 0:  # Scroll arriba -> Agrandar
                self.scale = min(3.0, self.scale + scale_factor)
                moved = True
                transform_type = "scale"
            elif event.y < 0:  # Scroll abajo -> Achicar
                self.scale = max(0.1, self.scale - scale_factor)
                moved = True
                transform_type = "scale"

        if keys:
            # Traslación
            if keys[pygame.K_w]:
                self.position[1] -= TRANSLATION_SPEED
                moved = True
                transform_type = "translation"
            if keys[pygame.K_s]:
                self.position[1] += TRANSLATION_SPEED
                moved = True
                transform_type = "translation"
            if keys[pygame.K_a]:
                self.position[0] -= TRANSLATION_SPEED
                moved = True
                transform_type = "translation"
            if keys[pygame.K_d]:
                self.position[0] += TRANSLATION_SPEED
                moved = True
                transform_type = "translation"

            # Rotación
            if keys[pygame.K_q]:
                self.rotation -= ROTATION_SPEED
                moved = True
                transform_type = "rotation"
                self.shake_intensity = min(MAX_SHAKE, self.shake_intensity + 0.5)
                self.stress_level = min(1.0, self.stress_level + 0.1)
            if keys[pygame.K_e]:
                self.rotation += ROTATION_SPEED
                moved = True
                transform_type = "rotation"
                self.shake_intensity = min(MAX_SHAKE, self.shake_intensity + 0.5)
                self.stress_level = min(1.0, self.stress_level + 0.1)

            # Escala (Teclas)
            if keys[pygame.K_z]:
                self.scale = max(0.1, self.scale - SCALE_SPEED)
                moved = True
                transform_type = "scale"
                self.stress_level = min(1.0, self.stress_level + 0.05)
            if keys[pygame.K_x]:
                self.scale = min(3.0, self.scale + SCALE_SPEED)
                moved = True
                transform_type = "scale"
                self.stress_level = min(1.0, self.stress_level + 0.05)

        # Contar movimiento solo si cambió el tipo de transformación
        if moved and transform_type != self.last_transform:
            self.moves_count += 1
            self.player.global_moves -= 1
            self.moves_remaining = self.player.global_moves
            self.last_transform = transform_type

            # Emitir efecto de contacto al cambiar tipo de transformación
            self.trail_effect.emit_contact_effect(
                self.position[0], self.position[1], NEON_CYAN
            )

            if self.player.global_moves <= 0:
                self.failed = True
                self.fail_reason = "moves"
        elif not moved:
            self.last_transform = None

    def check_completion(self):
        """Verifica si la forma está correctamente encajada"""
        # Verificar si está en zona prohibida (obstáculo)
        if hasattr(self.level, "zones"):
            current_vertices = self.transform_shape(
                self.shape_vertices, self.position, self.rotation, self.scale
            )
            for zone in self.level.zones:
                if zone.type == ZONE_TYPE_OBSTACLE and zone.check_collision_polygon(
                    current_vertices
                ):
                    # No se puede completar si se toca un obstáculo
                    # Feedback visual de error
                    self.particle_system.emit_burst(
                        self.position[0],
                        self.position[1],
                        COLOR_DANGER,
                        count=10,
                        spread=5.0,
                    )
                    return False

        # Verificar posición
        pos_diff = np.linalg.norm(
            np.array(self.position) - np.array(self.level.target_position)
        )

        # Verificar rotación (normalizar a 0-360)
        rot_diff = abs((self.rotation % 360) - (self.level.target_rotation % 360))
        rot_diff = min(rot_diff, 360 - rot_diff)

        # Verificar escala
        scale_diff = abs(self.scale - self.level.target_scale)

        # Tolerancias
        if pos_diff < SNAP_TOLERANCE and rot_diff < 5 and scale_diff < 0.1:
            self.completed = True
            self.time_elapsed = time.time() - self.start_time
            self.player.complete_level(
                self.level.level_number,
                self.level.difficulty,
                self.moves_count,
                self.time_elapsed,
            )
            return True

        return False

    def update(self):
        """Actualiza el estado del juego"""
        # Actualizar animación de respiración
        self.breathe_offset += BREATHE_SPEED

        # Actualizar zonas y aplicar efectos
        self.in_distortion = False
        if hasattr(self.level, "zones"):
            # Calcular vértices actuales para colisiones precisas
            current_vertices = self.transform_shape(
                self.shape_vertices, self.position, self.rotation, self.scale
            )

            for zone in self.level.zones:
                zone.update()
                # Verificar colisión con la zona
                if zone.check_collision_polygon(current_vertices):
                    effect_result = zone.apply_effect(self)

                    # Si es un obstáculo mortal
                    if zone.type == ZONE_TYPE_OBSTACLE and effect_result:
                        self.failed = True
                        self.fail_reason = "obstacle"
                        # Efecto de destrucción
                        self.particle_system.emit_burst(
                            self.position[0],
                            self.position[1],
                            COLOR_DANGER,
                            count=20,
                            spread=8.0,
                        )

        # Decaer efectos visuales (shake, stress)
        self.shake_intensity = max(0, self.shake_intensity * SHAKE_DECAY)
        self.stress_level = max(0, self.stress_level - 0.05)

        # Calcular proximidad para feedback visual
        self._calculate_proximity()

        # Actualizar temporizador
        if not self.completed and not self.failed:
            elapsed = time.time() - self.start_time
            self.time_remaining = max(0, self.level.time_limit - elapsed)

            if self.time_remaining <= 0:
                self.failed = True
                self.fail_reason = "time"

        # Actualizar rastro de partículas basado en movimiento
        current_pos = np.array(self.position)
        last_pos = np.array(self.last_particle_pos)
        if np.linalg.norm(current_pos - last_pos) > 0.5:
            color = NEON_CYAN if not self.completed else NEON_YELLOW
            # Cambiar color del rastro si hay distorsión o peligro
            if self.in_distortion:
                color = NEON_PURPLE

            self.trail_effect.update_position(self.position[0], self.position[1], color)
            self.last_particle_pos = self.position.copy()

        # Actualizar partículas
        self.particle_system.update()

        self.screen.fill(BG_DARK)
        self.draw_tessellation()
        self.draw_target()
        self.particle_system.draw()  # Dibujar partículas debajo de la forma del jugador
        self.draw_player_shape()
        self.draw_ui()

        # Efecto especial al completar
        if self.completed:
            # Emitir ráfaga de celebración
            if np.random.random() < 0.3:
                colors = [NEON_YELLOW, NEON_PINK, NEON_GREEN, NEON_CYAN]
                chosen_color = colors[np.random.randint(0, len(colors))]
                self.particle_system.emit_burst(
                    self.position[0],
                    self.position[1],
                    chosen_color,
                    count=5,
                    spread=4.0,
                )

        return self.completed or self.failed

    def _calculate_proximity(self):
        """Calcula qué tan cerca está el jugador de la solución para feedback visual"""
        pos_diff = np.linalg.norm(
            np.array(self.position) - np.array(self.level.target_position)
        )
        rot_diff = abs((self.rotation % 360) - (self.level.target_rotation % 360))
        rot_diff = min(rot_diff, 360 - rot_diff)
        scale_diff = abs(self.scale - self.level.target_scale)

        # Normalizar diferencias a un valor 0-1 (1 es muy cerca)
        # Asumimos rangos máximos razonables para la normalización
        p_score = max(0, 1 - pos_diff / 200)
        r_score = max(0, 1 - rot_diff / 45)
        s_score = max(0, 1 - scale_diff / 0.5)

        # Promedio ponderado
        self.proximity_factor = p_score * 0.4 + r_score * 0.3 + s_score * 0.3

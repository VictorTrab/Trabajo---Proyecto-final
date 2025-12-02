"""
Sistema de menús del juego con estilo Cyberpunk
"""

import pygame
import numpy as np
from config.constantes import *


class Menu:
    """Clase para manejar los menús del juego"""

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 80)
        self.font_menu = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        self.selected_option = 0

        # Flag para identificar el tipo de menú actual
        self.menu_type = "main"  # Valores: "main", "level_select", etc.

        # Animaciones
        self.breathe_offset = 0
        self.mouse_pos = (0, 0)
        self.wave_time = 0

        # Animación 3D del título
        self.title_pulse_time = 0
        self.title_scale = 1.0
        self.title_rotation = 0

        # Animación de opciones del menú
        self.menu_option_time = 0

    def draw_animated_background(self):
        """Dibuja teselado animado con efecto respiración y onda al cursor"""
        # Limpiar pantalla completamente primero
        self.screen.fill(BG_DARK)

        # Actualizar animaciones
        self.breathe_offset += BREATHE_SPEED
        self.wave_time += WAVE_SPEED
        self.mouse_pos = pygame.mouse.get_pos()

        # Intensidad de respiración
        breathe = BREATHE_MIN + (BREATHE_MAX - BREATHE_MIN) * (
            0.5 + 0.5 * np.sin(self.breathe_offset)
        )

        # Dibujar teselado hexagonal
        hex_size = TILE_SIZE
        for row in range(-1, SCREEN_HEIGHT // hex_size + 2):
            for col in range(-1, SCREEN_WIDTH // hex_size + 2):
                x = col * hex_size * 1.5
                y = row * hex_size * np.sqrt(3) + (
                    hex_size * np.sqrt(3) / 2 if col % 2 else 0
                )

                # Distancia al cursor para efecto onda
                dist = np.sqrt(
                    (x - self.mouse_pos[0]) ** 2 + (y - self.mouse_pos[1]) ** 2
                )
                wave_effect = 0

                if dist < WAVE_RADIUS:
                    # Efecto onda sinusoidal
                    wave_effect = (1 - dist / WAVE_RADIUS) * np.sin(
                        dist * 0.05 - self.wave_time * 2
                    )

                # Color base con respiración y onda
                is_even = (row + col) % 2 == 0
                base_color = BG_GRID_1 if is_even else BG_GRID_2
                intensity = breathe + wave_effect * 0.3
                color = tuple(int(min(255, max(0, c * intensity))) for c in base_color)

                # Color de borde con efecto onda
                if dist < WAVE_RADIUS:
                    border_intensity = 0.5 + wave_effect
                    border_color = tuple(
                        int(min(255, c * border_intensity)) for c in NEON_CYAN
                    )
                else:
                    border_color = tuple(int(c * 0.2) for c in NEON_PURPLE)

                self.draw_hexagon(x, y, hex_size * 0.5, color, border_color)

    def draw_hexagon(self, cx, cy, radius, color, border_color):
        """Dibuja un hexágono con borde neón"""
        points = []
        for i in range(6):
            angle = i * np.pi / 3
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append((x, y))

        # Asegurar que los colores sean válidos
        color = tuple(int(max(0, min(255, c))) for c in color)
        border_color = tuple(int(max(0, min(255, c))) for c in border_color)

        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, border_color, points, 1)

    def draw_3d_pulse_title(self, text, base_font_size, color, center_pos):
        """Dibuja título con efecto 3D Pulse Scale Animation"""
        # Actualizar animación de pulso (velocidad aumentada)
        self.title_pulse_time += 0.12

        # Escala pulsante más suave (oscila entre 0.96 y 1.04)
        pulse = np.sin(self.title_pulse_time) * 0.04
        self.title_scale = 1.0 + pulse

        # Rotación más suave
        self.title_rotation = np.sin(self.title_pulse_time * 0.7) * 2.5  # ±2.5 grados

        # Crear fuente escalada
        scaled_size = int(base_font_size * self.title_scale)
        scaled_font = pygame.font.Font(None, scaled_size)

        # Renderizar texto principal
        text_surface = scaled_font.render(text, True, color)

        # Rotar el texto con interpolación suave (rotozoom es más fluido que rotate)
        rotated_surface = pygame.transform.rotozoom(
            text_surface, self.title_rotation, 1.0
        )

        # Efecto 3D: capas de profundidad (reducidas y más sutiles)
        num_depth_layers = 6
        for layer in range(num_depth_layers, 0, -1):
            depth_offset_x = int(layer * 2 * np.cos(np.radians(45)))
            depth_offset_y = int(layer * 2 * np.sin(np.radians(45)))

            # Color de profundidad más oscuro
            depth_alpha = 0.15 * (num_depth_layers - layer) / num_depth_layers
            depth_color = tuple(int(c * depth_alpha) for c in color)

            depth_surface = scaled_font.render(text, True, depth_color)
            depth_rotated = pygame.transform.rotozoom(
                depth_surface, self.title_rotation, 1.0
            )
            depth_rect = depth_rotated.get_rect(
                center=(center_pos[0] + depth_offset_x, center_pos[1] + depth_offset_y)
            )
            self.screen.blit(depth_rotated, depth_rect)

        # Glow neón (solo 4 direcciones, más sutil)
        glow_layers = 3
        for glow in range(glow_layers, 0, -1):
            glow_intensity = 0.2 * glow / glow_layers
            glow_color = tuple(int(c * glow_intensity) for c in color)

            # Glow en 4 direcciones principales
            for angle in [0, 90, 180, 270]:
                offset_x = int(glow * 2 * np.cos(np.radians(angle)))
                offset_y = int(glow * 2 * np.sin(np.radians(angle)))

                glow_surface = scaled_font.render(text, True, glow_color)
                glow_rotated = pygame.transform.rotozoom(
                    glow_surface, self.title_rotation, 1.0
                )
                glow_rect = glow_rotated.get_rect(
                    center=(center_pos[0] + offset_x, center_pos[1] + offset_y)
                )
                self.screen.blit(glow_rotated, glow_rect)

        # Texto principal
        main_rect = rotated_surface.get_rect(center=center_pos)
        self.screen.blit(rotated_surface, main_rect)

    def draw_text_with_glow(self, text, font, color, center_pos, depth_3d=False):
        """Dibuja texto con efecto glow neón y opcionalmente efecto 3D"""
        if depth_3d:
            # Efecto 3D: múltiples capas con offset para simular profundidad
            num_depth_layers = 8
            for layer in range(num_depth_layers, 0, -1):
                depth_offset = layer * 2
                depth_alpha = 0.15 * (num_depth_layers - layer) / num_depth_layers
                depth_color = tuple(int(c * depth_alpha) for c in color)

                depth_text = font.render(text, True, depth_color)
                depth_rect = depth_text.get_rect(
                    center=(center_pos[0] + depth_offset, center_pos[1] + depth_offset)
                )
                self.screen.blit(depth_text, depth_rect)

        # Capas de glow
        for offset in range(GLOW_LAYERS, 0, -1):
            glow_color = tuple(int(c * 0.3 * offset / GLOW_LAYERS) for c in color)
            for dx, dy in [
                (offset, offset),
                (-offset, offset),
                (offset, -offset),
                (-offset, -offset),
            ]:
                glow_text = font.render(text, True, glow_color)
                glow_rect = glow_text.get_rect(
                    center=(center_pos[0] + dx, center_pos[1] + dy)
                )
                self.screen.blit(glow_text, glow_rect)

        # Texto principal
        main_text = font.render(text, True, color)
        main_rect = main_text.get_rect(center=center_pos)
        self.screen.blit(main_text, main_rect)

    def draw_main_menu(self):
        """Dibuja el menú principal"""
        self.menu_type = "main"  # Establecer tipo de menú
        self.draw_animated_background()

        # Actualizar animación de opciones (x3 más rápida)
        self.menu_option_time += 0.2

        # Título con efecto 3D Pulse Scale Animation
        self.draw_3d_pulse_title("CUBO", 240, NEON_PINK, (SCREEN_WIDTH // 2, 150))

        # Opciones del menú
        options = ["Jugar", "Niveles", "Perfil", "Acerca de", "Salir"]
        for i, option in enumerate(options):
            color = NEON_CYAN if i == self.selected_option else NEON_PURPLE
            y_pos = 300 + i * 70

            # Calcular escala para la opción seleccionada
            if i == self.selected_option:
                # Efecto de pulso en la opción seleccionada
                scale_pulse = 1.0 + np.sin(self.menu_option_time + i * 0.5) * 0.08
                scaled_size = int(50 * scale_pulse)
                scaled_font = pygame.font.Font(None, scaled_size)

                # Renderizar texto con escala
                text_surface = scaled_font.render(option, True, color)

                # Dibujar glow
                for offset in range(GLOW_LAYERS, 0, -1):
                    glow_color = tuple(
                        int(c * 0.3 * offset / GLOW_LAYERS) for c in color
                    )
                    for dx, dy in [
                        (offset, offset),
                        (-offset, offset),
                        (offset, -offset),
                        (-offset, -offset),
                    ]:
                        glow_text = scaled_font.render(option, True, glow_color)
                        glow_rect = glow_text.get_rect(
                            center=(SCREEN_WIDTH // 2 + dx, y_pos + dy)
                        )
                        self.screen.blit(glow_text, glow_rect)

                # Texto principal
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                self.screen.blit(text_surface, text_rect)
            else:
                text = self.font_menu.render(option, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                self.screen.blit(text, text_rect)

        # Instrucciones
        instructions = self.font_small.render(
            "Usa ↑↓ para navegar, ENTER para seleccionar", True, NEON_GREEN
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 700))
        self.screen.blit(instructions, inst_rect)

    def draw_level_select(self, player):
        """Dibuja el menú de selección de niveles"""
        self.menu_type = "level_select"  # Establecer tipo de menú
        self.draw_animated_background()

        # Título
        self.draw_text_with_glow(
            "SELECCIONAR NIVEL", self.font_title, NEON_PINK, (SCREEN_WIDTH // 2, 80)
        )

        # Configuración de cuadrícula: 3 niveles en una fila horizontal
        cols = 3
        rows = 1

        # Dimensiones de cada cuadro
        box_width = 150
        box_height = 100

        # Espaciado
        spacing_x = 180
        spacing_y = 130

        # Posición inicial centrada
        total_width = cols * spacing_x - (spacing_x - box_width)
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = 300  # Centrado verticalmente

        for i in range(1, TOTAL_LEVELS + 1):
            # Calcular posición en cuadrícula
            col = (i - 1) % cols
            row = (i - 1) // cols

            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            # Verificar si está desbloqueado
            is_unlocked = player.is_level_unlocked(i)

            # Color según estado
            if i == self.selected_option + 1:
                color = NEON_CYAN if is_unlocked else GRAY
                border_width = 5
            elif is_unlocked:
                color = NEON_PURPLE
                border_width = 3
            else:
                color = GRAY
                border_width = 3

            # Cuadro del nivel con glow
            if i == self.selected_option + 1 and is_unlocked:
                for glow in range(3):
                    glow_color = tuple(int(c * 0.3) for c in color)
                    pygame.draw.rect(
                        self.screen,
                        glow_color,
                        (
                            x - glow * 2,
                            y - glow * 2,
                            box_width + glow * 4,
                            box_height + glow * 4,
                        ),
                        border_width,
                    )

            pygame.draw.rect(
                self.screen, color, (x, y, box_width, box_height), border_width
            )

            # Número de nivel
            level_text = self.font_menu.render(f"NIVEL {i}", True, color)
            level_rect = level_text.get_rect(center=(x + box_width // 2, y + 30))
            self.screen.blit(level_text, level_rect)

            # Estado (bloqueado/desbloqueado)
            if not is_unlocked:
                lock_text = self.font_small.render("BLOQUEADO", True, GRAY)
                lock_rect = lock_text.get_rect(center=(x + box_width // 2, y + 65))
                self.screen.blit(lock_text, lock_rect)
            else:
                # Mostrar si está completado
                completed = player.levels_completed[i]
                if completed:
                    complete_text = self.font_small.render(
                        "✓ COMPLETO", True, NEON_GREEN
                    )
                    complete_rect = complete_text.get_rect(
                        center=(x + box_width // 2, y + 65)
                    )
                    self.screen.blit(complete_text, complete_rect)

        # Instrucciones actualizadas para navegación en cuadrícula
        instructions = self.font_small.render(
            "Usa ←→↑↓ para navegar, ENTER para seleccionar, ESC para volver",
            True,
            NEON_GREEN,
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 700))
        self.screen.blit(instructions, inst_rect)

    def draw_profile(self, player):
        """Dibuja el perfil del jugador"""
        self.draw_animated_background()

        # Título
        self.draw_text_with_glow(
            "PERFIL DE JUGADOR", self.font_title, NEON_PINK, (SCREEN_WIDTH // 2, 80)
        )

        # Panel de información
        panel_y = 180
        panel_width = 800
        panel_height = 480
        panel_x = (SCREEN_WIDTH - panel_width) // 2

        # Fondo del panel con transparencia
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((20, 10, 40, 200))
        pygame.draw.rect(panel_surface, NEON_CYAN, (0, 0, panel_width, panel_height), 2)
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Información del jugador
        y_offset = panel_y + 30

        # Nombre del jugador
        name_text = self.font_menu.render(f"⚡ {player.name}", True, NEON_YELLOW)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(name_text, name_rect)

        y_offset += 70

        # Estadísticas generales
        stats_left_x = panel_x + 50
        stats_right_x = panel_x + panel_width // 2 + 50

        # Columna izquierda
        left_stats = [
            (
                "Niveles completados:",
                f"{player.total_levels_completed}/{TOTAL_LEVELS}",
                NEON_CYAN,
            ),
            (
                "Progreso total:",
                f"{player.get_completion_percentage():.0f}%",
                NEON_GREEN,
            ),
            (
                "Niveles desbloqueados:",
                f"{player.unlocked_levels}/{TOTAL_LEVELS}",
                NEON_PURPLE,
            ),
        ]

        for i, (label, value, color) in enumerate(left_stats):
            label_text = self.font_small.render(label, True, GRAY)
            value_text = self.font_menu.render(value, True, color)
            self.screen.blit(label_text, (stats_left_x, y_offset + i * 60))
            self.screen.blit(value_text, (stats_left_x, y_offset + i * 60 + 25))

        # Columna derecha - Mejores tiempos por nivel
        best_times_title = self.font_small.render("Mejores Tiempos:", True, NEON_ORANGE)
        self.screen.blit(best_times_title, (stats_right_x, y_offset))

        for nivel in range(1, TOTAL_LEVELS + 1):
            nivel_y = y_offset + 30 + (nivel - 1) * 50

            if player.levels_completed.get(nivel, False):
                # Nivel completado - mostrar tiempo
                best_score = player.best_scores.get(nivel)
                if best_score and isinstance(best_score, dict) and "time" in best_score:
                    tiempo = best_score["time"]
                    minutos = int(tiempo // 60)
                    segundos = int(tiempo % 60)
                    tiempo_str = f"{minutos}:{segundos:02d}"
                    color = NEON_GREEN
                    icono = "✓"
                else:
                    tiempo_str = "--:--"
                    color = NEON_CYAN
                    icono = "✓"
            else:
                # Nivel no completado
                tiempo_str = (
                    "Bloqueado" if nivel > player.unlocked_levels else "Sin completar"
                )
                color = GRAY
                icono = "✗" if nivel > player.unlocked_levels else "○"

            nivel_text = self.font_small.render(f"{icono} Nivel {nivel}:", True, color)
            tiempo_text = self.font_small.render(tiempo_str, True, color)
            self.screen.blit(nivel_text, (stats_right_x, nivel_y))
            self.screen.blit(tiempo_text, (stats_right_x + 100, nivel_y))

        # Barra de progreso
        progress_y = panel_y + panel_height - 60
        progress_width = panel_width - 100
        progress_height = 30
        progress_x = panel_x + 50

        # Fondo de la barra
        pygame.draw.rect(
            self.screen,
            (40, 20, 60),
            (progress_x, progress_y, progress_width, progress_height),
        )
        pygame.draw.rect(
            self.screen,
            NEON_PURPLE,
            (progress_x, progress_y, progress_width, progress_height),
            2,
        )

        # Relleno de la barra
        progress_fill = int(progress_width * (player.get_completion_percentage() / 100))
        if progress_fill > 0:
            pygame.draw.rect(
                self.screen,
                NEON_CYAN,
                (progress_x, progress_y, progress_fill, progress_height),
            )

        # Texto de porcentaje
        percent_text = self.font_small.render(
            f"{player.get_completion_percentage():.0f}% Completado", True, WHITE
        )
        percent_rect = percent_text.get_rect(
            center=(SCREEN_WIDTH // 2, progress_y + progress_height // 2)
        )
        self.screen.blit(percent_text, percent_rect)

        # Opciones del perfil
        options_y = 685
        options = ["Volver", "Reiniciar Progreso"]

        for i, option in enumerate(options):
            is_selected = i == self.selected_option

            if is_selected:
                color = NEON_YELLOW if i == 0 else NEON_ORANGE
                size = 35
            else:
                color = NEON_GREEN if i == 0 else NEON_PINK
                size = 30

            option_font = pygame.font.Font(None, size)
            option_text = option_font.render(option, True, color)

            x_pos = SCREEN_WIDTH // 2 - 200 if i == 0 else SCREEN_WIDTH // 2 + 200
            option_rect = option_text.get_rect(center=(x_pos, options_y))

            # Flecha de selección
            if is_selected:
                arrow = option_font.render("►", True, color)
                arrow_rect = arrow.get_rect(center=(x_pos - 100, options_y))
                self.screen.blit(arrow, arrow_rect)

            self.screen.blit(option_text, option_rect)

        # Instrucciones
        instructions = self.font_small.render(
            "←→ Navegar | ENTER Seleccionar | ESC Volver", True, GRAY
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 720))
        self.screen.blit(instructions, inst_rect)

    def draw_about(self):
        """Dibuja la pantalla Acerca de"""
        self.draw_animated_background()

        # Título principal
        self.draw_text_with_glow(
            "CUBO: ARQUITECTO DEL CAOS",
            self.font_title,
            NEON_CYAN,
            (SCREEN_WIDTH // 2, 80),
        )

        # Panel de información
        panel_y = 160
        panel_width = 900
        panel_height = 500
        panel_x = (SCREEN_WIDTH - panel_width) // 2

        # Fondo del panel con transparencia
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((20, 10, 40, 200))
        pygame.draw.rect(
            panel_surface, NEON_PURPLE, (0, 0, panel_width, panel_height), 2
        )
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Información organizada en secciones
        y_offset = panel_y + 30

        # Versión del juego
        version_text = self.font_menu.render(
            f"Versión {GAME_VERSION}", True, NEON_YELLOW
        )
        version_rect = version_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(version_text, version_rect)

        y_offset += 60

        # Línea separadora
        pygame.draw.line(
            self.screen,
            NEON_CYAN,
            (panel_x + 100, y_offset - 10),
            (panel_x + panel_width - 100, y_offset - 10),
            1,
        )

        # Información del proyecto
        info_title = self.font_menu.render("INFORMACIÓN DEL PROYECTO", True, NEON_PINK)
        info_title_rect = info_title.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 10))
        self.screen.blit(info_title, info_title_rect)

        y_offset += 60

        # Detalles del proyecto
        project_details = [
            ("Autores:", GAME_AUTHORS, NEON_GREEN),
            ("Propósito:", GAME_PURPOSE, NEON_CYAN),
            ("Año:", GAME_YEAR, NEON_PURPLE),
            ("Licencia:", GAME_LICENSE, NEON_ORANGE),
        ]

        for label, value, color in project_details:
            label_text = self.font_small.render(label, True, GRAY)
            value_text = self.font_small.render(value, True, color)

            label_rect = label_text.get_rect(center=(SCREEN_WIDTH // 2 - 150, y_offset))
            value_rect = value_text.get_rect(center=(SCREEN_WIDTH // 2 + 100, y_offset))

            self.screen.blit(label_text, label_rect)
            self.screen.blit(value_text, value_rect)

            y_offset += 40

        y_offset += 20

        # Línea separadora
        pygame.draw.line(
            self.screen,
            NEON_CYAN,
            (panel_x + 100, y_offset),
            (panel_x + panel_width - 100, y_offset),
            1,
        )

        y_offset += 30

        # Características del juego
        features_title = self.font_menu.render("CARACTERÍSTICAS", True, NEON_PINK)
        features_rect = features_title.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(features_title, features_rect)

        y_offset += 45

        features = [
            "✦ 3 Niveles de dificultad progresiva",
            "✦ Sistema de transformaciones geométricas",
            "✦ Mecánicas de física y colisiones",
            "✦ Sistema de puntuación y mejores tiempos",
        ]

        left_x = panel_x + 80
        right_x = panel_x + panel_width // 2 + 40

        for i, feature in enumerate(features):
            if i < 2:
                x_pos = left_x
            else:
                x_pos = right_x

            y_pos = y_offset + (i % 2) * 35

            feature_text = self.font_small.render(feature, True, NEON_CYAN)
            self.screen.blit(feature_text, (x_pos, y_pos))

        y_offset += 90

        # Copyright
        copyright_text = self.font_small.render(
            "© 2025 - Todos los derechos reservados", True, NEON_PURPLE
        )
        copyright_rect = copyright_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        self.screen.blit(copyright_text, copyright_rect)

        # Instrucciones
        instructions = self.font_small.render(
            "Presiona ESC para volver", True, NEON_GREEN
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 720))
        self.screen.blit(instructions, inst_rect)

    def draw_confirmation_dialog(self, message="¿Desea salir?", selected_option=0):
        """
        Dibuja un diálogo de confirmación con estilo cyberpunk

        Args:
            message: Mensaje a mostrar
            selected_option: 0 para "Sí", 1 para "No"
        """
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Dimensiones del diálogo
        dialog_width = 500
        dialog_height = 250
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2

        # Fondo del diálogo con bordes neón
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, BG_DARK, dialog_rect)
        pygame.draw.rect(self.screen, NEON_CYAN, dialog_rect, 3)

        # Efecto de brillo en las esquinas
        corner_size = 10
        corners = [
            (dialog_x, dialog_y),
            (dialog_x + dialog_width - corner_size, dialog_y),
            (dialog_x, dialog_y + dialog_height - corner_size),
            (
                dialog_x + dialog_width - corner_size,
                dialog_y + dialog_height - corner_size,
            ),
        ]
        for corner_x, corner_y in corners:
            pygame.draw.circle(self.screen, NEON_CYAN, (corner_x, corner_y), 5)

        # Mensaje principal
        message_font = pygame.font.Font(None, 48)
        message_surf = message_font.render(message, True, NEON_CYAN)
        message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 80))
        self.screen.blit(message_surf, message_rect)

        # Opciones
        options = ["SÍ", "NO"]
        option_y = dialog_y + 150
        button_width = 120
        button_height = 50
        button_spacing = 60

        total_width = len(options) * button_width + (len(options) - 1) * button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2

        for i, option in enumerate(options):
            button_x = start_x + i * (button_width + button_spacing)
            button_rect = pygame.Rect(button_x, option_y, button_width, button_height)

            # Color según selección
            if i == selected_option:
                color = NEON_CYAN
                bg_color = (*NEON_CYAN[:3], 50)
                # Efecto de pulso
                pulse = abs(np.sin(self.menu_option_time * 3)) * 10
                expanded_rect = button_rect.inflate(int(pulse), int(pulse))
                pygame.draw.rect(self.screen, bg_color, expanded_rect)
                pygame.draw.rect(self.screen, color, expanded_rect, 3)
            else:
                color = GRAY
                pygame.draw.rect(self.screen, color, button_rect, 2)

            # Texto de la opción
            option_font = pygame.font.Font(None, 40)
            option_surf = option_font.render(option, True, color)
            option_rect = option_surf.get_rect(center=button_rect.center)
            self.screen.blit(option_surf, option_rect)

    def draw_reset_confirmation_dialog(self, selected_option=0):
        """
        Dibuja un diálogo de confirmación para reiniciar el progreso

        Args:
            selected_option: 0 para "Sí", 1 para "No"
        """
        # Overlay semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Dimensiones del diálogo
        dialog_width = 600
        dialog_height = 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2

        # Fondo del diálogo con bordes neón
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, BG_DARK, dialog_rect)
        pygame.draw.rect(self.screen, NEON_ORANGE, dialog_rect, 3)

        # Efecto de brillo en las esquinas
        corner_size = 10
        corners = [
            (dialog_x, dialog_y),
            (dialog_x + dialog_width - corner_size, dialog_y),
            (dialog_x, dialog_y + dialog_height - corner_size),
            (
                dialog_x + dialog_width - corner_size,
                dialog_y + dialog_height - corner_size,
            ),
        ]
        for corner_x, corner_y in corners:
            pygame.draw.circle(self.screen, NEON_ORANGE, (corner_x, corner_y), 5)

        # Icono de advertencia
        warning_font = pygame.font.Font(None, 80)
        warning_icon = warning_font.render("⚠", True, NEON_ORANGE)
        warning_rect = warning_icon.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 60))
        self.screen.blit(warning_icon, warning_rect)

        # Mensaje principal
        message_font = pygame.font.Font(None, 42)
        message_surf = message_font.render(
            "¿Reiniciar todo el progreso?", True, NEON_PINK
        )
        message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 120))
        self.screen.blit(message_surf, message_rect)

        # Advertencia
        warning_text_font = pygame.font.Font(None, 28)
        warning_text = warning_text_font.render(
            "Esta acción no se puede deshacer", True, GRAY
        )
        warning_text_rect = warning_text.get_rect(
            center=(SCREEN_WIDTH // 2, dialog_y + 155)
        )
        self.screen.blit(warning_text, warning_text_rect)

        # Opciones
        options = ["SÍ, REINICIAR", "NO, CANCELAR"]
        option_y = dialog_y + 210
        button_width = 180
        button_height = 50
        button_spacing = 40

        total_width = len(options) * button_width + (len(options) - 1) * button_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2

        for i, option in enumerate(options):
            button_x = start_x + i * (button_width + button_spacing)
            button_rect = pygame.Rect(button_x, option_y, button_width, button_height)

            # Color según selección
            if i == selected_option:
                color = NEON_ORANGE if i == 0 else NEON_CYAN
                bg_color = (*color[:3], 50)
                # Efecto de pulso
                pulse = abs(np.sin(self.menu_option_time * 3)) * 10
                expanded_rect = button_rect.inflate(int(pulse), int(pulse))
                pygame.draw.rect(self.screen, bg_color, expanded_rect)
                pygame.draw.rect(self.screen, color, expanded_rect, 3)
            else:
                color = GRAY
                pygame.draw.rect(self.screen, color, button_rect, 2)

            # Texto de la opción
            option_font = pygame.font.Font(None, 30)
            option_surf = option_font.render(option, True, color)
            option_rect = option_surf.get_rect(center=button_rect.center)
            self.screen.blit(option_surf, option_rect)

    def handle_input(self, event, max_options):
        """Maneja la entrada del teclado en el menú"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Navegación circular para menús verticales
                self.selected_option = (self.selected_option - 1) % max_options
                return "navigate"
            elif event.key == pygame.K_DOWN:
                # Navegación circular para menús verticales
                self.selected_option = (self.selected_option + 1) % max_options
                return "navigate"
            elif event.key == pygame.K_LEFT:
                # Para menú de niveles horizontal
                if self.menu_type == "level_select":
                    if self.selected_option > 0:
                        self.selected_option -= 1
                else:
                    self.selected_option = max(0, self.selected_option - 1)
                return "navigate"
            elif event.key == pygame.K_RIGHT:
                # Para menú de niveles horizontal
                if self.menu_type == "level_select":
                    if self.selected_option < max_options - 1:
                        self.selected_option += 1
                else:
                    self.selected_option = min(
                        max_options - 1, self.selected_option + 1
                    )
                return "navigate"
            elif event.key == pygame.K_RETURN:
                return "select"
            elif event.key == pygame.K_ESCAPE:
                return "back"
        return None

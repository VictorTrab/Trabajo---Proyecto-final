"""
Sistema de menús del juego con estilo Cyberpunk
"""

import pygame
import numpy as np
from config.constantes import *
from entidades.audio_emocional import AudioEmocional


class Menu:
    """Clase para manejar los menús del juego"""

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 80)
        self.font_menu = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 30)
        self.selected_option = 0
        self.selected_difficulty = 0  # 0=Fácil, 1=Medio, 2=Difícil
        
        # Sistema de audio
        self.audio = AudioEmocional()
        self.audio.reproducir_musica_menu()

        # Flag para identificar el tipo de menú actual
        self.menu_type = "main"  # Valores: "main", "level_select", "difficulty", etc.

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
        self.draw_3d_pulse_title("NEONFITS", 240, NEON_PINK, (SCREEN_WIDTH // 2, 150))

        # Opciones del menú
        options = ["Jugar", "Niveles", "Configuración", "Perfil", "Acerca de", "Salir"]
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
                # Mostrar completados
                completed = sum(player.levels_completed[i].values())
                complete_text = self.font_small.render(
                    f"{completed}/3", True, NEON_GREEN if completed > 0 else color
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

    def draw_difficulty_select(self, level_number, player):
        """Dibuja el menú de selección de dificultad"""
        self.menu_type = "difficulty"  # Establecer tipo de menú
        self.draw_animated_background()

        # Título
        self.draw_text_with_glow(
            f"NIVEL {level_number}",
            self.font_title,
            NEON_PINK,
            (SCREEN_WIDTH // 2, 100),
        )

        subtitle = self.font_menu.render("Selecciona Dificultad", True, NEON_CYAN)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)

        # Dificultades
        start_y = 280
        spacing = 100

        for i, difficulty in enumerate(DIFFICULTIES):
            y = start_y + i * spacing
            color = NEON_CYAN if i == self.selected_difficulty else NEON_PURPLE

            # Cuadro de dificultad
            rect_x = SCREEN_WIDTH // 2 - 200

            if i == self.selected_difficulty:
                for glow in range(3):
                    glow_color = tuple(int(c * 0.3) for c in color)
                    pygame.draw.rect(
                        self.screen,
                        glow_color,
                        (
                            rect_x - glow * 2,
                            y - glow * 2,
                            400 + glow * 4,
                            70 + glow * 4,
                        ),
                        5,
                    )

            pygame.draw.rect(self.screen, color, (rect_x, y, 400, 70), 3)

            # Nombre de dificultad
            diff_text = self.font_menu.render(difficulty.upper(), True, color)
            diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, y + 20))
            self.screen.blit(diff_text, diff_rect)

            # Tiempo disponible
            tiempo_minutos = TIME_BY_DIFFICULTY[difficulty] // 60
            tiempo_segundos = TIME_BY_DIFFICULTY[difficulty] % 60
            if tiempo_minutos > 0:
                tiempo_str = f"{tiempo_minutos}:{tiempo_segundos:02d} min"
            else:
                tiempo_str = f"{tiempo_segundos}s"

            info_text = self.font_small.render(
                f"Tiempo disponible: {tiempo_str}",
                True,
                color,
            )
            info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, y + 50))
            self.screen.blit(info_text, info_rect)

            # Mejor puntuación
            best = player.best_scores[level_number][difficulty]
            if best:
                best_text = self.font_small.render(
                    f"✓ Mejor tiempo: {best['time']:.1f}s",
                    True,
                    NEON_GREEN,
                )
                best_rect = best_text.get_rect(x=rect_x + 410, centery=y + 35)
                self.screen.blit(best_text, best_rect)

        # Instrucciones
        instructions = self.font_small.render(
            "Usa ↑↓ para navegar, ENTER para jugar, ESC para volver",
            True,
            NEON_GREEN,
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 680))
        self.screen.blit(instructions, inst_rect)

    def draw_profile(self, player):
        """Dibuja el perfil del jugador"""
        self.draw_animated_background()

        # Título
        self.draw_text_with_glow(
            "PERFIL", self.font_title, NEON_PINK, (SCREEN_WIDTH // 2, 100)
        )

        # Estadísticas
        stats_y = 220
        total_possible = TOTAL_LEVELS * len(DIFFICULTIES)
        stats = [
            f"Jugador: {player.name}",
            f"Niveles completados: {player.total_levels_completed}/{total_possible}",
            f"Progreso: {player.get_completion_percentage():.1f}%",
            f"Niveles desbloqueados: {player.unlocked_levels}/{TOTAL_LEVELS}",
        ]

        for i, stat in enumerate(stats):
            text = self.font_menu.render(stat, True, NEON_CYAN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + i * 70))
            self.screen.blit(text, text_rect)

        # Instrucciones
        instructions = self.font_small.render(
            "Presiona ESC para volver", True, NEON_GREEN
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 700))
        self.screen.blit(instructions, inst_rect)

    def draw_about(self):
        """Dibuja la pantalla Acerca de"""
        self.draw_animated_background()

        # Título
        self.draw_text_with_glow(
            "ACERCA DE", self.font_title, NEON_PINK, (SCREEN_WIDTH // 2, 100)
        )

        # Información del juego
        info_y = 220
        info_lines = [
            ("NEONFIT", NEON_CYAN, self.font_menu),
            (f"Versión {GAME_VERSION}", NEON_PURPLE, self.font_small),
            (f"Autores: {GAME_AUTHORS}", NEON_GREEN, self.font_small),
            (f"Año: {GAME_YEAR}", NEON_PURPLE, self.font_small),
            (GAME_PURPOSE, NEON_CYAN, self.font_small),
            (f"Licencia: {GAME_LICENSE}", NEON_PURPLE, self.font_small),
            ("© 2025 Todos los derechos reservados", NEON_GREEN, self.font_small),
        ]

        for i, (line, color, font) in enumerate(info_lines):
            text = font.render(line, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, info_y + i * 55))
            self.screen.blit(text, text_rect)

        # Instrucciones
        instructions = self.font_small.render(
            "Presiona ESC para volver", True, NEON_GREEN
        )
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 720))
        self.screen.blit(instructions, inst_rect)

    def draw_settings_menu(self, config):
        """Dibuja el menú de configuración"""
        self.draw_animated_background()

        # Título
        self.draw_3d_pulse_title(
            "CONFIGURACIÓN", 180, NEON_ORANGE, (SCREEN_WIDTH // 2, 120)
        )

        # Sección de indicadores visuales
        section_y = 250
        section_title = self.font_menu.render("INDICADOR VISUAL", True, NEON_CYAN)
        section_rect = section_title.get_rect(center=(SCREEN_WIDTH // 2, section_y))
        self.screen.blit(section_title, section_rect)

        # Descripción
        desc_font = pygame.font.Font(None, 28)
        desc_text = desc_font.render(
            "Selecciona cómo quieres ver tus controles en el juego:", True, NEON_PURPLE
        )
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, section_y + 50))
        self.screen.blit(desc_text, desc_rect)

        # Opciones de indicadores
        options_y = section_y + 120

        for i, indicator_type in enumerate(INDICATOR_TYPES):
            y_pos = options_y + i * 80

            # Verificar si es la opción seleccionada
            is_selected = i == self.selected_option
            is_current = indicator_type == config.indicator_type

            # Colores según estado
            if is_selected:
                color = NEON_YELLOW
                scale = 1.1
            elif is_current:
                color = NEON_GREEN
                scale = 1.0
            else:
                color = NEON_PURPLE
                scale = 0.9

            # Renderizar opción
            size = int(45 * scale)
            option_font = pygame.font.Font(None, size)
            option_text = option_font.render(indicator_type, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))

            # Glow si está seleccionada
            if is_selected:
                for offset in range(3, 0, -1):
                    glow_color = tuple(int(c * 0.3 * offset / 3) for c in color)
                    for dx, dy in [
                        (offset, offset),
                        (-offset, offset),
                        (offset, -offset),
                        (-offset, -offset),
                    ]:
                        glow = option_font.render(indicator_type, True, glow_color)
                        glow_rect = glow.get_rect(
                            center=(SCREEN_WIDTH // 2 + dx, y_pos + dy)
                        )
                        self.screen.blit(glow, glow_rect)

            self.screen.blit(option_text, option_rect)

            # Indicador de selección actual
            if is_current:
                check_font = pygame.font.Font(None, 40)
                check = check_font.render("✓", True, NEON_GREEN)
                check_rect = check.get_rect(center=(SCREEN_WIDTH // 2 - 200, y_pos))
                self.screen.blit(check, check_rect)

            # Flecha de selección
            if is_selected:
                arrow_font = pygame.font.Font(None, 50)
                arrow = arrow_font.render("►", True, NEON_YELLOW)
                arrow_rect = arrow.get_rect(center=(SCREEN_WIDTH // 2 - 250, y_pos))
                self.screen.blit(arrow, arrow_rect)

        # Descripciones de cada indicador
        descriptions = [
            "Muestra un teclado virtual en pantalla",
            "Barras de progreso por tipo de acción",
            "Sin indicador visual (modo limpio)",
        ]

        if 0 <= self.selected_option < len(descriptions):
            desc_y = options_y + len(INDICATOR_TYPES) * 80 + 40
            desc_detail = desc_font.render(
                descriptions[self.selected_option], True, NEON_CYAN
            )
            desc_detail_rect = desc_detail.get_rect(center=(SCREEN_WIDTH // 2, desc_y))
            self.screen.blit(desc_detail, desc_detail_rect)

        # Instrucciones
        inst_y = SCREEN_HEIGHT - 80
        instructions = [
            ("↑↓ Navegar", NEON_PURPLE),
            ("ENTER Seleccionar", NEON_GREEN),
            ("ESC Volver", NEON_ORANGE),
        ]

        inst_font = pygame.font.Font(None, 30)
        total_width = sum(inst_font.size(text)[0] + 40 for text, _ in instructions)
        start_x = (SCREEN_WIDTH - total_width) // 2

        for text, color in instructions:
            inst = inst_font.render(text, True, color)
            self.screen.blit(inst, (start_x, inst_y))
            start_x += inst_font.size(text)[0] + 40

    def handle_input(self, event, max_options):
        """Maneja la entrada del teclado en el menú"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Navegación circular para menús verticales
                self.selected_option = (self.selected_option - 1) % max_options
                self.selected_difficulty = (self.selected_difficulty - 1) % max_options
                self.audio.reproducir_efecto("ui_navigate")
                return "navigate"
            elif event.key == pygame.K_DOWN:
                # Navegación circular para menús verticales
                self.selected_option = (self.selected_option + 1) % max_options
                self.selected_difficulty = (self.selected_difficulty + 1) % max_options
                self.audio.reproducir_efecto("ui_navigate")
                return "navigate"
            elif event.key == pygame.K_LEFT:
                # Para menú de niveles horizontal
                if self.menu_type == "level_select":
                    if self.selected_option > 0:
                        self.selected_option -= 1
                        self.audio.reproducir_efecto("ui_navigate")
                else:
                    self.selected_option = max(0, self.selected_option - 1)
                    self.audio.reproducir_efecto("ui_navigate")
                return "navigate"
            elif event.key == pygame.K_RIGHT:
                # Para menú de niveles horizontal
                if self.menu_type == "level_select":
                    if self.selected_option < max_options - 1:
                        self.selected_option += 1
                        self.audio.reproducir_efecto("ui_navigate")
                else:
                    self.selected_option = min(
                        max_options - 1, self.selected_option + 1
                    )
                    self.audio.reproducir_efecto("ui_navigate")
                return "navigate"
            elif event.key == pygame.K_RETURN:
                self.audio.reproducir_efecto("ui_select")
                return "select"
            elif event.key == pygame.K_ESCAPE:
                self.audio.reproducir_efecto("ui_back")
                return "back"
        return None

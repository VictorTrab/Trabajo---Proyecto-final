import pygame
import numpy as np
from constantes import *
from gestor_recursos import AssetManager


class UIUtils:
    """Utilidades de interfaz de usuario"""

    @staticmethod
    def draw_text_with_glow(screen, text, size, color, center_pos, glow_layers=3):
        """Dibuja texto con efecto de resplandor"""
        font = AssetManager.get_font(size)

        # Capas de glow
        for offset in range(glow_layers, 0, -1):
            glow_color = tuple(int(c * 0.3 * offset / glow_layers) for c in color)
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
                screen.blit(glow_text, glow_rect)

        # Texto principal
        main_text = font.render(text, True, color)
        main_rect = main_text.get_rect(center=center_pos)
        screen.blit(main_text, main_rect)

    @staticmethod
    def draw_hexagon(screen, cx, cy, radius, color, border_color, width=0):
        """Dibuja un hexagono"""
        points = []
        for i in range(6):
            angle = i * np.pi / 3
            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)
            points.append((x, y))

        # Asegurar colores validos
        color = tuple(int(max(0, min(255, c))) for c in color)
        border_color = tuple(int(max(0, min(255, c))) for c in border_color)

        pygame.draw.polygon(screen, color, points, width)
        if width == 0:  # Si es relleno, dibujar borde tambien
            pygame.draw.polygon(screen, border_color, points, 1)


class NeonButton:
    """Boton con estilo neon"""

    def __init__(self, text, x, y, width, height, color=NEON_CYAN, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.action = action
        self.is_hovered = False
        self.pulse_time = 0

    def update(self):
        """Actualiza estado del boton"""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.pulse_time += 0.1
        else:
            self.pulse_time = 0

    def draw(self, screen):
        """Dibuja el boton"""
        # Color base
        current_color = self.color if not self.is_hovered else NEON_PINK

        # Efecto de pulso si esta seleccionado
        scale = 1.0
        if self.is_hovered:
            scale = 1.0 + np.sin(self.pulse_time) * 0.05

        # Dibujar borde con glow
        glow_width = 3 if not self.is_hovered else 5
        pygame.draw.rect(screen, current_color, self.rect, glow_width)

        if self.is_hovered:
            # Glow extra
            for i in range(3):
                glow_rect = self.rect.inflate(i * 4, i * 4)
                pygame.draw.rect(
                    screen, tuple(int(c * 0.3) for c in current_color), glow_rect, 1
                )

        # Texto
        font_size = 40 if not self.is_hovered else 45
        UIUtils.draw_text_with_glow(
            screen, self.text, font_size, current_color, self.rect.center
        )

    def handle_event(self, event):
        """Maneja eventos de input"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.action:
                return self.action()
        return None

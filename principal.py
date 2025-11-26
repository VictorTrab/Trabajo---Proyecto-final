"""
NeonFit - Juego de Puzzle con Transformaciones Geometricas
Punto de entrada principal del juego
"""

import pygame
import sys
from constantes import *
from jugador import Player
from sistema_menu import Menu
from logica_juego import Game
from estados_juego import (
    MainMenuState,
    LevelSelectState,
    DifficultySelectState,
    PlayingState,
    TransitionState,
    ProfileState,
    AboutState,
)


class GameManager:
    """Gestor principal del juego"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("NeonFit - Puzzle de Transformaciones Geometricas")
        self.clock = pygame.time.Clock()

        # crear jugador
        self.player = Player.load()

        self.menu = Menu(self.screen)

        self.current_game = None
        self.selected_level = None
        self.transition_data = None
        self.running = True

        # Inicializar estados
        self.states = {
            "main_menu": MainMenuState(self),
            "level_select": LevelSelectState(self),
            "difficulty_select": DifficultySelectState(self),
            "playing": PlayingState(self),
            "transition": TransitionState(self),
            "profile": ProfileState(self),
            "about": AboutState(self),
        }
        self.current_state = self.states["main_menu"]

    def change_state(self, state_name):
        """Cambia el estado actual del juego"""
        if state_name in self.states:
            self.current_state = self.states[state_name]

    def draw_transition_screen_impl(self):
        """Dibuja la pantalla de transicion con efecto blur"""
        if not self.transition_data:
            return

        # Dibujar snapshot con blur (usando escala para simular blur)
        snapshot = self.transition_data["snapshot"]

        # Crear efecto blur escalando hacia abajo y luego hacia arriba
        blur_size = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
        blurred = pygame.transform.smoothscale(snapshot, blur_size)
        blurred = pygame.transform.smoothscale(blurred, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Dibujar imagen borrosa
        self.screen.blit(blurred, (0, 0))

        # Añadir capa oscura semi-transparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BG_DARK)
        self.screen.blit(overlay, (0, 0))

        # Título "NIVEL COMPLETADO"
        font_title = pygame.font.Font(None, 100)
        title_text = font_title.render("¡NIVEL COMPLETADO!", True, NEON_GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))

        # Glow en título
        for offset in range(5, 0, -1):
            glow_color = tuple(int(c * 0.2 * offset / 5) for c in NEON_GREEN)
            for dx, dy in [
                (offset * 2, offset * 2),
                (-offset * 2, offset * 2),
                (offset * 2, -offset * 2),
                (-offset * 2, -offset * 2),
            ]:
                glow_text = font_title.render("¡NIVEL COMPLETADO!", True, glow_color)
                self.screen.blit(glow_text, (title_rect.x + dx, title_rect.y + dy))

        self.screen.blit(title_text, title_rect)

        # Estadísticas
        font_stats = pygame.font.Font(None, 50)
        stats_y = 320

        stats = [
            f"Nivel: {self.transition_data['level']}",
            f"Dificultad: {self.transition_data['difficulty']}",
            f"Movimientos: {self.transition_data['moves']}",
            f"Tiempo: {self.transition_data['time']:.1f}s",
        ]

        for i, stat in enumerate(stats):
            stat_text = font_stats.render(stat, True, NEON_CYAN)
            stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + i * 60))
            self.screen.blit(stat_text, stat_rect)

        # Instrucción para continuar
        font_instruction = pygame.font.Font(None, 40)
        instruction_text = font_instruction.render(
            "Presiona ENTER para continuar", True, NEON_PINK
        )
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 650))

        # Efecto parpadeante
        alpha = int(128 + 127 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
        instruction_surface = pygame.Surface(
            instruction_text.get_size(), pygame.SRCALPHA
        )
        instruction_surface.fill((0, 0, 0, 0))
        temp_text = font_instruction.render(
            "Presiona ENTER para continuar", True, NEON_PINK
        )
        instruction_surface.blit(temp_text, (0, 0))
        instruction_surface.set_alpha(alpha)
        self.screen.blit(instruction_surface, instruction_rect)

    def run(self):
        """Bucle principal del juego"""
        while self.running:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Delegar manejo de input al estado actual
                self.current_state.handle_input(event)

            # Actualizar estado actual
            self.current_state.update()

            # Dibujar estado actual
            self.current_state.draw(self.screen)

            # Actualizar pantalla
            pygame.display.flip()
            self.clock.tick(FPS)

        # Guardar antes de salir
        self.player.save()
        pygame.quit()
        sys.exit()


def main():
    """Función principal"""
    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()

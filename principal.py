"""
CUBO: Arquitecto del Caos - Juego de Puzzle con Transformaciones Geometricas
Punto de entrada principal del juego
"""

import pygame
import sys
import os

# Agregar el directorio del proyecto al path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.constantes import *
from config.jugador import Player
from entidades.sistema_menu import Menu
from entidades.audio_dinamico import AudioDinamico
from core.estados_juego import (
    MainMenuState,
    LevelSelectState,
    PlayingState,
    TransitionState,
    LevelTransitionState,
    ProfileState,
    AboutState,
)


class GameManager:
    """Gestor principal del juego"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CUBO: Arquitecto del Caos")
        self.clock = pygame.time.Clock()

        # crear jugador
        self.player = Player.load()

        self.menu = Menu(self.screen)

        # Sistema de audio dinámico (singleton)
        self.audio = AudioDinamico()

        self.current_game = None
        self.selected_level = None
        self.transition_data = None
        self.running = True

        # Inicializar estados
        self.states = {
            "main_menu": MainMenuState(self),
            "level_select": LevelSelectState(self),
            "playing": PlayingState(self),
            "transition": TransitionState(self),
            "level_transition": LevelTransitionState(self),
            "profile": ProfileState(self),
            "about": AboutState(self),
        }
        self.current_state = self.states["main_menu"]

        # Iniciar música del menú
        self.audio.reproducir_musica("menu")

    def change_state(self, state_name):
        """Cambia el estado actual del juego"""
        if state_name in self.states:
            self.current_state = self.states[state_name]
        else:
            print(f"[WARNING] Estado '{state_name}' no existe")

    def draw_transition_screen_impl(self):
        """Dibuja la pantalla de transicion con efecto blur"""
        if not self.transition_data or not isinstance(self.transition_data, dict):
            return

        # Validar que snapshot existe y es válido
        if "snapshot" not in self.transition_data:
            return

        snapshot = self.transition_data["snapshot"]
        if snapshot is None:
            return

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

        # Verificar si es Game Over
        is_game_over = self.transition_data.get("game_over", False)

        if is_game_over:
            # Pantalla de Game Over
            font_title = pygame.font.Font(None, 100)
            title_text = font_title.render("GAME OVER", True, NEON_PINK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))

            # Glow en título
            for offset in range(5, 0, -1):
                glow_color = tuple(int(c * 0.2 * offset / 5) for c in NEON_PINK)
                for dx, dy in [
                    (offset * 2, offset * 2),
                    (-offset * 2, offset * 2),
                    (offset * 2, -offset * 2),
                    (-offset * 2, -offset * 2),
                ]:
                    glow_text = font_title.render("GAME OVER", True, glow_color)
                    self.screen.blit(glow_text, (title_rect.x + dx, title_rect.y + dy))

            self.screen.blit(title_text, title_rect)

            # Opciones
            font_options = pygame.font.Font(None, 45)
            option1_text = font_options.render(
                "ENTER - Jugar de nuevo", True, NEON_CYAN
            )
            option1_rect = option1_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
            self.screen.blit(option1_text, option1_rect)

            option2_text = font_options.render(
                "ESC - Menú Principal", True, NEON_PURPLE
            )
            option2_rect = option2_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
            self.screen.blit(option2_text, option2_rect)

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

            # Dibujar contador de FPS en la esquina inferior derecha
            fps_actual = self.clock.get_fps()
            font_fps = pygame.font.Font(None, 30)
            fps_text = font_fps.render(f"FPS: {int(fps_actual)}", True, NEON_GREEN)
            fps_rect = fps_text.get_rect()
            fps_rect.bottomright = (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)
            self.screen.blit(fps_text, fps_rect)

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

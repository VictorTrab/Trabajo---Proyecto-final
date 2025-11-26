import pygame
from constantes import *
from logica_juego import Game


class GameState:
    """Clase base para los estados del juego"""

    def __init__(self, manager):
        self.manager = manager

    def handle_input(self, event):
        """Maneja eventos de entrada"""
        pass

    def update(self):
        """Actualiza la logica del estado"""
        pass

    def draw(self, screen):
        """Dibuja el estado en pantalla"""
        pass


class MainMenuState(GameState):
    """Estado del menu principal"""

    def handle_input(self, event):
        result = self.manager.menu.handle_input(event, 5)
        if result == "select":
            option = self.manager.menu.selected_option
            if option == 0:  # Jugar
                self.manager.change_state("level_select")
                self.manager.menu.selected_option = 0
            elif option == 1:  # Niveles
                self.manager.change_state("level_select")
                self.manager.menu.selected_option = 0
            elif option == 2:  # Perfil
                self.manager.change_state("profile")
                self.manager.menu.selected_option = 0
            elif option == 3:  # Acerca de
                self.manager.change_state("about")
                self.manager.menu.selected_option = 0
            elif option == 4:  # Salir
                self.manager.running = False

    def draw(self, screen):
        screen.fill(BG_DARK)
        self.manager.menu.draw_main_menu()


class LevelSelectState(GameState):
    """Estado de seleccion de nivel"""

    def handle_input(self, event):
        result = self.manager.menu.handle_input(event, TOTAL_LEVELS)
        if result == "select":
            selected_level = self.manager.menu.selected_option + 1
            if self.manager.player.is_level_unlocked(selected_level):
                self.manager.selected_level = selected_level
                self.manager.change_state("difficulty_select")
                self.manager.menu.selected_difficulty = 0
        elif result == "back":
            self.manager.change_state("main_menu")
            self.manager.menu.selected_option = 0

    def draw(self, screen):
        screen.fill(BG_DARK)
        self.manager.menu.draw_level_select(self.manager.player)


class DifficultySelectState(GameState):
    """Estado de seleccion de dificultad"""

    def handle_input(self, event):
        result = self.manager.menu.handle_input(event, len(DIFFICULTIES))
        if result == "select":
            difficulty = DIFFICULTIES[self.manager.menu.selected_difficulty]
            self.manager.current_game = Game(
                self.manager.screen,
                self.manager.selected_level,
                difficulty,
                self.manager.player,
            )
            self.manager.change_state("playing")
        elif result == "back":
            self.manager.change_state("level_select")
            self.manager.menu.selected_option = 0
            self.manager.menu.selected_difficulty = 0

    def draw(self, screen):
        screen.fill(BG_DARK)
        self.manager.menu.draw_difficulty_select(
            self.manager.selected_level, self.manager.player
        )


class PlayingState(GameState):
    """Estado de juego activo"""

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_state("difficulty_select")
                self.manager.menu.selected_option = 0
                self.manager.menu.selected_difficulty = 0
                self.manager.player.save()
            elif event.key == pygame.K_SPACE:
                if self.manager.current_game.check_completion():
                    self.manager.player.save()

    def update(self):
        # Manejar entrada continua (movimiento)
        keys = pygame.key.get_pressed()
        self.manager.current_game.handle_input(keys)

        game_ended = self.manager.current_game.update()
        if game_ended:
            # Logica de fin de juego (espera y transicion)
            # Nota: Para simplificar, manejamos la espera aqui o pasamos a un estado de 'resultado'
            # Por ahora, mantenemos la logica original simplificada
            if self.manager.current_game.failed:
                # Reiniciar
                difficulty = DIFFICULTIES[self.manager.menu.selected_difficulty]
                self.manager.current_game = Game(
                    self.manager.screen,
                    self.manager.selected_level,
                    difficulty,
                    self.manager.player,
                )
            else:
                # Completado
                self.manager.transition_data = {
                    "level": self.manager.selected_level,
                    "difficulty": DIFFICULTIES[self.manager.menu.selected_difficulty],
                    "moves": self.manager.current_game.moves_count,
                    "time": self.manager.current_game.time_elapsed,
                    "snapshot": self.manager.screen.copy(),
                }
                self.manager.change_state("transition")
                self.manager.player.save()

    def draw(self, screen):
        # El metodo update de Game ya dibuja, asi que aqui no hacemos nada o refactorizamos Game
        # Game.update() devuelve bool, pero tambien dibuja.
        # Idealmente Game.update() solo actualizaria y Game.draw() dibujaria.
        # Por ahora asumimos que Game.update() maneja el dibujo como estaba antes.
        pass


class TransitionState(GameState):
    """Estado de transicion entre niveles"""

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.manager.change_state("difficulty_select")
                self.manager.menu.selected_option = 0
                self.manager.menu.selected_difficulty = 0
                self.manager.transition_data = None

    def draw(self, screen):
        self.manager.draw_transition_screen_impl()


class ProfileState(GameState):
    """Estado de perfil de jugador"""

    def handle_input(self, event):
        result = self.manager.menu.handle_input(event, 1)
        if result == "back":
            self.manager.change_state("main_menu")
            self.manager.menu.selected_option = 0

    def draw(self, screen):
        screen.fill(BG_DARK)
        self.manager.menu.draw_profile(self.manager.player)


class AboutState(GameState):
    """Estado Acerca De"""

    def handle_input(self, event):
        result = self.manager.menu.handle_input(event, 1)
        if result == "back":
            self.manager.change_state("main_menu")
            self.manager.menu.selected_option = 0

    def draw(self, screen):
        screen.fill(BG_DARK)
        self.manager.menu.draw_about()

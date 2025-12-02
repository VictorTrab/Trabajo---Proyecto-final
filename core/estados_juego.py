import pygame
from config.constantes import *
from core.logica_cubo_fase3 import GameCuboFase3
from core.logica_cubo_fase4 import GameCuboFase4
from core.logica_cubo_fase5 import GameCuboFase5
from entidades.audio_simple import AudioSimple


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

                # Crear instancia del juego (Fase 5: Sistema Emocional Avanzado)
                self.manager.current_game = GameCuboFase5(
                    self.manager.screen,
                    self.manager.selected_level,
                    self.manager.player,
                    audio=self.manager.audio,
                )

                # Reproducir música del nivel correspondiente
                self.manager.audio.reproducir_musica_nivel(selected_level)

                self.manager.change_state("playing")
        elif result == "back":
            self.manager.change_state("main_menu")
            self.manager.menu.selected_option = 0

    def draw(self, screen):
        screen.fill(BG_DARK)
        self.manager.menu.draw_level_select(self.manager.player)


class PlayingState(GameState):
    """Estado de juego activo"""

    def __init__(self, manager):
        super().__init__(manager)
        self.show_exit_confirmation = False
        self.exit_confirmation_option = 1  # 0=Sí, 1=No (por defecto en No)

    def handle_input(self, event):
        # Si está mostrando el diálogo de confirmación de salida
        if self.show_exit_confirmation:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # Cambiar entre Sí y No
                    self.exit_confirmation_option = 1 - self.exit_confirmation_option
                    self.manager.audio.reproducir_efecto("click")
                elif event.key == pygame.K_RETURN:
                    self.manager.audio.reproducir_efecto("click")
                    if self.exit_confirmation_option == 0:  # Sí
                        # Salir al menú de niveles
                        self.show_exit_confirmation = False
                        # Reproducir sonido de salir
                        self.manager.audio.reproducir_efecto("salir_nivel")
                        # Detener música del nivel inmediatamente
                        pygame.mixer.music.stop()
                        pygame.time.wait(50)
                        self.manager.change_state("level_select")
                        self.manager.menu.selected_option = 0
                        # Reproducir música del menú
                        self.manager.audio.reproducir_musica("menu")
                        self.manager.player.save()
                    else:  # No
                        # Cerrar diálogo y continuar jugando
                        self.show_exit_confirmation = False
                elif event.key == pygame.K_ESCAPE:
                    # ESC cierra el diálogo (equivalente a "No")
                    self.show_exit_confirmation = False
                    self.manager.audio.reproducir_efecto("click")
            return  # No procesar más eventos si el diálogo está activo

        # Si el juego está esperando confirmación, manejar ENTER
        if hasattr(self.manager.current_game, "esperando_confirmacion"):
            if self.manager.current_game.esperando_confirmacion:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # Reproducir música de nivel completado
                    self.manager.audio.reproducir_musica("completado")

                    # Iniciar transición al siguiente nivel
                    self.manager.transition_data = {
                        "level": self.manager.selected_level,
                        "snapshot": self.manager.screen.copy(),
                        "completed": True,
                    }
                    # Resetear el estado de transición antes de cambiarlo
                    self.manager.states["level_transition"].reset()
                    self.manager.change_state("level_transition")
                    self.manager.player.save()
                    return

        if event.type == pygame.MOUSEWHEEL:
            self.manager.current_game.handle_input(None, event)
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            # Pasar eventos de clic de mouse al juego
            self.manager.current_game.handle_input(None, event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Mostrar pantalla de confirmación
                self.show_exit_confirmation = True
                self.exit_confirmation_option = 1  # Por defecto en "No"
                self.manager.audio.reproducir_efecto("click")
            elif event.key == pygame.K_SPACE:
                # Verificar directamente el flag completed
                if self.manager.current_game.completed:
                    self.manager.player.save()
            else:
                # Pasar otros eventos de teclado (como E y Q) al juego
                self.manager.current_game.handle_input(None, event)

    def update(self):
        # Si está mostrando el diálogo de confirmación, no actualizar el juego
        if self.show_exit_confirmation:
            return

        # No manejar entrada si está esperando confirmación
        if hasattr(self.manager.current_game, "esperando_confirmacion"):
            if not self.manager.current_game.esperando_confirmacion:
                keys = pygame.key.get_pressed()
                self.manager.current_game.handle_input(keys)
        else:
            keys = pygame.key.get_pressed()
            self.manager.current_game.handle_input(keys)

        game_ended = self.manager.current_game.update()
        if game_ended:
            # Verificar si hay un delay de completitud activo (Fase 3)
            if hasattr(self.manager.current_game, "completion_delay"):
                # Si aún hay delay, no terminar el juego todavía
                if self.manager.current_game.completion_delay > 0:
                    return  # Continuar mostrando el resultado
                # Después del delay, activar modo de espera SOLO si fue exitoso
                if hasattr(self.manager.current_game, "esperando_confirmacion"):
                    if (
                        self.manager.current_game.completed
                        and not self.manager.current_game.failed
                    ):
                        self.manager.current_game.esperando_confirmacion = True
                        return  # Esperar a que el usuario presione ENTER

            # Logica de fin de juego
            if self.manager.current_game.failed:
                # Game Over por intentos o tiempo - Ir a pantalla de transición con opciones
                # Reproducir música de game over
                self.manager.audio.reproducir_musica("game_over")

                self.manager.transition_data = {
                    "level": self.manager.selected_level,
                    "attempts": self.manager.current_game.attempts_used,
                    "time": 0,
                    "snapshot": self.manager.screen.copy(),
                    "game_over": True,  # Flag especial para indicar Game Over
                }
                self.manager.change_state("transition")
            else:
                # Nivel completado pero sin sistema de espera (fases antiguas)
                # Detener música del nivel inmediatamente
                pygame.mixer.music.stop()
                pygame.time.wait(50)
                self.manager.change_state("level_select")
                self.manager.menu.selected_option = 0
                # Reproducir música del menú
                self.manager.audio.reproducir_musica("menu")
                self.manager.player.save()

    def draw(self, screen):
        # Verificar si el juego tiene un método draw separado (como GameCuboFase2)
        if hasattr(self.manager.current_game, "draw"):
            self.manager.current_game.draw()
        # De lo contrario, el juego original dibuja en update()

        # Si está mostrando el diálogo de confirmación, dibujarlo encima
        if self.show_exit_confirmation:
            self.manager.menu.draw_confirmation_dialog(
                "¿Desea salir?", self.exit_confirmation_option
            )


class TransitionState(GameState):
    """Estado de transicion entre niveles"""

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            is_game_over = (
                self.manager.transition_data
                and self.manager.transition_data.get("game_over", False)
            )

            if event.key == pygame.K_RETURN:
                if is_game_over:
                    # Reiniciar desde el mismo nivel
                    self.manager.current_game = GameCuboFase5(
                        self.manager.screen,
                        self.manager.selected_level,
                        self.manager.player,
                        audio=self.manager.audio,
                    )
                    # Reproducir música del nivel
                    self.manager.audio.reproducir_musica_nivel(
                        self.manager.selected_level
                    )
                    self.manager.change_state("playing")
                else:
                    # Nivel completado - volver a selección de niveles
                    # Detener música del nivel inmediatamente
                    pygame.mixer.music.stop()
                    pygame.time.wait(50)
                    self.manager.change_state("level_select")
                    self.manager.menu.selected_option = 0
                    # Reproducir música del menú
                    self.manager.audio.reproducir_musica("menu")

                self.manager.transition_data = None

            elif event.key == pygame.K_ESCAPE and is_game_over:
                # Solo en Game Over: volver al menú principal
                # Detener música del nivel inmediatamente
                pygame.mixer.music.stop()
                pygame.time.wait(50)
                self.manager.change_state("main_menu")
                self.manager.menu.selected_option = 0
                # Reproducir música del menú
                self.manager.audio.reproducir_musica("menu")
                self.manager.transition_data = None

    def draw(self, screen):
        self.manager.draw_transition_screen_impl()


class LevelTransitionState(GameState):
    """Estado de transición animada entre niveles"""

    def __init__(self, manager):
        super().__init__(manager)
        self.reset()

    def reset(self):
        """Reinicia el estado de la animación"""
        self.animation_time = 0
        self.animation_duration = 1.5  # Duración de la animación en segundos
        self.completed = False
        self.start_time = None

    def handle_input(self, event):
        # No permitir interrumpir la animación
        pass

    def update(self):
        import time

        if self.start_time is None:
            self.start_time = time.time()

        self.animation_time = time.time() - self.start_time

        # Cuando termine la animación, ir a selección de nivel
        if self.animation_time >= self.animation_duration and not self.completed:
            self.completed = True
            # Detener música del nivel inmediatamente
            pygame.mixer.music.stop()
            pygame.time.wait(50)
            self.manager.change_state("level_select")
            self.manager.menu.selected_option = 0
            # Reproducir música del menú
            self.manager.audio.reproducir_musica("menu")

    def draw(self, screen):
        # Dibujar el snapshot del juego
        if self.manager.transition_data and "snapshot" in self.manager.transition_data:
            screen.blit(self.manager.transition_data["snapshot"], (0, 0))

        # Calcular progreso de la animación (0.0 a 1.0)
        progress = min(1.0, self.animation_time / self.animation_duration)

        # Fase 1: Fade out (primeros 0.5 segundos)
        if progress < 0.33:
            alpha = int((progress / 0.33) * 200)
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(alpha)
            overlay.fill(BG_DARK)
            screen.blit(overlay, (0, 0))

            # Texto de completado con zoom
            zoom_factor = 1.0 + (progress / 0.33) * 0.2
            font_size = int(80 * zoom_factor)
            font = pygame.font.Font(None, font_size)
            texto = font.render("¡NIVEL COMPLETADO!", True, NEON_GREEN)
            texto_rect = texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(texto, texto_rect)

        # Fase 2: Transición con círculos expandiéndose (0.33 a 0.66)
        elif progress < 0.66:
            # Fondo oscuro completo
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(220)
            overlay.fill(BG_DARK)
            screen.blit(overlay, (0, 0))

            # Círculos expandiéndose desde el centro
            phase_progress = (progress - 0.33) / 0.33
            max_radius = int(SCREEN_WIDTH * 1.5)

            for i in range(3):
                delay = i * 0.2
                if phase_progress > delay:
                    circle_progress = min(1.0, (phase_progress - delay) / (1.0 - delay))
                    radius = int(max_radius * circle_progress)
                    alpha = int(100 * (1.0 - circle_progress))

                    circle_surface = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                    )
                    color = (
                        (*NEON_CYAN[:3], alpha)
                        if i % 2 == 0
                        else (*NEON_PURPLE[:3], alpha)
                    )
                    pygame.draw.circle(
                        circle_surface,
                        color,
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                        radius,
                        3,
                    )
                    screen.blit(circle_surface, (0, 0))

        # Fase 3: Fade in al menú (últimos 0.34 segundos)
        else:
            # Fondo oscuro
            screen.fill(BG_DARK)

            # Texto "Volviendo al menú" con fade in
            phase_progress = (progress - 0.66) / 0.34
            alpha = int(255 * phase_progress)

            font = pygame.font.Font(None, 60)
            texto = font.render("Volviendo al menú...", True, NEON_CYAN)
            texto_rect = texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

            texto_surface = pygame.Surface(texto.get_size(), pygame.SRCALPHA)
            texto_surface.fill((0, 0, 0, 0))
            temp_text = font.render("Volviendo al menú...", True, NEON_CYAN)
            texto_surface.blit(temp_text, (0, 0))
            texto_surface.set_alpha(alpha)
            screen.blit(texto_surface, texto_rect)


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

    def __init__(self, manager):
        super().__init__(manager)
        self.music_started = False

    def handle_input(self, event):
        result = self.manager.menu.handle_input(event, 1)
        if result == "back":
            # Volver a música del menú
            self.manager.audio.reproducir_musica("menu")
            self.music_started = False
            self.manager.change_state("main_menu")
            self.manager.menu.selected_option = 0

    def draw(self, screen):
        # Reproducir música de créditos solo una vez
        if not self.music_started:
            self.manager.audio.reproducir_musica("creditos")
            self.music_started = True

        screen.fill(BG_DARK)
        self.manager.menu.draw_about()

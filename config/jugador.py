"""
Sistema de jugador y gestión de guardado
"""

import json
import os
from config.constantes import SAVE_FILE, TOTAL_LEVELS


class Player:
    """Clase que maneja el perfil del jugador y sus estadísticas"""

    def __init__(self, name="Jugador"):
        self.name = name
        # Para cada nivel: completado (True/False)
        self.levels_completed = {i: False for i in range(1, TOTAL_LEVELS + 1)}
        # Mejor puntuación por nivel
        self.best_scores = {i: None for i in range(1, TOTAL_LEVELS + 1)}
        self.total_levels_completed = 0
        self.unlocked_levels = 1  # Solo el nivel 1 está desbloqueado al inicio
        self.last_level_played = 1  # Último nivel jugado

    def complete_level(self, level_number, attempts_used, time_used):
        """Marca un nivel como completado y actualiza estadísticas"""
        if 1 <= level_number <= TOTAL_LEVELS:
            self.levels_completed[level_number] = True

            # Actualizar mejor puntuación
            current_best = self.best_scores[level_number]

            # Validar que current_best tiene el formato correcto
            if (
                current_best is None
                or not isinstance(current_best, dict)
                or "attempts" not in current_best
            ):
                # Primer completado o datos en formato antiguo
                self.best_scores[level_number] = {
                    "attempts": attempts_used,
                    "time": time_used,
                }
            else:
                # Mejor es menos intentos, y si empatan, menos tiempo
                if attempts_used < current_best["attempts"] or (
                    attempts_used == current_best["attempts"]
                    and time_used < current_best.get("time", float("inf"))
                ):
                    self.best_scores[level_number] = {
                        "attempts": attempts_used,
                        "time": time_used,
                    }

            # Desbloquear siguiente nivel (sin exceder el máximo)
            self.unlocked_levels = min(
                max(self.unlocked_levels, level_number + 1), TOTAL_LEVELS
            )

            # Actualizar total
            self.total_levels_completed = sum(self.levels_completed.values())

    def is_level_unlocked(self, level_number):
        """Verifica si un nivel está desbloqueado"""
        return level_number <= self.unlocked_levels

    def reset_progress(self):
        """Reinicia todo el progreso del jugador"""
        self.levels_completed = {i: False for i in range(1, TOTAL_LEVELS + 1)}
        self.best_scores = {i: None for i in range(1, TOTAL_LEVELS + 1)}
        self.total_levels_completed = 0
        self.unlocked_levels = 1

    def get_completion_percentage(self):
        """Retorna el porcentaje de niveles completados"""
        return (self.total_levels_completed / TOTAL_LEVELS) * 100

    def save(self):
        """Guarda el progreso del jugador en un archivo JSON"""
        # Validar datos antes de guardar
        try:
            data = {
                "name": str(self.name) if self.name else "Jugador",
                "levels_completed": {
                    str(k): bool(v) for k, v in self.levels_completed.items()
                },
                "best_scores": {str(k): v for k, v in self.best_scores.items()},
                "total_levels_completed": (
                    int(self.total_levels_completed)
                    if self.total_levels_completed
                    else 0
                ),
                "unlocked_levels": (
                    int(self.unlocked_levels) if self.unlocked_levels else 1
                ),
                "last_level_played": (
                    int(self.last_level_played) if self.last_level_played else 1
                ),
            }
        except (ValueError, TypeError) as e:
            print(f"Error al preparar datos para guardar: {e}")
            return False

        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def load():
        """Carga el progreso del jugador desde un archivo JSON"""
        if not os.path.exists(SAVE_FILE):
            return Player()

        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validar que data sea un diccionario
            if not isinstance(data, dict):
                print("Error: archivo de guardado corrupto")
                return Player()

            player = Player(data.get("name", "Jugador"))

            # Convertir claves de string a int
            levels_completed = data.get("levels_completed", {})
            player.levels_completed = (
                {int(k): v for k, v in levels_completed.items()}
                if levels_completed
                else player.levels_completed
            )

            best_scores = data.get("best_scores", {})
            player.best_scores = (
                {int(k): v for k, v in best_scores.items()}
                if best_scores
                else player.best_scores
            )

            player.total_levels_completed = data.get("total_levels_completed", 0)
            player.unlocked_levels = data.get("unlocked_levels", 1)
            player.last_level_played = data.get("last_level_played", 1)

            # Asegurar que todos los niveles existan
            for i in range(1, TOTAL_LEVELS + 1):
                if i not in player.levels_completed:
                    player.levels_completed[i] = False
                if i not in player.best_scores:
                    player.best_scores[i] = None

            return player
        except json.JSONDecodeError:
            print(f"[Player] Save file corrupto, creando nuevo jugador")
            return Player()
        except PermissionError:
            print(f"[Player] Sin permisos para leer save file")
            return Player()
        except UnicodeDecodeError:
            print(f"[Player] Error de codificación en save file")
            return Player()
        except Exception as e:
            print(f"Error al cargar: {e}")
            return Player()

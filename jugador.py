"""
Sistema de jugador y gestión de guardado
"""

import json
import os
from constantes import SAVE_FILE, TOTAL_LEVELS, DIFFICULTIES


class Player:
    """Clase que maneja el perfil del jugador y sus estadísticas"""

    def __init__(self, name="Jugador"):
        self.name = name
        # Para cada nivel: {dificultad: completado}
        self.levels_completed = {
            i: {diff: False for diff in DIFFICULTIES}
            for i in range(1, TOTAL_LEVELS + 1)
        }
        # Mejor puntuación por nivel y dificultad
        self.best_scores = {
            i: {diff: None for diff in DIFFICULTIES} for i in range(1, TOTAL_LEVELS + 1)
        }
        self.total_levels_completed = 0
        self.unlocked_levels = 1  # Solo el nivel 1 está desbloqueado al inicio

    def complete_level(self, level_number, difficulty, moves_used, time_used):
        """Marca un nivel como completado y actualiza estadísticas"""
        if 1 <= level_number <= TOTAL_LEVELS:
            self.levels_completed[level_number][difficulty] = True

            # Actualizar mejor puntuación
            current_best = self.best_scores[level_number][difficulty]
            if current_best is None:
                self.best_scores[level_number][difficulty] = {
                    "moves": moves_used,
                    "time": time_used,
                }
            else:
                # Mejor es menos movimientos, y si empatan, menos tiempo
                if moves_used < current_best["moves"] or (
                    moves_used == current_best["moves"]
                    and time_used < current_best["time"]
                ):
                    self.best_scores[level_number][difficulty] = {
                        "moves": moves_used,
                        "time": time_used,
                    }

            # Desbloquear siguiente nivel si se completa cualquier dificultad
            if any(self.levels_completed[level_number].values()):
                self.unlocked_levels = max(self.unlocked_levels, level_number + 1)

            # Actualizar total
            self.total_levels_completed = sum(
                sum(diffs.values()) for diffs in self.levels_completed.values()
            )

    def is_level_unlocked(self, level_number):
        """Verifica si un nivel está desbloqueado"""
        return level_number <= self.unlocked_levels

    def reset_progress(self):
        """Reinicia todo el progreso del jugador"""
        self.levels_completed = {
            i: {diff: False for diff in DIFFICULTIES}
            for i in range(1, TOTAL_LEVELS + 1)
        }
        self.best_scores = {
            i: {diff: None for diff in DIFFICULTIES} for i in range(1, TOTAL_LEVELS + 1)
        }
        self.total_levels_completed = 0
        self.unlocked_levels = 1

    def get_completion_percentage(self):
        """Retorna el porcentaje de niveles completados"""
        total_possible = TOTAL_LEVELS * len(DIFFICULTIES)
        return (self.total_levels_completed / total_possible) * 100

    def save(self):
        """Guarda el progreso del jugador en un archivo JSON"""
        data = {
            "name": self.name,
            "levels_completed": {str(k): v for k, v in self.levels_completed.items()},
            "best_scores": {str(k): v for k, v in self.best_scores.items()},
            "total_levels_completed": self.total_levels_completed,
            "unlocked_levels": self.unlocked_levels,
        }

        try:
            with open(SAVE_FILE, "w") as f:
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
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)

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

            return player
        except Exception as e:
            print(f"Error al cargar: {e}")
            return Player()

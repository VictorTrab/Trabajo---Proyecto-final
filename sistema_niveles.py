"""
Sistema de niveles y configuracion de puzzles
"""

import numpy as np
import json
import os
from constantes import *


class Level:
    """Clase que define un nivel del juego"""

    def __init__(
        self,
        level_number,
        difficulty,
        shape_type,
        target_position,
        target_rotation,
        target_scale,
        grid_pattern,
    ):
        self.level_number = level_number
        self.difficulty = difficulty  # 'Facil', 'Medio', 'Dificil'
        self.shape_type = shape_type  # 'triangle', 'pentagon', 'star'
        self.target_position = target_position  # (x, y)
        self.target_rotation = target_rotation  # angulo en grados
        self.target_scale = target_scale  # factor de escala
        self.max_moves = MOVES_BY_DIFFICULTY[difficulty]
        self.time_limit = TIME_BY_DIFFICULTY[difficulty]
        self.grid_pattern = grid_pattern  # patron del teselado

    def get_shape_vertices(self):
        """Retorna los vertices de la forma segun el tipo"""
        if self.shape_type == "triangle":
            return np.array([[0, -50], [-43.3, 25], [43.3, 25]], dtype=float)

        elif self.shape_type == "square":
            return np.array([[-40, -40], [40, -40], [40, 40], [-40, 40]], dtype=float)

        elif self.shape_type == "pentagon":
            angles = np.linspace(0, 2 * np.pi, 6)[:-1] - np.pi / 2
            radius = 50
            return np.array(
                [[radius * np.cos(a), radius * np.sin(a)] for a in angles], dtype=float
            )

        elif self.shape_type == "hexagon":
            angles = np.linspace(0, 2 * np.pi, 7)[:-1]
            radius = 45
            return np.array(
                [[radius * np.cos(a), radius * np.sin(a)] for a in angles], dtype=float
            )

        elif self.shape_type == "star":
            vertices = []
            outer_radius = 50
            inner_radius = 20
            for i in range(10):
                angle = i * np.pi / 5 - np.pi / 2
                radius = outer_radius if i % 2 == 0 else inner_radius
                vertices.append([radius * np.cos(angle), radius * np.sin(angle)])
            return np.array(vertices, dtype=float)

        return np.array([[0, 0]], dtype=float)


# Cache de niveles cargados
_LEVEL_CACHE = {}


def get_level(level_number, difficulty):
    """Retorna el nivel correspondiente al numero y dificultad cargando desde JSON"""
    cache_key = (level_number, difficulty)
    if cache_key in _LEVEL_CACHE:
        return _LEVEL_CACHE[cache_key]

    try:
        file_path = os.path.join("niveles", f"level_{level_number}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        diff_data = data["difficulties"].get(difficulty)
        if not diff_data:
            print(f"Dificultad {difficulty} no encontrada para nivel {level_number}")
            return None

        level = Level(
            level_number=data["id"],
            difficulty=difficulty,
            shape_type=data["shape_type"],
            target_position=tuple(diff_data["target_position"]),
            target_rotation=diff_data["target_rotation"],
            target_scale=diff_data["target_scale"],
            grid_pattern=data["grid_pattern"],
        )

        _LEVEL_CACHE[cache_key] = level
        return level

    except FileNotFoundError:
        print(f"Archivo de nivel no encontrado: levels/level_{level_number}.json")
        return None
    except Exception as e:
        print(f"Error cargando nivel {level_number}: {e}")
        return None

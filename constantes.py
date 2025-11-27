"""
Constantes del juego - NeonFit
"""

# Dimensiones de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colores RGB - Paleta Cyberpunk
GRAY = (128, 128, 128)

# Colores Neón Cyberpunk
NEON_PINK = (255, 16, 240)  # Magenta neón
NEON_CYAN = (0, 255, 255)  # Cyan brillante
NEON_PURPLE = (138, 43, 226)  # Púrpura eléctrico
NEON_GREEN = (57, 255, 20)  # Verde neón
NEON_BLUE = (0, 191, 255)  # Azul eléctrico
NEON_ORANGE = (255, 165, 0)  # Naranja neón
NEON_YELLOW = (255, 255, 0)  # Amarillo brillante

# Colores de fondo Cyberpunk
BG_DARK = (10, 0, 20)  # Púrpura muy oscuro
BG_GRID_1 = (20, 10, 40)  # Púrpura oscuro 1
BG_GRID_2 = (30, 15, 50)  # Púrpura oscuro 2

# Configuración del juego
FPS = 60
TOTAL_LEVELS = 3

# Dificultades
DIFFICULTIES = ["Fácil", "Medio", "Difícil"]

# Movimientos por dificultad (Ya no se usa para inicialización, pero se mantiene por compatibilidad si es necesario)
MOVES_BY_DIFFICULTY = {"Fácil": 10, "Medio": 22, "Difícil": 20}

# Configuración de movimientos globales
INITIAL_GLOBAL_MOVES = 50
MOVES_REWARD = {"Fácil": 5, "Medio": 10, "Difícil": 15}

# Tiempo límite por dificultad (en segundos)
TIME_BY_DIFFICULTY = {
    "Fácil": 120,  # 2 minutos
    "Medio": 90,  # 1.5 minutos
    "Difícil": 60,  # 1 minuto
}

# Tolerancia para validar encaje (en píxeles)
SNAP_TOLERANCE = 20

# Configuración de teselado
TILE_SIZE = 40

# Velocidades de transformación
ROTATION_SPEED = 5  # grados por tecla presionada
TRANSLATION_SPEED = 5  # píxeles por tecla presionada
SCALE_SPEED = 0.05  # factor de escala por tecla presionada

# Configuración de animaciones Cyberpunk
BREATHE_SPEED = 0.03  # Velocidad del efecto respiración
BREATHE_MIN = 0.3  # Mínima intensidad
BREATHE_MAX = 0.7  # Máxima intensidad
WAVE_SPEED = 0.1  # Velocidad de propagación de onda
WAVE_RADIUS = 150  # Radio máximo del efecto onda
GLOW_LAYERS = 3  # Número de capas para efecto glow

# Archivos de guardado
SAVE_FILE = "player_save.json"

# Información del juego
GAME_VERSION = "1.0.0"
GAME_AUTHORS = "V.H & R."
GAME_LICENSE = "Uso Educativo"
GAME_YEAR = "2025"
GAME_PURPOSE = "Proyecto de informatica grafica"

# --- NUEVAS CONSTANTES PARA MECÁNICAS AVANZADAS ---

# Colores de Feedback
COLOR_SUCCESS_GLOW = (50, 255, 50)  # Verde éxito
COLOR_DANGER = (255, 50, 50)  # Rojo peligro
COLOR_WARNING = (255, 165, 0)  # Naranja advertencia

# Tipos de Zonas
ZONE_TYPE_OBSTACLE = "obstacle"  # Zona prohibida (muerte o bloqueo)
ZONE_TYPE_DISTORTION = "distortion"  # Altera escala/rotación
ZONE_TYPE_GRAVITY = "gravity"  # Arrastra la figura

# Configuración de Feedback Visual
SHAKE_DECAY = 0.9  # Cuánto disminuye el temblor por frame
MAX_SHAKE = 10.0  # Máximo desplazamiento en píxeles
PROXIMITY_THRESHOLD = 50.0  # Distancia para empezar a brillar verde

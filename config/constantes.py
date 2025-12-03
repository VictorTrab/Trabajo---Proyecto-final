"""
Constantes del juego - CUBO: Arquitecto del Caos
"""

# Dimensiones de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
WINDOW_WIDTH = SCREEN_WIDTH
WINDOW_HEIGHT = SCREEN_HEIGHT

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

# Colores básicos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Colores de fondo Cyberpunk
BG_DARK = (10, 0, 20)  # Púrpura muy oscuro
BG_GRID_1 = (20, 10, 40)  # Púrpura oscuro 1
BG_GRID_2 = (30, 15, 50)  # Púrpura oscuro 2

# Configuración del juego
FPS = 90
TOTAL_LEVELS = 3  # Solo 3 niveles simples

# Tiempo límite simplificado (en segundos)
TIME_LIMIT = 90  # 1.5 minutos por nivel

# Tolerancia para validar encaje (en píxeles)
SNAP_TOLERANCE = 20

# Configuración de teselado
TILE_SIZE = 40

# Velocidades de transformación
ROTATION_SPEED = 3  # grados por tecla presionada (más preciso)
TRANSLATION_SPEED = 5  # píxeles por tecla presionada

# Configuración de animaciones Cyberpunk
BREATHE_SPEED = 0.03  # Velocidad del efecto respiración
BREATHE_MIN = 0.3  # Mínima intensidad
BREATHE_MAX = 0.7  # Máxima intensidad
WAVE_SPEED = 0.1  # Velocidad de propagación de onda
WAVE_RADIUS = 150  # Radio máximo del efecto onda
GLOW_LAYERS = 3  # Número de capas para efecto glow

# Archivos de guardado
SAVE_FILE = "config/player_save.json"

# Información del juego
GAME_VERSION = "3.6"
GAME_AUTHORS = "V.H & R.M"
GAME_LICENSE = "Uso Educativo"
GAME_YEAR = "2025"
GAME_PURPOSE = "Proyecto informatica grafica aplicada"


# Función simple para obtener total de niveles
def get_total_levels():
    """Retorna el número total de niveles"""
    return TOTAL_LEVELS


# Cargar TOTAL_LEVELS dinámicamente
TOTAL_LEVELS = get_total_levels()

# Colores de Feedback
COLOR_DANGER = (255, 50, 50)  # Rojo peligro

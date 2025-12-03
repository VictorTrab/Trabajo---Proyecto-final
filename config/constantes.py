"""
Constantes del juego - CUBO: Arquitecto del Caos
"""

# Dimensiones de pantalla
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
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
FPS = 60
TOTAL_LEVELS = 3  # Solo 3 niveles simples

# Sistema de intentos simplificado
MAX_ATTEMPTS = 10

# Tiempo límite simplificado (en segundos)
TIME_LIMIT = 120  # 2 minutos por nivel

# Tolerancia para validar encaje (en píxeles)
SNAP_TOLERANCE = 20

# Configuración de teselado
TILE_SIZE = 40

# Velocidades de transformación
ROTATION_SPEED = 3  # grados por tecla presionada (más preciso)
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
SAVE_FILE = "config/player_save.json"

# Información del juego
GAME_VERSION = "3.6"
GAME_AUTHORS = "V.H & R.M"
GAME_LICENSE = "Uso Educativo"
GAME_YEAR = "2025"
GAME_PURPOSE = "Proyecto de informatica grafica"


# Función simple para obtener total de niveles
def get_total_levels():
    """Retorna el número total de niveles"""
    return TOTAL_LEVELS


# Cargar TOTAL_LEVELS dinámicamente
TOTAL_LEVELS = get_total_levels()

# --- NUEVAS CONSTANTES PARA MECÁNICAS AVANZADAS ---

# Colores de Feedback
COLOR_SUCCESS_GLOW = (50, 255, 50)  # Verde éxito
COLOR_DANGER = (255, 50, 50)  # Rojo peligro
COLOR_WARNING = (255, 165, 0)  # Naranja advertencia

# Configuración de Feedback Visual
PROXIMITY_THRESHOLD = 50.0  # Distancia para empezar a brillar verde
SAFE_ZONE_RADIUS = (
    150.0  # Radio de zona segura alrededor del objetivo (ignora obstáculos)
)

# Configuración de objetivo dinámico
TARGET_REPOSITION_INTERVAL = 30.0  # Intervalo en segundos para cambiar el objetivo

# Sistema de daño
DAMAGE_PER_HIT = 25  # Daño por cada colisión con obstáculo
HEALTH_REGEN_RATE = 5  # Regeneración de vida por segundo (cuando no hay colisión)
DAMAGE_COOLDOWN = 1.0  # Tiempo en segundos entre daños (invulnerabilidad temporal)

# --- CONSTANTES FASE 3: PUNTUACIÓN Y NIVELES ---

# Sistema de puntuación
PUNTOS_BASE = 1000  # Puntos base por completar un nivel
BONUS_TIEMPO_MAX = 500  # Bonus máximo por velocidad
BONUS_PRECISION_MAX = 300  # Bonus máximo por precisión
BONUS_SIN_ERRORES = 200  # Bonus por no cometer errores
PENALIZACION_POR_INTENTO_FALLIDO = 25  # Puntos perdidos por cada intento fallido
PENALIZACION_POR_PISTA = 100  # Puntos perdidos por usar una pista

# Multiplicadores de dificultad
MULTIPLICADOR_FACIL = 1.0
MULTIPLICADOR_MEDIO = 1.5
MULTIPLICADOR_DIFICIL = 2.0

# Sistema de pistas
MAX_PISTAS_POR_NIVEL = 3  # Número máximo de pistas disponibles
DURACION_PISTA = 5.0  # Segundos que dura visible una pista

# Sistema de estrellas
UMBRAL_1_ESTRELLA = 0.5  # 50% de puntos base
UMBRAL_2_ESTRELLAS = 1.0  # 100% de puntos base
UMBRAL_3_ESTRELLAS = 1.5  # 150% de puntos base

# Guía de Desarrollo y Mantenimiento - CUBO: Arquitecto del Caos

## 🛠️ Configuración del Entorno de Desarrollo

### Requisitos Previos

```bash
# Python 3.10 o superior
python --version

# Pip actualizado
python -m pip install --upgrade pip
```

### Instalación

```bash
# Clonar repositorio
git clone [URL_DEL_REPO]
cd "Trabajo - Proyecto final"

# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv

# Activar entorno virtual
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.\.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Estructura de Archivos

```
Trabajo - Proyecto final/
├── principal.py              # ⭐ Punto de entrada
├── requirements.txt          # Dependencias
├── save_game.json           # Guardado del jugador (generado)
│
├── config/                   # ⚙️ Configuración
│   ├── __init__.py
│   ├── constantes.py        # Constantes globales
│   ├── jugador.py           # Sistema de guardado
│   └── configuracion.py     # Configuración del juego
│
├── core/                     # 🎮 Lógica del juego
│   ├── __init__.py
│   ├── estados_juego.py     # Máquina de estados
│   ├── logica_cubo_fase2.py # Base: piezas y magnetismo
│   ├── logica_cubo_fase3.py # + Puntuación y niveles
│   ├── logica_cubo_fase4.py # + Meteoros y portales
│   └── logica_cubo_fase5.py # + Sistema emocional
│
├── entidades/               # 🎨 Entidades del juego
│   ├── __init__.py
│   ├── cubo.py             # Personaje principal
│   ├── pieza_geometrica.py # Piezas del puzzle
│   ├── meteoro.py          # Obstáculos dinámicos
│   ├── portal.py           # Sistema de teletransporte
│   ├── powerup.py          # Mejoras temporales
│   ├── sistema_menu.py     # Interfaz de menús
│   ├── sistema_particulas.py # Efectos de partículas
│   ├── audio_simple.py     # Sistema de audio
│   ├── efectos_emocionales.py
│   ├── animaciones_emocionales.py
│   ├── narrativa_dinamica.py
│   ├── combo_emocional.py
│   └── ambiente_emocional.py
│
├── niveles/                 # 📋 Definición de niveles
│   └── niveles.json        # Configuración de niveles
│
├── songs/                   # 🎵 Audio (MP3)
│   ├── SongMenu.mp3
│   ├── SongFacil.mp3
│   ├── SongGameStart.mp3
│   ├── SongGameOver.mp3
│   ├── SongClick.mp3
│   └── ... (otros archivos de audio)
│
└── docs/                    # 📚 Documentación
    ├── README_JUEGO.md
    ├── ARQUITECTURA_TECNICA.md
    └── GUIA_DESARROLLO.md
```

## 🔧 Tareas de Desarrollo Comunes

### Añadir un Nuevo Nivel

1. **Editar `niveles/niveles.json`:**

```json
{
  "4": {
    "nombre": "Nivel 4: Nombre",
    "piezas": [
      { "tipo": "CUADRADO", "posicion": [0, 0] },
      { "tipo": "TRIANGULO", "posicion": [1, 0] }
    ]
  }
}
```

2. **Actualizar constantes en `config/constantes.py`:**

```python
TOTAL_LEVELS = 4  # Cambiar de 3 a 4
```

3. **Probar el nuevo nivel:**

```bash
python principal.py
```

### Añadir un Nuevo Tipo de Pieza

1. **Definir en `entidades/pieza_geometrica.py`:**

```python
class PiezaGeometrica:
    # Agregar nuevo tipo
    ESTRELLA = 5  # Nuevo ID

    def _dibujar_estrella(self):
        # Implementar dibujado
        points = [...]  # Puntos de la estrella
        pygame.draw.polygon(self.surface, color, points)
```

2. **Actualizar método `draw()`:**

```python
def draw(self):
    if self.tipo == self.ESTRELLA:
        self._dibujar_estrella()
    # ... resto del código
```

3. **Agregar al generador de niveles:**

```python
tipos_disponibles = [
    PiezaGeometrica.CUADRADO,
    PiezaGeometrica.TRIANGULO,
    # ...
    PiezaGeometrica.ESTRELLA  # Añadir aquí
]
```

### Modificar Parámetros del Juego

**Cambiar tiempo límite:**

```python
# config/constantes.py
TIME_LIMIT = 180  # De 120 a 180 segundos
```

**Cambiar número de intentos:**

```python
# config/constantes.py
MAX_ATTEMPTS = 15  # De 10 a 15 intentos
```

**Ajustar velocidad de meteoros:**

```python
# entidades/meteoro.py
class GeneradorMeteoros:
    def __init__(self):
        self.velocidad_min = 150  # Reducir velocidad
        self.velocidad_max = 250
```

### Añadir Nuevos Efectos de Sonido

1. **Colocar archivo MP3 en `songs/`:**

```
songs/
  └── SongNuevoEfecto.mp3
```

2. **Registrar en `entidades/audio_simple.py`:**

```python
self.rutas_efectos = {
    "click": "songs/SongClick.mp3",
    # ... otros efectos
    "nuevo_efecto": "songs/SongNuevoEfecto.mp3"  # Añadir
}
```

3. **Usar en el juego:**

```python
self.manager.audio.reproducir_efecto("nuevo_efecto")
```

### Crear un Nuevo Estado del Juego

1. **Definir clase en `core/estados_juego.py`:**

```python
class NuevoState(GameState):
    def handle_input(self, event):
        # Manejar entrada
        pass

    def update(self):
        # Actualizar lógica
        pass

    def draw(self, screen):
        # Dibujar en pantalla
        pass
```

2. **Registrar en GameManager (`principal.py`):**

```python
self.states = {
    # ... estados existentes
    "nuevo_state": NuevoState(self)
}
```

3. **Cambiar a ese estado:**

```python
self.manager.change_state("nuevo_state")
```

## 🐛 Debugging y Resolución de Problemas

### Habilitar Logs Detallados

```python
# Al inicio de principal.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Problemas Comunes

#### 1. **Error: "pygame.error: No available video device"**

```bash
# Asegurar que tienes un sistema de ventanas
# En Linux, puede requerir X11 o Wayland
export DISPLAY=:0
```

#### 2. **Error: "FileNotFoundError: [Errno 2] No such file or directory: 'songs/...'**

```bash
# Verificar que estás en el directorio correcto
cd "Trabajo - Proyecto final"
python principal.py
```

#### 3. **El audio no se reproduce**

```python
# Verificar inicialización en audio_simple.py
# Añadir prints para debug:
def reproducir_musica(self, tipo):
    print(f"[DEBUG] Intentando reproducir: {tipo}")
    # ... resto del código
```

#### 4. **Guardado corrupto**

```bash
# Eliminar y regenerar save_game.json
rm save_game.json
python principal.py  # Se creará uno nuevo
```

### Herramientas de Debug

**Ver FPS en tiempo real:**

```python
# En principal.py, en el game loop:
print(f"FPS: {self.clock.get_fps():.1f}")
```

**Dibujar hitboxes:**

```python
# En entidades/cubo.py o pieza_geometrica.py
pygame.draw.circle(screen, (255, 0, 0),
                   (int(self.x), int(self.y)),
                   self.radio, 2)  # Borde rojo
```

**Modo de desarrollo:**

```python
# config/constantes.py
DEBUG_MODE = True

# En el código:
if DEBUG_MODE:
    print(f"Cubo en: ({self.x}, {self.y})")
```

## 🧪 Testing

### Testing Manual

```bash
# Ejecutar y probar cada nivel
python principal.py

# Checklist de pruebas:
☐ Menú principal funciona
☐ Selección de niveles funciona
☐ Nivel 1 completable
☐ Nivel 2 completable
☐ Nivel 3 completable
☐ Meteoros aparecen y dañan
☐ Portales teletransportan
☐ Power-ups funcionan
☐ Audio se reproduce
☐ Guardado/Carga funciona
☐ ESC muestra confirmación
☐ Pistas funcionan correctamente
```

### Testing de Rendimiento

```python
# Medir tiempo de actualización
import time

start = time.time()
self.current_game.update(dt)
elapsed = time.time() - start

if elapsed > 0.016:  # >16ms (60 FPS)
    print(f"⚠️ Update lento: {elapsed*1000:.2f}ms")
```

## 📝 Convenciones de Código

### Nombres

```python
# Clases: PascalCase
class GameCuboFase5:
    pass

# Funciones/métodos: snake_case
def calcular_puntuacion():
    pass

# Constantes: UPPER_SNAKE_CASE
SCREEN_WIDTH = 1280

# Variables privadas: _prefijo
def __init__(self):
    self._variable_interna = 0
```

### Documentación

```python
def metodo_ejemplo(self, parametro1, parametro2):
    """
    Descripción breve del método

    Args:
        parametro1: Descripción del parámetro
        parametro2: Descripción del parámetro

    Returns:
        Descripción del valor de retorno
    """
    pass
```

### Imports

```python
# 1. Librerías estándar
import json
import os

# 2. Librerías de terceros
import pygame
import numpy as np

# 3. Módulos locales
from config.constantes import *
from entidades.cubo import Cubo
```

## 🚀 Optimización

### Perfilado de Rendimiento

```python
import cProfile
import pstats

# Ejecutar con profiler
cProfile.run('game_manager.run()', 'output.prof')

# Analizar resultados
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 funciones lentas
```

### Optimizaciones Comunes

1. **Caché de superficies:**

```python
# En lugar de recrear cada frame:
self.surface = pygame.Surface((size, size))  # En __init__
# Reusar en draw()
```

2. **Limitar actualizaciones:**

```python
# Solo actualizar cuando sea necesario
if self.activo and not self.pausado:
    self.update(dt)
```

3. **Reducir llamadas a draw:**

```python
# Dibujar solo elementos visibles
if self.on_screen():
    self.draw(screen)
```

## 📦 Distribución

### Crear Ejecutable con PyInstaller

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --windowed --name "CUBO_Arquitecto_del_Caos" principal.py

# El ejecutable estará en dist/CUBO_Arquitecto_del_Caos.exe
```

### Empaquetar con Assets

```bash
# Incluir carpetas de recursos
pyinstaller --onefile --windowed \
    --add-data "songs;songs" \
    --add-data "niveles;niveles" \
    --name "CUBO_Arquitecto_del_Caos" principal.py
```

## 🔄 Control de Versiones (Git)

### Workflow Recomendado

```bash
# Crear rama para nueva característica
git checkout -b feature/nueva-caracteristica

# Hacer cambios y commits
git add .
git commit -m "Añadir nueva característica X"

# Mergear a main
git checkout main
git merge feature/nueva-caracteristica

# Subir cambios
git push origin main
```

### .gitignore Recomendado

```
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# Guardados
save_game*.json

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

## 📊 Métricas de Calidad

### Complejidad Ciclomática

- **Objetivo**: < 10 por función
- **Herramienta**: `radon cc core/ entidades/`

### Cobertura de Código

- **Objetivo**: > 70%
- **Herramienta**: `coverage run -m pytest`

## 🎓 Recursos Adicionales

### Documentación de Pygame

- [Pygame Docs](https://www.pygame.org/docs/)
- [Pygame Tutorial](https://realpython.com/pygame-a-primer/)

### Tutoriales Recomendados

- State machines en juegos
- Sistemas de partículas
- Detección de colisiones optimizada

## 🆘 Soporte

### Problemas Conocidos

1. **Audio retrasado**: Usar buffer más pequeño en mixer.init()
2. **Lag en muchos meteoros**: Limitar cantidad simultánea
3. **Guardado lento**: Reducir frecuencia de auto-guardado

### Contacto

- GitHub Issues: [Enlace al repositorio]
- Email: [email del desarrollador]

---

**Última actualización**: Diciembre 2025
**Versión del juego**: 1.0 (Sistema Simplificado)

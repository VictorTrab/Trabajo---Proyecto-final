# Arquitectura Técnica - CUBO: Arquitecto del Caos

## 🏗️ Visión General del Sistema

CUBO: Arquitecto del Caos implementa una arquitectura modular basada en el patrón **State Machine** para gestionar los diferentes estados del juego, con un sistema de herencia progresiva donde cada fase extiende las capacidades de la anterior.

## 📐 Arquitectura de Estados

### Máquina de Estados (`core/estados_juego.py`)

```
                    ┌─────────────────────────┐
                    │     GameManager         │
                    │  (Gestor Principal)     │
                    └───────────┬─────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼─────┐  ┌──────▼──────┐  ┌────▼─────┐
        │ MainMenu    │  │ LevelSelect │  │ Playing  │
        │  State      │  │   State     │  │  State   │
        └───────┬─────┘  └──────┬──────┘  └────┬─────┘
                │               │               │
        ┌───────┼───────┐       │      ┌────────┼────────┐
        │       │       │       │      │        │        │
    ┌───▼───┐┌──▼──┐┌──▼───┐   │  ┌───▼───┐┌───▼────┐┌──▼────┐
    │Profile││About││Settings│  │  │Victory││GameOver││Pause  │
    │ State ││State││ State  │  │  │ State ││ State  ││Dialog │
    └───────┘└─────┘└────────┘  │  └───────┘└────────┘└───────┘
                                 │
                        ┌────────▼────────┐
                        │  Transition     │
                        │     State       │
                        └─────────────────┘
```

**Estados Principales:**

| Estado               | Descripción                 | Transiciones                            |
| -------------------- | --------------------------- | --------------------------------------- |
| **MainMenuState**    | Menú principal con opciones | → LevelSelect, Profile, About, Settings |
| **LevelSelectState** | Selección de nivel (1-3)    | → Playing, MainMenu                     |
| **PlayingState**     | Juego activo (Fases 2-5)    | → Victory, GameOver, Pause              |
| **TransitionState**  | Animaciones de transición   | → LevelSelect, Playing                  |
| **ProfileState**     | Estadísticas del jugador    | → MainMenu                              |
| **AboutState**       | Información del juego       | → MainMenu                              |
| **SettingsState**    | Configuración de audio      | → MainMenu                              |

### Diagrama de Flujo Detallado

```
    ┌──────────┐
    │  INICIO  │
    └────┬─────┘
         │
         ▼
    ┌─────────────────┐
    │  MAIN MENU      │◄──────────────────┐
    │  - Jugar        │                   │
    │  - Perfil       │                   │
    │  - Acerca de    │                   │
    │  - Salir        │                   │
    └─┬───┬───┬───┬───┘                   │
      │   │   │   │                       │
      │   │   │   └─────► [SALIR]         │
      │   │   │                           │
      │   │   └───► ┌──────────────┐      │
      │   │         │   ACERCA DE  │      │
      │   │         │  - Info      │      │
      │   │         │  - Créditos  │──────┤
      │   │         └──────────────┘      │
      │   │                               │
      │   └─────► ┌──────────────────┐    │
      │           │     PERFIL       │    │
      │           │  - Progreso      │    │
      │           │  - Estadísticas  │────┤
      │           │  - Reiniciar     │    │
      │           └──────────────────┘    │
      │                                   │
      ▼                                   │
  ┌───────────────────┐                  │
  │  LEVEL SELECT     │                  │
  │  ┌───┐ ┌───┐ ┌───┐│                  │
  │  │ 1 │ │ 2 │ │ 3 ││                  │
  │  └───┘ └───┘ └───┘│                  │
  │  [VOLVER]         │──────────────────┤
  └─────────┬─────────┘                  │
            │                            │
            ▼                            │
      ┌──────────┐                       │
      │ PLAYING  │                       │
      │  Fase 5  │                       │
      └─┬──┬──┬──┘                       │
        │  │  │                          │
   ┌────┘  │  └────┐                     │
   │       │       │                     │
   ▼       ▼       ▼                     │
┌──────┐┌──────┐┌─────────┐              │
│PAUSE ││GAME  ││ VICTORY │              │
│      ││OVER  ││         │              │
│[ESC] │└──┬───┘└────┬────┘              │
└──┬───┘   │         │                   │
   │       │         │                   │
   │   ┌───▼─────────▼───────┐           │
   │   │   TRANSITION        │           │
   │   │  - Animación        │           │
   │   │  - Estadísticas     │           │
   └───►  - Continuar/Retry  ├───────────┘
       └─────────────────────┘
```

## 🎮 Sistema de Fases Progresivas

### Jerarquía de Herencia

```
GameCuboFase2 (Base)
    ↓
GameCuboFase3 (+ Puntuación y Niveles)
    ↓
GameCuboFase4 (+ Meteoros y Portales)
    ↓
GameCuboFase5 (+ Sistema Emocional)
```

### Fase 2: Base - Piezas y Magnetismo

**Archivo**: `core/logica_cubo_fase2.py`

**Responsabilidades:**

- Movimiento del cubo
- Recolección y colocación de piezas
- Sistema de magnetismo (atracción automática)
- Validación de figura objetivo
- Límite de tiempo (120s) y intentos (10)

**Componentes Clave:**

```python
class GameCuboFase2:
    - cubo: Cubo principal
    - piezas: Lista de piezas disponibles
    - figura_objetivo: Figura a completar
    - particle_system: Sistema de partículas
```

### Fase 3: Puntuación y Múltiples Niveles

**Archivo**: `core/logica_cubo_fase3.py`

**Responsabilidades:**

- Sistema de puntuación completo
- Generador de niveles desde JSON
- Sistema de pistas (3 por nivel)
- Validación avanzada de piezas
- Piezas distractor (3 extra)

**Componentes Clave:**

```python
class SistemaPuntuacion:
    # Valores hardcodeados en __init__
    - puntos_base: 1000
    - bonus_tiempo_max: 500
    - bonus_precision_max: 300
    - bonus_sin_errores: 200

class GeneradorNiveles:
    - cargar desde niveles.json
    - generar niveles aleatorios
    - calcular distractores
```

### Fase 4: Meteoros, Portales y Power-ups

**Archivo**: `core/logica_cubo_fase4.py`

**Responsabilidades:**

- Sistema de meteoros dinámicos
- Portales de teletransporte (2 pares)
- Power-ups aleatorios
- Validación de spawn (evitar colisiones)
- Gestión de vida del jugador

**Componentes Clave:**

```python
class GeneradorMeteoros:
    - intervalo: 5-8 segundos
    - velocidad: 200-300 px/s
    - zonas_prohibidas: portales

class SistemaPortales:
    - pares_portales: [(entrada, salida)]
    - cooldown por uso

class SistemaPowerUps:
    - tipos: escudo, velocidad, etc.
    - spawn aleatorio
```

### Fase 5: Sistema Emocional Avanzado

**Archivo**: `core/logica_cubo_fase5.py`

**Responsabilidades:**

- Estados emocionales del cubo
- Sistema de combos
- Efectos visuales emocionales
- Narrativa dinámica
- Ambiente emocional

**Componentes Clave:**

```python
class GameCuboFase5:
    - efectos_emocionales: Partículas emocionales
    - animador: Animaciones especiales
    - narrativa: Diálogos contextuales
    - combo: Sistema de multiplicadores
    - ambiente: Efectos ambientales
```

## 🎨 Sistema de Entidades

### Cubo (`entidades/cubo.py`)

```python
class Cubo:
    - posición (x, y)
    - velocidad
    - pieza_actual: Pieza sostenida
    - emocion: Estado emocional
    - vida: Puntos de vida

    Métodos:
    - mover(dx, dy)
    - recoger_pieza(pieza)
    - soltar_pieza()
    - cambiar_emocion(emocion, duracion)
```

### Piezas Geométricas (`entidades/pieza_geometrica.py`)

```python
class PiezaGeometrica:
    TIPOS:
    - CUADRADO
    - TRIANGULO
    - CIRCULO
    - ROMBO
    - RECTANGULO

    Propiedades:
    - tipo
    - posición (x, y)
    - rotación (0°, 90°, 180°, 270°)
    - color
    - sostenida: bool

class FiguraObjetivo:
    - definicion: lista de piezas esperadas
    - verificar_completitud()
    - dibujar_guia()
```

### Meteoros (`entidades/meteoro.py`)

```python
class Meteoro:
    - posición, velocidad
    - advertencia_timer: 1s
    - rotación dinámica
    - trail_particles: estela

class GeneradorMeteoros:
    - generar según intervalo
    - validar zonas prohibidas
    - gestionar lista activa
```

### Portales (`entidades/portal.py`)

```python
class Portal:
    - tipo: ENTRADA o SALIDA
    - pareja: Portal conectado
    - cooldown: evitar bucles

class SistemaPortales:
    - crear pares
    - teletransportar(cubo)
    - dibujar con animaciones
```

### Power-ups (`entidades/powerup.py`)

```python
class PowerUp:
    TIPOS:
    - ESCUDO: protección temporal
    - VELOCIDAD: movimiento rápido
    - TIEMPO: +30 segundos

class SistemaPowerUps:
    - spawn aleatorio
    - aplicar_efecto(cubo)
    - duración limitada
```

## 🎵 Sistema de Audio

### AudioDinamico (`entidades/audio_dinamico.py`)

Sistema de audio unificado enfocado en jugabilidad.

```python
class AudioDinamico:
    Música:
    - "menu": Menú principal
    - "nivel1", "nivel2", "nivel3": Música específica por nivel
    - "completado": Nivel completado
    - "game_over": Derrota
    - "creditos": Pantalla de créditos

    Efectos de Jugabilidad:
    - "click": Click en botones y selecciones de menú
    - "rotar": Rotar piezas
    - "colocar": Colocar piezas
    - "explotar": Explosiones
    - "colision_borde": Colisiones con bordes
    - "error": Errores generales
    - "salir_nivel": Salir del nivel
    - "iniciar_nivel": Iniciar nivel

    Métodos:
    - reproducir_musica(tipo)
    - reproducir_musica_nivel(nivel_numero)
    - reproducir_efecto(nombre)
    - cambiar_volumen_musica(volumen)
    - cambiar_volumen_efectos(volumen)
    - detener_musica()
    - pausar_musica()
    - reanudar_musica()
    - limpiar()
```

**Características:**

- Sistema de caché para efectos de sonido (optimización)
- Validación de archivos antes de reproducir
- Control independiente de volúmenes (música: 0.5, efectos: 0.7)
- Manejo robusto de errores (no crashea si falta audio)
- Sonido de click integrado en todas las selecciones de menú

## 💾 Sistema de Persistencia

### Jugador (`config/jugador.py`)

```python
class Player:
    Datos:
    - name: Nombre del jugador
    - levels_completed: {nivel: bool}
    - best_scores: {nivel: {attempts, time}}
    - unlocked_levels: int

    Métodos:
    - complete_level(nivel, attempts, time)
    - save() → save_game.json
    - load() → Player instance
```

### Formato de Guardado (JSON)

```json
{
  "name": "Jugador",
  "levels_completed": {
    "1": true,
    "2": false,
    "3": false
  },
  "best_scores": {
    "1": { "attempts": 0, "time": 45.5 },
    "2": null,
    "3": null
  },
  "unlocked_levels": 2
}
```

## 🎨 Sistema de Renderizado

### Menú (`entidades/sistema_menu.py`)

```python
class Menu:
    Componentes:
    - draw_main_menu()
    - draw_level_select()
    - draw_profile()
    - draw_about()
    - draw_settings()
    - draw_confirmation_dialog()

    Efectos:
    - Fondo animado con ondas
    - Texto con glow (resplandor)
    - Pulso en opciones seleccionadas
    - Partículas de fondo
```

### Sistema de Partículas (`entidades/sistema_particulas.py`)

```python
class ParticleSystem:
    Tipos:
    - Explosión (al colocar pieza)
    - Estela (meteoros)
    - Ambiente (fondo)
    - Emocional (estados del cubo)

    Propiedades:
    - posición, velocidad
    - color, alpha (transparencia)
    - vida útil
    - gravedad
```

## 🔧 Configuración

### Constantes (`config/constantes.py`)

```python
# Pantalla
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 90

# Juego
TOTAL_LEVELS = 3
TIME_LIMIT = 90  # segundos

# Colores Cyberpunk
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_PURPLE = (138, 43, 226)
NEON_GREEN = (57, 255, 20)
NEON_ORANGE = (255, 140, 0)
```

## 🔄 Ciclo de Actualización (Game Loop)

```
┌─────────────────────────────────────┐
│         Game Manager Loop           │
└─────────────────────────────────────┘
           │
           ↓
    ┌──────────────┐
    │ Handle Input │ ← Eventos de teclado/ratón
    └──────┬───────┘
           │
           ↓
    ┌──────────────┐
    │    Update    │ ← Lógica del juego (dt)
    └──────┬───────┘
           │
           ├─→ Update Cubo
           ├─→ Update Piezas
           ├─→ Update Meteoros
           ├─→ Update Portales
           ├─→ Update Power-ups
           ├─→ Update Efectos
           ├─→ Check Colisiones
           └─→ Check Completitud
           │
           ↓
    ┌──────────────┐
    │     Draw     │ ← Renderizado
    └──────┬───────┘
           │
           ├─→ Draw Fondo
           ├─→ Draw Objetivo
           ├─→ Draw Piezas
           ├─→ Draw Cubo
           ├─→ Draw Meteoros
           ├─→ Draw Portales
           ├─→ Draw UI
           └─→ Draw Efectos
           │
           ↓
    ┌──────────────┐
    │    Flip      │ ← Actualizar pantalla
    └──────────────┘
```

## 🧩 Patrones de Diseño Utilizados

### 1. **State Pattern**

- GameManager gestiona estados
- Cambios de estado mediante `change_state()`

### 2. **Inheritance (Herencia Progresiva)**

- Cada fase extiende la anterior
- Reuso de código y funcionalidad acumulativa

### 3. **Singleton (Audio)**

- Una sola instancia de AudioDinamico en GameManager
- Acceso global mediante `self.manager.audio`
- Sistema unificado sin duplicación de código

### 4. **Observer (Implícito)**

- Sistema de callbacks para eventos
- Ejemplo: `on_pieza_colocada()`

### 5. **Factory (Generadores)**

- GeneradorMeteoros
- GeneradorNiveles
- SistemaPowerUps

## 📊 Métricas de Rendimiento

### Optimizaciones

- **Delta Time (dt)**: Actualización basada en tiempo real
- **Caché de superficies**: Piezas pre-renderizadas
- **Culling**: Solo dibujar elementos visibles
- **Límite de partículas**: Máximo de 500 activas

### FPS Target

- **Objetivo**: 60 FPS
- **Clock de Pygame**: Control de frame rate
- **Render condicional**: Solo actualizar cuando sea necesario

## 🐛 Debugging y Logging

### Mensajes del Sistema

```python
[AudioDinamico] Sistema de audio inicializado
[AudioDinamico] Efecto cargado exitosamente: click -> songs/SongClick.mp3
[AudioDinamico] Reproduciendo efecto: click
[GeneradorMeteoros] Meteoro generado en (x, y)
[SistemaPortales] Teletransporte: Portal 1 → Portal 2
```

### Validación de Audio

- Verificación automática de existencia de archivos
- Mensajes de error descriptivos si falta un archivo
- Sistema robusto que no crashea por archivos faltantes

## 🚀 Extensibilidad

### Añadir un Nuevo Nivel

1. Editar `niveles/niveles.json`
2. Incrementar `TOTAL_LEVELS` en constantes
3. Reiniciar el juego

### Añadir un Nuevo Tipo de Pieza

1. Definir constante en `PiezaGeometrica`
2. Agregar lógica de dibujado
3. Actualizar generador de niveles

### Añadir un Nuevo Estado Emocional

1. Agregar constante en `Cubo`
2. Definir color y efectos en `EfectosEmocionales`
3. Actualizar lógica de cambio de emoción

## 📦 Dependencias

```
pygame==2.6.1      # Motor de juego
numpy>=1.24.0      # Cálculos matemáticos
```

## 🔐 Seguridad y Validación

### Validaciones Implementadas

- **Límites de pantalla**: Cubo no puede salir
- **Colisiones**: Detección precisa
- **Zonas prohibidas**: Spawn seguro de meteoros
- **Cooldown de portales**: Evitar bucles infinitos
- **Validación de guardado**: Integridad del JSON

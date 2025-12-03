# CUBO: Arquitecto del Caos

## Resumen del Proyecto - Informe Académico

---

## 1. INFORMACIÓN GENERAL DEL PROYECTO

### 1.1 Datos Básicos

- **Nombre del Proyecto:** CUBO: Arquitecto del Caos
- **Versión:** 3.6
- **Autores:** V.H & R.
- **Año:** 2025
- **Propósito:** Proyecto de Informática Gráfica
- **Tipo:** Videojuego Educativo - Puzzle Geométrico
- **Licencia:** Uso Educativo

### 1.2 Descripción General

CUBO: Arquitecto del Caos es un videojuego de puzzle 3D desarrollado en Python que combina transformaciones geométricas, física computacional y elementos de diseño cyberpunk. El proyecto implementa conceptos avanzados de informática gráfica incluyendo transformaciones matriciales, detección de colisiones, sistemas de partículas y renderizado 2D con efectos visuales.

---

## 2. OBJETIVOS DEL PROYECTO

### 2.1 Objetivos Generales

- Desarrollar un videojuego funcional que demuestre la aplicación práctica de conceptos de informática gráfica
- Implementar un sistema de transformaciones geométricas interactivo
- Crear una experiencia de usuario atractiva mediante efectos visuales y audio

### 2.2 Objetivos Específicos

1. Implementar transformaciones geométricas 2D (traslación, rotación, escala)
2. Desarrollar un sistema de detección de colisiones preciso
3. Crear un sistema de física básico para objetos dinámicos
4. Implementar efectos visuales avanzados (partículas, animaciones, glows)
5. Diseñar una interfaz de usuario intuitiva con estética cyberpunk
6. Desarrollar un sistema de progresión por niveles
7. Implementar persistencia de datos (guardado/carga de progreso)

---

## 3. TECNOLOGÍAS Y HERRAMIENTAS

### 3.1 Lenguajes y Frameworks

- **Python 3.10.0:** Lenguaje principal de desarrollo
- **Pygame 2.6.1:** Framework para desarrollo de videojuegos
- **NumPy:** Operaciones matemáticas y matriciales
- **JSON:** Almacenamiento de datos y configuración

### 3.2 Entorno de Desarrollo

- **Editor:** Visual Studio Code
- **Control de Versiones:** Git/GitHub
- **Gestión de Dependencias:** pip, venv (entorno virtual)
- **Sistema Operativo:** Windows

### 3.3 Recursos Multimedia

- **Audio:** MP3 (música de fondo y efectos de sonido)
- **Fuentes:** Sistema de fuentes de Pygame
- **Gráficos:** Generación procedural con Pygame

---

## 4. ARQUITECTURA DEL SOFTWARE

### 4.1 Patrón de Diseño

El proyecto implementa el **patrón State (Estado)** para gestionar las diferentes pantallas y estados del juego:

```
GameManager (Gestor Principal)
├── MainMenuState (Menú Principal)
├── LevelSelectState (Selección de Nivel)
├── PlayingState (Jugando)
├── TransitionState (Transición entre niveles)
├── LevelTransitionState (Transición animada)
├── ProfileState (Perfil del jugador)
└── AboutState (Acerca de)
```

### 4.2 Estructura de Directorios

```
proyecto/
├── principal.py              # Punto de entrada principal
├── config/                   # Configuración del juego
│   ├── constantes.py        # Constantes globales
│   └── jugador.py           # Sistema de jugador
├── core/                     # Lógica central del juego
│   ├── estados_juego.py     # Máquina de estados
│   ├── logica_cubo_fase2.py # Sistema base
│   ├── logica_cubo_fase3.py # Sistema de puntuación
│   ├── logica_cubo_fase4.py # Meteoros y portales
│   └── logica_cubo_fase5.py # Sistema emocional
├── entidades/               # Entidades del juego
│   ├── cubo.py             # Cubo principal
│   ├── pieza_geometrica.py # Piezas del puzzle
│   ├── sistema_menu.py     # Sistema de menús
│   ├── sistema_particulas.py # Sistema de partículas
│   ├── audio_simple.py     # Sistema de audio
│   ├── meteoro.py          # Sistema de meteoros
│   ├── portal.py           # Sistema de portales
│   └── powerup.py          # Sistema de power-ups
├── docs/                    # Documentación
│   ├── README_JUEGO.md
│   ├── ARQUITECTURA_TECNICA.md
│   ├── GUIA_DESARROLLO.md
│   └── RESUMEN_PROYECTO.md
└── songs/                   # Recursos de audio
```

### 4.3 Flujo del Programa

```
Inicio
  ↓
Inicialización (Pygame, Audio, Jugador)
  ↓
Menú Principal → Selección de Nivel → Jugando
  ↓                     ↓                ↓
Perfil              Acerca de      Game Over / Nivel Completado
  ↓                     ↓                ↓
Reiniciar Progreso  Volver         Reintentar / Siguiente Nivel
  ↓                     ↓                ↓
←─────────────────── Menú Principal ─────────────────→
```

---

## 5. CARACTERÍSTICAS IMPLEMENTADAS

### 5.1 Sistema de Transformaciones Geométricas

#### 5.1.1 Transformaciones Soportadas

- **Traslación:** Movimiento en el plano 2D (ejes X, Y)
- **Rotación:** Giro alrededor del centro de la pieza
- **Escala:** Aumento/reducción del tamaño

#### 5.1.2 Implementación Matemática

```python
# Matrices de transformación 2D
Traslación: T(dx, dy) = [x + dx, y + dy]
Rotación: R(θ) = [x*cos(θ) - y*sin(θ), x*sin(θ) + y*cos(θ)]
Escala: S(sx, sy) = [x*sx, y*sy]
```

#### 5.1.3 Controles

- **Flechas (↑↓←→):** Traslación de piezas
- **Q/E:** Rotación en sentido antihorario/horario
- **A/D:** Escala (reducir/aumentar)
- **Rueda del ratón:** Rotación alternativa
- **Clic izquierdo:** Arrastrar piezas
- **Espacio:** Usar pista (cuando disponible)

### 5.2 Sistema de Física

#### 5.2.1 Detección de Colisiones

- **Colisión AABB (Axis-Aligned Bounding Box):** Para piezas rectangulares
- **Colisión Circular:** Para meteoros y efectos
- **Colisión Píxel-Perfect:** Para validación precisa de encaje

#### 5.2.2 Magnetismo y Snap

- Sistema de "snap" para alinear piezas automáticamente
- Tolerancia configurable (20 píxeles por defecto)
- Zonas de atracción en el cubo principal

#### 5.2.3 Física de Meteoros (Fase 4)

- Trayectorias balísticas
- Velocidad variable según dificultad
- Colisiones elásticas con objetos

### 5.3 Sistema de Partículas

#### 5.3.1 Tipos de Efectos

1. **Explosión (Burst):** Partículas que se expanden desde un punto
2. **Lluvia:** Partículas que caen verticalmente
3. **Chispas:** Efectos de colisión
4. **Trail:** Estelas de movimiento

#### 5.3.2 Propiedades

- Color personalizable
- Tiempo de vida variable
- Física gravitacional
- Fade out progresivo

### 5.4 Sistema de Niveles

#### 5.4.1 Estructura de Niveles

El juego cuenta con **3 niveles** con dificultad progresiva:

**Nivel 1: Tutorial**

- Figura simple (3-4 piezas)
- Sin obstáculos
- Tiempo límite: 120 segundos
- Introducción a mecánicas básicas

**Nivel 2: Intermedio**

- Figura más compleja (5-6 piezas)
- Meteoros ocasionales
- 1 par de portales
- Power-ups básicos

**Nivel 3: Avanzado**

- Figura compleja (7-8 piezas)
- Múltiples meteoros
- 2 pares de portales
- Power-ups variados

#### 5.4.2 Sistema de Progresión

- Desbloqueo secuencial de niveles
- Guardado automático del progreso
- Registro de mejores tiempos
- Sistema de reinicio de progreso

### 5.5 Sistema de Puntuación (Fase 3)

#### 5.5.1 Cálculo de Puntuación

```
Puntuación Base: 1000 puntos

Bonificaciones:
+ Bonus de Tiempo: hasta 500 puntos (más rápido = más puntos)
+ Bonus de Precisión: hasta 300 puntos (menos piezas extra)
+ Sin Errores: 200 puntos (cero intentos fallidos)

Penalizaciones:
- Intentos Fallidos: -25 puntos por intento
- Uso de Pistas: -100 puntos por pista usada

Puntuación Final = Base + Bonificaciones - Penalizaciones
```

#### 5.5.2 Sistema de Estrellas

- ⭐⭐⭐ (3 estrellas): ≥ 1500 puntos
- ⭐⭐ (2 estrellas): ≥ 1000 puntos
- ⭐ (1 estrella): < 1000 puntos

### 5.6 Mecánicas Avanzadas (Fase 4 y 5)

#### 5.6.1 Meteoros

- Generación procedural con zonas prohibidas
- Trayectorias calculadas con física
- Daño al impacto
- Efectos visuales de explosión

#### 5.6.2 Portales

- Teletransportación instantánea
- Múltiples pares por nivel
- Efectos visuales de entrada/salida
- Conexión bidireccional

#### 5.6.3 Power-ups

1. **Escudo:** Protección temporal contra meteoros
2. **Tiempo Extra:** +30 segundos al reloj
3. **Slowmo:** Ralentiza meteoros

#### 5.6.4 Sistema Emocional del Cubo

El cubo principal responde emocionalmente a eventos:

- **😊 Feliz:** Al completar nivel o colocar pieza correctamente
- **😢 Triste:** Al fallar o perder tiempo
- **😨 Miedo:** Cuando hay muchos meteoros
- **😣 Dolor:** Al recibir impacto
- **💪 Determinado:** Con escudo activo o cerca de completar

---

## 6. SISTEMA DE AUDIO

### 6.1 Música de Fondo

- **SongMenu.mp3:** Menú principal
- **Nivel1.mp3:** Música del nivel 1
- **Nivel2.mp3:** Música del nivel 2
- **Nivel3.mp3:** Música del nivel 3
- **SongJugarNivel.mp3:** Nivel completado
- **SongGameOver.mp3:** Game over
- **SongCreditos.mp3:** Pantalla "Acerca de"
- **SongGameStart.mp3:** Inicio de juego

### 6.2 Efectos de Sonido

- **SongClick.mp3:** Interacción con menús
- **SongRotarFigura.mp3:** Rotar piezas
- **SongColisionBordeVentana.mp3:** Errores y colisiones
- **SongExplocion.mp3:** Impacto de meteoros
- **SongSalirDeNivel.mp3:** Salir al menú
- **SongJugarNivel.mp3:** Iniciar nivel

### 6.3 Implementación

```python
class AudioSimple:
    - Singleton para gestión centralizada
    - Caché de efectos para optimización
    - Control de volumen independiente (música/efectos)
    - Reproducción por tipo de evento
```

---

## 7. INTERFAZ DE USUARIO

### 7.1 Estética Cyberpunk

#### 7.1.1 Paleta de Colores

```python
NEON_PINK = (255, 16, 240)      # Magenta neón
NEON_CYAN = (0, 255, 255)       # Cyan brillante
NEON_PURPLE = (138, 43, 226)    # Púrpura eléctrico
NEON_GREEN = (57, 255, 20)      # Verde neón
NEON_BLUE = (0, 191, 255)       # Azul eléctrico
NEON_ORANGE = (255, 165, 0)     # Naranja neón
NEON_YELLOW = (255, 255, 0)     # Amarillo brillante
BG_DARK = (10, 0, 20)           # Fondo oscuro
```

#### 7.1.2 Efectos Visuales

1. **Glow Effect:** Resplandor en textos importantes
2. **Breathing Animation:** Pulsación de elementos de fondo
3. **Wave Effect:** Ondas reactivas al cursor
4. **Particle Systems:** Efectos de explosión y movimiento
5. **Pulse Animation:** Pulsación en elementos seleccionados

### 7.2 Pantallas del Juego

#### 7.2.1 Menú Principal

- Título con efecto 3D y pulsación
- 5 opciones navegables:
  1. Jugar (inicio rápido)
  2. Niveles (selección manual)
  3. Perfil (estadísticas del jugador)
  4. Acerca de (créditos)
  5. Salir
- Fondo animado con teselado hexagonal

#### 7.2.2 Selección de Niveles

- Vista de cuadrícula horizontal (3 niveles)
- Indicadores visuales:
  - ✓ COMPLETO (verde) - Nivel completado
  - DISPONIBLE (cyan) - Nivel desbloqueado
  - 🔒 BLOQUEADO (gris) - Nivel no disponible
- Mejores tiempos mostrados por nivel

#### 7.2.3 Pantalla de Juego

**HUD (Heads-Up Display):**

- Timer: Tiempo restante (MM:SS)
- Intentos: Contador de intentos fallidos
- Nivel: Número del nivel actual
- Piezas: Colocadas/Total necesarias
- Objetivo: Vista previa de la figura completa
- Indicadores de power-ups activos

#### 7.2.4 Perfil del Jugador

- Panel central con estadísticas:
  - Nombre del jugador
  - Niveles completados (X/3)
  - Progreso total (%)
  - Niveles desbloqueados
- Mejores tiempos por nivel (MM:SS)
- Barra de progreso visual
- Opciones:
  - Volver al menú
  - Reiniciar progreso (con confirmación)

#### 7.2.5 Acerca de

- Información del proyecto:
  - Versión 3.6
  - Autores
  - Propósito académico
  - Licencia
- Características del juego
- Copyright

#### 7.2.6 Pantalla de Transición

- Snapshot del nivel con efecto blur
- Dos variantes:
  1. **Nivel Completado:**
     - Mensaje de felicitación
     - Estadísticas (puntos, estrellas, tiempo)
     - Opción: Continuar
  2. **Game Over:**
     - Mensaje de fallo
     - Causa (tiempo agotado/sin intentos)
     - Opciones: Reintentar / Menú

### 7.3 Sistema de Diálogos

#### 7.3.1 Diálogo de Confirmación de Salida

- Aparece al presionar ESC durante el juego
- Opciones: SÍ / NO
- Por defecto en "NO"
- Overlay semi-transparente

#### 7.3.2 Diálogo de Reinicio de Progreso

- Advertencia visual (icono ⚠)
- Mensaje: "¿Reiniciar todo el progreso?"
- Advertencia: "Esta acción no se puede deshacer"
- Opciones: SÍ, REINICIAR / NO, CANCELAR
- Por defecto en "NO, CANCELAR"
- Borde naranja (peligro)

---

## 8. PERSISTENCIA DE DATOS

### 8.1 Sistema de Guardado

#### 8.1.1 Archivo de Guardado

```json
{
  "name": "Jugador",
  "levels_completed": {
    "1": true,
    "2": true,
    "3": false
  },
  "best_scores": {
    "1": { "attempts": 0, "time": 45.2 },
    "2": { "attempts": 0, "time": 78.5 },
    "3": null
  },
  "total_levels_completed": 2,
  "unlocked_levels": 3
}
```

#### 8.1.2 Ubicación

- **Ruta:** `config/player_save.json`
- **Formato:** JSON
- **Codificación:** UTF-8

#### 8.1.3 Funcionalidades

- **Guardado automático:** Al completar nivel
- **Carga automática:** Al iniciar el juego
- **Validación de datos:** Manejo de formatos antiguos
- **Migración de datos:** Compatible con versiones anteriores

### 8.2 Clase Player

```python
class Player:
    def __init__(self, name="Jugador"):
        self.name = name
        self.levels_completed = {1: False, 2: False, 3: False}
        self.best_scores = {1: None, 2: None, 3: None}
        self.total_levels_completed = 0
        self.unlocked_levels = 1

    def complete_level(level, attempts, time):
        # Marca nivel como completado
        # Actualiza mejor puntuación
        # Desbloquea siguiente nivel

    def is_level_unlocked(level):
        # Verifica si un nivel está disponible

    def reset_progress():
        # Reinicia todo el progreso

    def save():
        # Guarda en JSON

    @staticmethod
    def load():
        # Carga desde JSON
```

---

## 9. CONCEPTOS DE INFORMÁTICA GRÁFICA APLICADOS

### 9.1 Transformaciones Geométricas 2D

#### 9.1.1 Matrices de Transformación

```
Matriz de Traslación:
[1  0  tx]
[0  1  ty]
[0  0  1 ]

Matriz de Rotación:
[cos(θ)  -sin(θ)  0]
[sin(θ)   cos(θ)  0]
[0        0       1]

Matriz de Escala:
[sx  0   0]
[0   sy  0]
[0   0   1]
```

#### 9.1.2 Composición de Transformaciones

Las transformaciones se aplican mediante multiplicación matricial, permitiendo combinar múltiples operaciones en una sola transformación compuesta.

### 9.2 Sistema de Coordenadas

#### 9.2.1 Espacio de la Pantalla

- Origen: Esquina superior izquierda (0, 0)
- Eje X: Positivo hacia la derecha
- Eje Y: Positivo hacia abajo
- Resolución: 1200 x 800 píxeles

#### 9.2.2 Espacio del Objeto

Cada pieza geométrica mantiene:

- Posición en coordenadas del mundo (x, y)
- Rotación en grados
- Escala relativa (sx, sy)
- Centro de transformación

### 9.3 Renderizado

#### 9.3.1 Pipeline de Renderizado

```
1. Actualización de Lógica (Update)
   ↓
2. Cálculo de Transformaciones
   ↓
3. Detección de Colisiones
   ↓
4. Renderizado de Fondo
   ↓
5. Renderizado de Entidades
   ↓
6. Renderizado de Partículas
   ↓
7. Renderizado de UI
   ↓
8. Presentación en Pantalla (Flip)
```

#### 9.3.2 Capas de Renderizado

1. **Capa 0 (Fondo):** Teselado animado
2. **Capa 1 (Juego):** Piezas, cubo, meteoros
3. **Capa 2 (Efectos):** Partículas, portales
4. **Capa 3 (UI):** HUD, menús
5. **Capa 4 (Overlays):** Diálogos, transiciones

### 9.4 Detección de Colisiones

#### 9.4.1 Algoritmo AABB (Axis-Aligned Bounding Box)

```python
def aabb_collision(rect1, rect2):
    return (rect1.x < rect2.x + rect2.width and
            rect1.x + rect1.width > rect2.x and
            rect1.y < rect2.y + rect2.height and
            rect1.y + rect1.height > rect2.y)
```

#### 9.4.2 Colisión Circular

```python
def circle_collision(c1_pos, c1_radius, c2_pos, c2_radius):
    distance = sqrt((c1_pos.x - c2_pos.x)² + (c1_pos.y - c2_pos.y)²)
    return distance < (c1_radius + c2_radius)
```

#### 9.4.3 Optimizaciones

- Spatial partitioning (cuadrícula)
- Early exit en colisiones complejas
- Uso de bounding boxes antes de píxel-perfect

### 9.5 Sistemas de Partículas

#### 9.5.1 Modelo de Partícula

```python
class Particle:
    position: Vector2D
    velocity: Vector2D
    acceleration: Vector2D (gravity)
    color: RGB
    lifetime: float
    age: float
    size: float
```

#### 9.5.2 Física de Partículas

```
Actualización por frame:
position += velocity * dt
velocity += acceleration * dt
age += dt
alpha = 1 - (age / lifetime)  # Fade out
```

### 9.6 Interpolación y Animación

#### 9.6.1 Interpolación Lineal (LERP)

```python
def lerp(start, end, t):
    return start + (end - start) * t
```

#### 9.6.2 Easing Functions

- Sin/Cos para movimientos suaves
- Cubic easing para aceleración/desaceleración
- Bounce para efectos elásticos

### 9.7 Optimización de Rendimiento

#### 9.7.1 Técnicas Implementadas

1. **Object Pooling:** Reutilización de partículas
2. **Dirty Flag:** Solo redibujar cuando hay cambios
3. **Culling:** No procesar objetos fuera de pantalla
4. **Caché:** Superficies pre-renderizadas
5. **Delta Time:** Movimiento independiente del framerate

#### 9.7.2 Framerate

- **Target:** 60 FPS
- **V-Sync:** Habilitado
- **Delta Time:** Calculado por frame para consistencia

---

## 10. DESAFÍOS Y SOLUCIONES

### 10.1 Desafíos Técnicos

#### 10.1.1 Detección Precisa de Encaje

**Problema:** Validar si una pieza encaja exactamente en su posición objetivo.

**Solución:**

- Implementación de tolerancia configurable (20 píxeles)
- Comparación de múltiples puntos de la pieza
- Sistema de "snap" para alineación automática
- Validación de rotación y escala

#### 10.1.2 Rendimiento con Muchas Partículas

**Problema:** Degradación del rendimiento con cientos de partículas activas.

**Solución:**

- Object pooling para reutilización
- Límite máximo de partículas simultáneas
- Eliminación temprana de partículas muertas
- Optimización del loop de actualización

#### 10.1.3 Gestión de Estados del Juego

**Problema:** Transiciones complejas entre estados.

**Solución:**

- Implementación del patrón State
- Máquina de estados finitos
- Datos de transición para contexto
- Estados independientes y desacoplados

#### 10.1.4 Sincronización de Audio

**Problema:** Retrasos y solapamiento de efectos de sonido.

**Solución:**

- Sistema de caché de sonidos
- Canal dedicado para música
- Múltiples canales para efectos
- Gestión de volumen independiente

### 10.2 Desafíos de Diseño

#### 10.2.1 Curva de Aprendizaje

**Problema:** Hacer el juego accesible pero desafiante.

**Solución:**

- Nivel 1 como tutorial con mecánicas básicas
- Introducción gradual de elementos nuevos
- Sistema de pistas para jugadores atascados
- Feedback visual claro

#### 10.2.2 Balance de Dificultad

**Problema:** Ajustar la dificultad de cada nivel.

**Solución:**

- Pruebas iterativas con usuarios
- Ajuste de tiempos límite
- Escalado gradual de complejidad
- Sistema de puntuación que recompensa eficiencia

---

## 11. PRUEBAS Y VALIDACIÓN

### 11.1 Tipos de Pruebas Realizadas

#### 11.1.1 Pruebas Funcionales

- ✓ Todas las transformaciones geométricas funcionan correctamente
- ✓ Sistema de colisiones detecta impactos precisamente
- ✓ Guardado y carga de progreso funciona sin pérdida de datos
- ✓ Transiciones entre estados sin errores
- ✓ Audio se reproduce en momentos correctos

#### 11.1.2 Pruebas de Usabilidad

- ✓ Controles intuitivos y responsivos
- ✓ Menús navegables con teclado y ratón
- ✓ Feedback visual claro en todas las acciones
- ✓ Tiempos de respuesta aceptables

#### 11.1.3 Pruebas de Rendimiento

- ✓ Mantiene 60 FPS en hardware de gama media
- ✓ No hay memory leaks en sesiones prolongadas
- ✓ Carga de archivos instantánea
- ✓ Transiciones suaves sin stuttering

### 11.2 Casos de Prueba Principales

| ID  | Caso de Prueba                  | Resultado |
| --- | ------------------------------- | --------- |
| T01 | Completar nivel 1               | ✓ Pasa    |
| T02 | Game over por tiempo            | ✓ Pasa    |
| T03 | Guardar y cargar progreso       | ✓ Pasa    |
| T04 | Reiniciar progreso              | ✓ Pasa    |
| T05 | Colisión con meteoros           | ✓ Pasa    |
| T06 | Teletransportación por portales | ✓ Pasa    |
| T07 | Uso de power-ups                | ✓ Pasa    |
| T08 | Navegación de menús             | ✓ Pasa    |
| T09 | Reproducción de audio           | ✓ Pasa    |
| T10 | Efectos visuales                | ✓ Pasa    |

---

## 12. RESULTADOS Y CONCLUSIONES

### 12.1 Logros del Proyecto

#### 12.1.1 Técnicos

- ✓ Implementación exitosa de transformaciones geométricas 2D
- ✓ Sistema de física funcional y realista
- ✓ Renderizado eficiente con efectos visuales avanzados
- ✓ Arquitectura modular y mantenible
- ✓ Sistema de audio completo e inmersivo

#### 12.1.2 Educativos

- ✓ Aplicación práctica de conceptos de informática gráfica
- ✓ Comprensión profunda de matemáticas para gráficos
- ✓ Experiencia en desarrollo de videojuegos
- ✓ Implementación de patrones de diseño
- ✓ Gestión de proyecto de software completo

#### 12.1.3 De Diseño

- ✓ Estética visual coherente (cyberpunk)
- ✓ Experiencia de usuario pulida
- ✓ Progresión de dificultad balanceada
- ✓ Interfaz intuitiva y accesible

### 12.2 Estadísticas del Proyecto

```
Líneas de Código:        ~15,000 líneas
Archivos de Código:      25 archivos .py
Clases Implementadas:    35+ clases
Métodos/Funciones:       200+ métodos
Archivos de Audio:       13 archivos
Documentación:           4 documentos completos
Tiempo de Desarrollo:    [Período de desarrollo]
Commits:                 [Número de commits]
```

### 12.3 Aprendizajes Clave

1. **Matemáticas Gráficas:**

   - Dominio de transformaciones matriciales
   - Aplicación de álgebra lineal
   - Geometría computacional

2. **Programación:**

   - Patrones de diseño (State, Singleton)
   - Programación orientada a objetos
   - Gestión de eventos
   - Optimización de rendimiento

3. **Desarrollo de Videojuegos:**

   - Game loop y delta time
   - Sistemas de partículas
   - Física 2D
   - UI/UX para juegos

4. **Gestión de Proyecto:**
   - Control de versiones
   - Documentación técnica
   - Testing y debugging
   - Refactorización de código

### 12.4 Limitaciones Conocidas

1. **Técnicas:**

   - Limitado a 2D (sin perspectiva 3D real)
   - Sin multijugador
   - Sin editor de niveles en tiempo real

2. **Contenido:**

   - Solo 3 niveles (extensible a más)
   - Figuras objetivo predefinidas
   - Sin personalización visual del jugador

3. **Plataforma:**
   - Optimizado para Windows
   - Requiere instalación de dependencias

### 12.5 Trabajo Futuro

#### 12.5.1 Mejoras Planificadas

- [ ] Editor de niveles visual
- [ ] Más niveles (5-10 adicionales)
- [ ] Modo multijugador (competitivo/cooperativo)
- [ ] Clasificaciones en línea
- [ ] Logros y trofeos
- [ ] Soporte para gamepad

#### 12.5.2 Características Avanzadas

- [ ] Figuras 3D con rotación isométrica
- [ ] Generación procedural de niveles
- [ ] Modo historia con narrativa
- [ ] Banda sonora dinámica
- [ ] Shaders para efectos visuales

#### 12.5.3 Multiplataforma

- [ ] Exportación a ejecutable standalone
- [ ] Versión web (Pygame Web)
- [ ] Versión móvil (Pygame Subset for Android)

---

## 13. INSTRUCCIONES DE USO

### 13.1 Requisitos del Sistema

#### 13.1.1 Mínimos

- **SO:** Windows 10 o superior
- **Python:** 3.10.0 o superior
- **RAM:** 2 GB
- **Almacenamiento:** 50 MB
- **Resolución:** 1200x800 o superior

#### 13.1.2 Dependencias

```
pygame==2.6.1
numpy>=1.21.0
```

### 13.2 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/VictorTrab/Trabajo---Proyecto-final.git

# 2. Navegar al directorio
cd "Trabajo - Proyecto final"

# 3. Crear entorno virtual
python -m venv .venv

# 4. Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 5. Instalar dependencias
pip install -r requirements.txt
```

### 13.3 Ejecución

```bash
# Ejecutar el juego
python principal.py
```

### 13.4 Controles del Juego

#### 13.4.1 En el Menú

- **↑↓ o ←→:** Navegar opciones
- **ENTER:** Seleccionar
- **ESC:** Volver/Salir

#### 13.4.2 Durante el Juego

- **←→↑↓:** Mover pieza seleccionada
- **Q/E:** Rotar pieza (antihorario/horario)
- **A/D:** Escalar pieza (reducir/aumentar)
- **Clic izquierdo:** Arrastrar pieza
- **Rueda del ratón:** Rotar pieza
- **ESPACIO:** Usar pista (si disponible)
- **ESC:** Menú de pausa/salida

---

## 14. ANEXOS

### 14.1 Glosario de Términos

- **AABB:** Axis-Aligned Bounding Box - Caja delimitadora alineada a ejes
- **Blit:** Block Image Transfer - Copiar una imagen a la pantalla
- **Delta Time:** Tiempo transcurrido entre frames
- **FPS:** Frames Per Second - Cuadros por segundo
- **HUD:** Heads-Up Display - Interfaz superpuesta
- **Lerp:** Linear Interpolation - Interpolación lineal
- **Pipeline:** Secuencia de operaciones de procesamiento
- **Singleton:** Patrón de diseño que permite solo una instancia
- **State Machine:** Máquina de estados finitos
- **V-Sync:** Sincronización vertical

### 14.2 Referencias Bibliográficas

1. **Pygame Documentation**

   - URL: https://www.pygame.org/docs/
   - Consultado: 2025

2. **Mathematics for Computer Graphics**

   - Autor: John Vince
   - Editorial: Springer

3. **Game Programming Patterns**

   - Autor: Robert Nystrom
   - URL: https://gameprogrammingpatterns.com/

4. **Real-Time Rendering**
   - Autores: Tomas Akenine-Möller, Eric Haines
   - Editorial: CRC Press

### 14.3 Créditos

#### 14.3.1 Desarrollo

- **Programación:** V.H & R.
- **Diseño de Niveles:** V.H & R.
- **Documentación:** V.H & R.

#### 14.3.2 Recursos

- **Framework:** Pygame Community
- **Audio:** Recursos propios
- **Fuentes:** Pygame default fonts

#### 14.3.3 Agradecimientos

- Comunidad de Pygame
- Profesores del curso de Informática Gráfica
- Testers y colaboradores

---

## 15. INFORMACIÓN DE CONTACTO Y LICENCIA

### 15.1 Información del Proyecto

- **Repositorio:** https://github.com/VictorTrab/Trabajo---Proyecto-final
- **Versión Actual:** 3.6
- **Última Actualización:** Diciembre 2025

### 15.2 Licencia

Este proyecto está desarrollado con fines educativos.

**Licencia:** Uso Educativo
**Restricciones:** No comercial
**Derechos:** © 2025 V.H & R. - Todos los derechos reservados

### 15.3 Contribuciones

El proyecto está abierto a contribuciones educativas. Para colaborar:

1. Fork del repositorio
2. Crear rama de feature
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

---

**Documento generado:** Diciembre 2025  
**Proyecto:** CUBO: Arquitecto del Caos v3.6  
**Autores:** V.H & R.  
**Propósito:** Informe Académico - Proyecto de Informática Gráfica

# CUBO: Arquitecto del Caos

## Puzzle de Transformaciones Geométricas

## 📋 Descripción

Juego de puzzle cyberpunk donde controlas un cubo que debe recolectar y colocar piezas geométricas para completar figuras objetivo mientras esquivas meteoros y usa portales.

## 🎮 Cómo Jugar

### Controles Básicos

- **Flechas (↑←↓→)**: Mover el cubo
- **E**: Recoger/Soltar pieza
- **Q**: Rotar pieza (90°)
- **Rueda del ratón**: Rotar pieza
- **Espacio**: Usar pista (cuando estés cerca del objetivo)
- **ESC**: Pausar/Salir (con confirmación)
- **ENTER**: Confirmar/Continuar

### Navegación en Menús

- **↑↓**: Navegar opciones verticales
- **←→**: Navegar opciones horizontales (selección de niveles)
- **ENTER**: Seleccionar
- **ESC**: Volver atrás

## 🎯 Objetivo del Juego

Completa la figura objetivo que aparece en la esquina superior derecha colocando las piezas correctas en las posiciones indicadas. Tienes 120 segundos y 10 intentos por nivel.

## 🌟 Características

### Niveles

- **3 niveles únicos** con dificultad progresiva
- Sistema de desbloqueo: completa un nivel para desbloquear el siguiente
- Guardado automático de progreso

### Mecánicas de Juego

#### Piezas Geométricas

- **Cuadrado**: Pieza básica cuadrada
- **Triángulo**: Pieza triangular
- **Círculo**: Pieza circular
- **Rombo**: Pieza en forma de rombo
- **Rectángulo**: Pieza rectangular

#### Sistema de Magnetismo

- Las piezas se atraen automáticamente cuando están cerca de su posición correcta
- Facilita la colocación precisa

#### Meteoros (Fase 4)

- Caen desde arriba del cielo
- Tienen advertencia visual antes de aparecer
- Al impactar, reducen tu vida
- Esquívalos para sobrevivir

#### Portales (Fase 4)

- Pares de portales conectados (entrada/salida)
- Teletransportan el cubo instantáneamente
- Útiles para escapar de meteoros

#### Power-ups (Fase 4)

- Aparecen aleatoriamente en el campo
- Efectos: escudo temporal, velocidad aumentada, etc.
- Recógelos para obtener ventajas

#### Sistema de Pistas

- **3 pistas disponibles** por nivel
- Presiona **Espacio** cerca del objetivo para ver la siguiente pieza a colocar
- Se resalta visualmente qué pieza necesitas

### Sistema Emocional (Fase 5)

El cubo reacciona emocionalmente según el estado del juego:

- **Neutral**: Estado inicial
- **Feliz**: Al colocar piezas correctamente
- **Determinado**: Cuando estás cerca de completar
- **Triste**: Al fallar
- **Miedo**: Cuando hay peligro (meteoros cerca)
- **Dolor**: Al recibir daño

### Combos y Bonificaciones

- Coloca piezas consecutivamente sin errores para crear combos
- Los combos multiplican tu puntuación
- Bonus adicional por:
  - Tiempo restante
  - Precisión (usar solo las piezas necesarias)
  - No cometer errores

## 📊 Sistema de Puntuación

### Puntos Base

- **1000 puntos** base por completar el nivel

### Bonificaciones

- **Bonus de tiempo**: Hasta 500 puntos según el tiempo restante
- **Bonus de precisión**: Hasta 300 puntos por usar solo las piezas necesarias
- **Sin errores**: 200 puntos adicionales si no fallas ningún intento
- **Combos**: Multiplicador de puntos por colocaciones consecutivas

### Penalizaciones

- **-25 puntos** por cada intento fallido de colocación

## 🎨 Estilo Visual

- **Tema Cyberpunk** con neones brillantes
- Colores: Cyan, Rosa, Púrpura, Verde Neón, Naranja
- Efectos visuales: partículas, brillo, animaciones suaves
- Fondo animado con respiración

## 🎵 Audio

Sistema de audio simple con:

- **Música de fondo**: Menú, juego, nivel completado, game over
- **Efectos de sonido**: Clicks, rotación, colocación, errores

## 🏆 Progreso del Jugador

- Se guarda automáticamente al completar niveles
- Registro de mejor tiempo por nivel
- Sistema de niveles desbloqueados
- Porcentaje de completitud total

## 💾 Guardado

El progreso se guarda automáticamente en `save_game.json`:

- Niveles completados
- Mejores puntuaciones
- Niveles desbloqueados
- Estadísticas generales

## 🚀 Ejecución del Juego

### Requisitos

- Python 3.10+
- Pygame 2.6.1
- NumPy

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/VictorTrab/Trabajo---Proyecto-final.git

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar juego
python principal.py
```

## 📁 Estructura del Proyecto

```
Trabajo - Proyecto final/
├── principal.py              # Punto de entrada
├── config/                   # Configuración
│   ├── constantes.py        # Constantes del juego
│   ├── jugador.py           # Sistema de guardado
│   └── configuracion.py     # Configuración general
├── core/                     # Lógica del juego
│   ├── estados_juego.py     # Máquina de estados
│   ├── logica_cubo_fase2.py # Piezas y magnetismo
│   ├── logica_cubo_fase3.py # Puntuación y niveles
│   ├── logica_cubo_fase4.py # Meteoros y portales
│   └── logica_cubo_fase5.py # Sistema emocional
├── entidades/               # Entidades del juego
│   ├── cubo.py             # Personaje principal
│   ├── pieza_geometrica.py # Piezas del puzzle
│   ├── meteoro.py          # Obstáculos
│   ├── portal.py           # Sistema de teletransporte
│   ├── powerup.py          # Mejoras temporales
│   └── audio_simple.py     # Sistema de audio
├── songs/                   # Archivos de audio MP3
└── docs/                    # Documentación
```

## 🎓 Consejos y Trucos

1. **Planifica antes de actuar**: Observa la figura objetivo antes de empezar
2. **Usa las pistas sabiamente**: Solo tienes 3 por nivel
3. **Prioriza la supervivencia**: Es mejor esquivar un meteoro que apresurarte a colocar
4. **Aprovecha los portales**: Úsalos estratégicamente para moverte rápido
5. **Construye combos**: Coloca piezas seguidas para multiplicar puntos
6. **Gestiona el tiempo**: 120 segundos pasan rápido, no pierdas tiempo en piezas incorrectas

## 🐛 Solución de Problemas

### El juego no inicia

- Verifica que tienes Python 3.10+
- Asegúrate de que pygame está instalado: `pip install pygame`

### No hay sonido

- Verifica que los archivos MP3 están en la carpeta `songs/`
- Comprueba el volumen del sistema

### El progreso no se guarda

- Verifica permisos de escritura en la carpeta del juego
- El archivo `save_game.json` debe ser creado automáticamente

## 📝 Créditos

Proyecto desarrollado como parte del curso de Programación.

**Versión**: 3.6 (Sistema Simplificado)
**Fecha**: Diciembre 2025

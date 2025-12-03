# CUBO: Arquitecto del Caos

![Versión](https://img.shields.io/badge/versión-3.6-blue)
![Python](https://img.shields.io/badge/python-3.10.0-green)
![Pygame](https://img.shields.io/badge/pygame-2.6.1-orange)

## 📖 Descripción

**CUBO: Arquitecto del Caos** es un videojuego de puzzle geométrico desarrollado en Python con Pygame. El jugador controla a CUBO, una entidad robótica que debe recolectar y ensamblar piezas geométricas para completar figuras objetivo mientras evita meteoros y utiliza portales.

## ✨ Características Principales

- 🎮 **3 Niveles de Dificultad** con complejidad progresiva
- 🎨 **Estética Cyberpunk** con efectos neón y partículas
- 🎵 **Sistema de Audio** completo con música y efectos de sonido
- 💾 **Persistencia de Progreso** mediante guardado automático
- ⚡ **Sistema Emocional** dinámico que afecta las animaciones
- 🌀 **Portales** para teletransportación instantánea
- ☄️ **Meteoros** como obstáculos dinámicos
- 🎁 **Power-ups** temporales (escudo, tiempo extra, slowmo)
- 📊 **Sistema de Puntuación** con bonificaciones y penalizaciones
- 👤 **Perfil de Jugador** con estadísticas detalladas

## 🎯 Cambios Recientes (v3.6)

### Optimizaciones y Limpieza de Código

- ✅ Eliminado sistema de láseres (archivo corrupto)
- ✅ Removido sistema de combo emocional
- ✅ Eliminada narrativa dinámica (mensajes contextuales)
- ✅ Sistema de estrellas reemplazado por visualización numérica de vidas
- ✅ Reducción de ~850 líneas de código en sistemas emocionales
- ✅ Archivos optimizados: `efectos_emocionales.py`, `ambiente_emocional.py`, `animaciones_emocionales.py`
- ✅ Corrección de bug: niveles desbloqueados ahora limitados a máximo (3/3)

### Sistema de Audio Simplificado

- ✅ Sistema de audio unificado en `audio_dinamico.py`
- ✅ Eliminados archivos: `audio_simple.py` y `audio_emocional.py`
- ✅ Enfoque en efectos de jugabilidad (click, rotar, explotar, colisiones)
- ✅ Sonido de click agregado en todas las selecciones de menú
- ✅ Música específica por nivel (nivel1, nivel2, nivel3)

### Documentación Consolidada

- ✅ Reducción de archivos de documentación de 6 → 3 (-50%)
- ✅ README principal unificado con información académica
- ✅ Manual de usuario completo creado
- ✅ Documentación técnica mejorada con diagramas visuales

## 🚀 Instalación

### Requisitos Previos

- Python 3.10.0 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/VictorTrab/Trabajo---Proyecto-final.git
cd "Trabajo - Proyecto final"
```

2. **Crear entorno virtual (recomendado):**

```bash
python -m venv .venv
```

3. **Activar entorno virtual:**

- Windows:
  ```bash
  .venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source .venv/bin/activate
  ```

4. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## 🎮 Ejecución

```bash
python principal.py
```

## 🎯 Controles

### Menú Principal

- **Mouse:** Navegar y seleccionar opciones
- **ESC:** Cerrar el juego

### Durante el Juego

- **Flechas / WASD:** Mover a CUBO
- **Click Izquierdo:** Arrastrar piezas
- **Espacio:** Soltar pieza en zona objetivo
- **R:** Rotar pieza seleccionada
- **H:** Usar pista (3 disponibles por nivel)
- **ESC:** Pausar/Salir

## 📁 Estructura del Proyecto

```
proyecto/
├── principal.py              # Punto de entrada
├── config/                   # Configuración
│   ├── constantes.py        # Constantes globales
│   └── jugador.py           # Sistema de jugador
├── core/                     # Lógica del juego
│   ├── estados_juego.py     # Máquina de estados
│   ├── logica_cubo_fase2.py # Sistema base
│   ├── logica_cubo_fase3.py # Sistema de puntuación
│   ├── logica_cubo_fase4.py # Meteoros y portales
│   └── logica_cubo_fase5.py # Sistema emocional
├── entidades/               # Entidades del juego
│   ├── cubo.py             # Personaje principal
│   ├── pieza_geometrica.py # Piezas del puzzle
│   ├── meteoro.py          # Obstáculos
│   ├── portal.py           # Teletransporte
│   ├── powerup.py          # Mejoras temporales
│   ├── audio_dinamico.py   # Sistema de audio unificado
│   ├── efectos_emocionales.py
│   ├── animaciones_emocionales.py
│   └── ambiente_emocional.py
├── niveles/                 # Definiciones de niveles
├── songs/                   # Audio (MP3)
└── docs/                    # Documentación
```

## 📚 Documentación Adicional

- **[Manual de Usuario](docs/MANUAL_USUARIO.md)** - Guía completa para jugadores
- **[Arquitectura Técnica](docs/ARQUITECTURA_TECNICA.md)** - Documentación técnica detallada

## 🛠️ Tecnologías Utilizadas

- **Python 3.10.0** - Lenguaje de programación
- **Pygame 2.6.1** - Framework de juegos
- **NumPy** - Operaciones matemáticas
- **JSON** - Almacenamiento de datos

## 🎓 Información Académica

### Objetivos del Proyecto

**General:** Demostrar aplicación práctica de conceptos de informática gráfica mediante un videojuego interactivo.

**Específicos:**

1. Implementar transformaciones geométricas 2D (traslación, rotación, escala)
2. Desarrollar sistema de detección de colisiones preciso
3. Crear sistema de física básica para objetos dinámicos
4. Implementar efectos visuales avanzados (partículas, animaciones, glows)
5. Diseñar interfaz de usuario intuitiva con estética cyberpunk
6. Implementar sistema de progresión y persistencia de datos

### Conceptos de Informática Gráfica Aplicados

#### Transformaciones Geométricas

- **Traslación:** `T(dx, dy) = [x + dx, y + dy]`
- **Rotación:** `R(θ) = [x*cos(θ) - y*sin(θ), x*sin(θ) + y*cos(θ)]`
- **Escala:** `S(sx, sy) = [x*sx, y*sy]`

#### Sistema de Física

- **Colisiones AABB** para piezas rectangulares
- **Colisiones Circulares** para meteoros
- **Sistema Snap** con tolerancia de 20px para alineación automática
- **Física de Meteoros** con trayectorias balísticas

#### Sistema de Partículas

- Tipos: Explosión, lluvia, chispas, estelas
- Propiedades: Color personalizable, tiempo de vida, gravedad, fade-out
- Optimización mediante pooling de partículas

#### Renderizado y Efectos Visuales

- Efectos neón y glow cyberpunk
- Animaciones procedurales (respiración, flotación, pulsos)
- Filtros de color según estados emocionales
- Teselado hexagonal en menús

### Arquitectura del Software

**Patrón de Diseño:** State Pattern (Máquina de Estados)

```
GameManager
├── MainMenuState (Menú Principal)
├── LevelSelectState (Selección de Nivel)
├── PlayingState (Jugando)
├── TransitionState (Transición entre niveles)
├── ProfileState (Perfil del Jugador)
├── AboutState (Acerca de)
└── SettingsState (Configuración)
```

### Sistema de Puntuación

**Base:** 1000 puntos

**Bonificaciones:**

- Tiempo restante: hasta +500 puntos
- Precisión (menos intentos): hasta +300 puntos
- Sin errores: +200 puntos

**Penalizaciones:**

- Intentos fallidos: -25 puntos cada uno
- Pistas usadas: -100 puntos cada una

### Logros Técnicos

✅ Implementación completa de transformaciones geométricas 2D  
✅ Sistema de física con múltiples tipos de colisiones  
✅ Sistema de partículas versátil y eficiente  
✅ Patrón State para gestión de estados del juego  
✅ Persistencia de datos mediante JSON  
✅ Sistema de audio integrado (música + efectos)  
✅ Optimización de código (~850 líneas reducidas en v3.6)

### Aprendizajes

- Arquitectura de software para videojuegos
- Optimización de rendimiento en Python
- Diseño de interfaces de usuario
- Gestión de recursos multimedia
- Control de versiones con Git/GitHub
- Matemáticas aplicadas a videojuegos

## 👥 Autores

**V.H & R.**  
Proyecto de Informática Gráfica - 2025

## 📄 Licencia

Este proyecto es de **uso educativo**. Desarrollado como proyecto académico.

---

**Versión:** 3.6  
**Año:** 2025  
**Curso:** Informática Gráfica

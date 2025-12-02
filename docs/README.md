# 🎮 CUBO: Arquitecto del Caos

**Proyecto de Informática Gráfica**  
Desarrolladores: V.H & R.  
Año: 2025

---

## 📖 Descripción del Proyecto

CUBO: Arquitecto del Caos es un juego innovador que combina mecánicas de construcción geométrica con un sistema emocional dinámico. El jugador controla a CUBO, un robot con emociones, que debe construir figuras geométricas utilizando piezas dispersas por el escenario.

---

## 🎯 Fases de Desarrollo

### ✅ Fase 1: Movimiento de CUBO

**Estado:** Completada  
**Características:**

- Movimiento fluido en 4 direcciones (WASD)
- Sistema de emociones con 5 estados
- Animaciones de respiración y expresiones faciales
- Controles responsivos con aceleración/desaceleración

### ✅ Fase 2: Construcción con Piezas

**Estado:** Completada  
**Características:**

- 5 tipos de piezas geométricas (cuadrado, triángulo, círculo, rombo, rectángulo)
- Sistema de magnetismo inteligente (radio 80px)
- Validación de construcción con tolerancia
- Partículas espectaculares (burst, glow, sparks)
- Animaciones avanzadas (pulso, rotación, flotación)
- Efectos visuales (glow, brillo, checkmarks)
- Delay de completitud para apreciar resultados

**Documentación:** Ver archivos de Fase 2

### ✅ Fase 3: Validación Avanzada ⭐ **NUEVA**

**Estado:** Completada  
**Características:**

#### 1. Sistema de Puntuación

- **Puntos base:** 1000 puntos por completar
- **Bonus tiempo:** Hasta 500 puntos (proporcional al tiempo restante)
- **Bonus precisión:** Hasta 300 puntos (usar solo piezas necesarias)
- **Bonus sin errores:** 200 puntos (sin intentos fallidos)
- **Penalizaciones:** -25 por error, -100 por pista
- **Multiplicadores:** x1.0 (Fácil), x1.5 (Medio), x2.0 (Difícil)
- **Sistema de estrellas:** 1-3 estrellas según rendimiento

#### 2. Múltiples Niveles

- **10 niveles** con complejidad creciente
- **Niveles 1-3 (Básicos):** 2-4 piezas (casa, robot, torre)
- **Niveles 4-6 (Intermedios):** 5 piezas (cohete, castillo, estrella)
- **Niveles 7-10 (Avanzados):** 6-8 piezas (figuras complejas aleatorias)
- **Distractores dinámicos:** Aumentan según nivel y dificultad

#### 3. Sistema de Pistas

- **Pista H (Siguiente Pieza):** Resalta la próxima pieza a colocar
- **Pista J (Posición Objetivo):** Muestra la zona objetivo completa
- **Límite:** 3 pistas por nivel
- **Duración:** 5 segundos con efectos visuales animados
- **Costo:** 100 puntos por pista

**Documentación:**

- `FASE3_README.md` - Documentación técnica completa
- `GUIA_RAPIDA_FASE3.md` - Guía de usuario
- `CHECKLIST_FASE3.md` - Lista de verificación

### ⏳ Fase 4: Meteoros y Portales (Planeada)

- Obstáculos dinámicos que caen
- Portales de teletransportación
- Zonas de gravedad
- Power-ups temporales

### ✅ Fase 5: Sistema Emocional Avanzado (COMPLETADA)

**Documentación completa:** [FASE5_README.md](FASE5_README.md)

- ✅ Efectos visuales por emoción (partículas, filtros, overlays)
- ✅ Sistema de audio emocional (música y SFX adaptativos)
- ✅ Animaciones contextuales (rebotes, temblores, pulsos)
- ✅ Narrativa dinámica (diálogos y mensajes contextuales)
- ✅ Sistema de combos emocionales (multiplicadores x2.5)
- ✅ Ambiente reactivo (partículas ambientales, clima, iluminación)

---

## 🎮 Controles

### Movimiento (Todas las Fases)

- `W` / `↑`: Mover arriba
- `S` / `↓`: Mover abajo
- `A` / `←`: Mover izquierda
- `D` / `→`: Mover derecha

### Piezas (Fases 2 y 3)

- `E`: Recoger pieza más cercana
- `Q`: Soltar pieza en zona de construcción

### Pistas (Fase 3) ⭐

- `H`: Pista de siguiente pieza
- `J`: Pista de posición objetivo

### Emociones (Testing)

- `1`: Emoción Feliz
- `2`: Emoción Triste
- `3`: Emoción Miedo
- `4`: Emoción Dolor
- `5`: Emoción Determinado

### Sistema

- `ESC`: Pausar / Menú
- `SPACE`: Confirmar

---

## 🚀 Instalación y Ejecución

### Requisitos

- Python 3.10 o superior
- Pygame 2.6.1 o superior

### Instalación

```bash
# 1. Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd "Trabajo - Proyecto final"

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv .venv

# 3. Activar entorno virtual
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# 4. Instalar dependencias
pip install pygame

# 5. Ejecutar el juego
python principal.py
```

---

## 🎯 Cómo Jugar

### Inicio Rápido

1. Ejecuta `python principal.py`
2. Selecciona un nivel (1-10)
3. Elige dificultad (Fácil, Medio, Difícil)
4. ¡Construye la figura objetivo!

### Objetivo del Juego

- Construir la figura objetivo mostrada en la esquina superior derecha
- Usar las piezas geométricas disponibles en el escenario
- Maximizar tu puntuación siendo rápido y preciso
- Obtener 3 estrellas en cada nivel

### Estrategias para Ganar

1. **Observa primero:** Identifica las piezas necesarias antes de mover
2. **Sé preciso:** Evita errores para obtener el bonus de 200 puntos
3. **Optimiza tiempo:** Completa rápido pero sin sacrificar precisión
4. **Usa pistas sabiamente:** Solo cuando realmente las necesites
5. **Practica:** Los niveles iniciales son perfectos para aprender

---

## 📊 Sistema de Puntuación (Fase 3)

### Fórmula

```
Puntos = (Base + BonusTiempo + BonusPrecisión + BonusSinErrores - Penalizaciones) × Multiplicador - PenasPistas
```

### Ejemplo

```
Nivel 1, Dificultad Difícil:
- Puntos base:           +1000
- Bonus tiempo:          +450   (completado en 20/60s)
- Bonus precisión:       +300   (solo piezas necesarias)
- Bonus sin errores:     +200   (0 intentos fallidos)
- Penalización intentos: -0
- Subtotal:              1950
- Multiplicador:         ×2.0   (Difícil)
- Pistas usadas:         -100   (1 pista)
─────────────────────────────
TOTAL:                   3800 puntos ⭐⭐⭐
```

### Sistema de Estrellas

- ⭐ (1 estrella): Nivel completado
- ⭐⭐ (2 estrellas): Buena puntuación (≥100% puntos base)
- ⭐⭐⭐ (3 estrellas): Excelente puntuación (≥150% puntos base)

---

## 🎨 Características Técnicas

### Gráficos

- Resolución: 1200×800 píxeles
- Estética: Cyberpunk neón
- FPS: 60 cuadros por segundo
- Efectos de partículas: Múltiples tipos (burst, glow, spark)
- Animaciones: Suaves con interpolación

### Sistemas

- **Motor:** Pygame 2.6.1
- **Física:** Magnetismo con radio de atracción
- **Validación:** Tolerancia de 30px para colocación
- **Emociones:** 5 estados con transiciones fluidas
- **Puntuación:** Sistema complejo multi-factor

### Arquitectura

- Diseño modular con separación de responsabilidades
- Herencia para extender funcionalidad entre fases
- Sistema de estados para gestión de escenas
- Código limpio y documentado

---

## 📁 Estructura del Proyecto

```
Trabajo - Proyecto final/
├── principal.py                 # Punto de entrada
├── estados_juego.py             # Gestión de estados
├── constantes.py                # Configuración global
│
├── logica_cubo.py               # Fase 1: Movimiento
├── logica_cubo_fase2.py         # Fase 2: Piezas
├── logica_cubo_fase3.py         # Fase 3: Puntuación ⭐
│
├── cubo.py                      # Clase CUBO
├── pieza_geometrica.py          # Piezas y figuras
├── sistema_particulas.py        # Efectos visuales
│
├── interfaz_usuario.py          # UI y HUD
├── sistema_menu.py              # Menús
├── jugador.py                   # Datos del jugador
│
├── FASE3_README.md              # Documentación Fase 3 ⭐
├── GUIA_RAPIDA_FASE3.md         # Guía de usuario ⭐
├── CHECKLIST_FASE3.md           # Testing ⭐
├── FASE3_COMPLETADA.md          # Resumen ejecutivo ⭐
└── fase3_resumen.py             # Resumen técnico ⭐
```

---

## 🔧 Configuración

### Cambiar Fase Activa

Editar `estados_juego.py` (línea ~92):

```python
FASE_ACTIVA = 3  # Fase 3: Puntuación y niveles

# Opciones:
# 0 = Juego original (geometría)
# 1 = Fase 1 (Movimiento CUBO)
# 2 = Fase 2 (Piezas y magnetismo)
# 3 = Fase 3 (Puntuación y niveles) ← ACTUAL
```

### Personalizar Puntuación

Editar `constantes.py`:

```python
# Puntuación
PUNTOS_BASE = 1000
BONUS_TIEMPO_MAX = 500
BONUS_PRECISION_MAX = 300
BONUS_SIN_ERRORES = 200
PENALIZACION_POR_INTENTO_FALLIDO = 25
PENALIZACION_POR_PISTA = 100

# Pistas
MAX_PISTAS_POR_NIVEL = 3
DURACION_PISTA = 5.0
```

---

## 🐛 Solución de Problemas

### El juego no inicia

- Verifica que tengas Python 3.10+
- Instala Pygame: `pip install pygame`
- Activa el entorno virtual si lo estás usando

### No veo las pistas (H, J)

- Verifica que `FASE_ACTIVA = 3` en `estados_juego.py`
- Asegúrate de tener pistas disponibles (ver panel inferior izquierdo)

### La puntuación parece incorrecta

- Revisa el desglose al final del nivel
- Verifica que estés en Fase 3
- Consulta `FASE3_README.md` para la fórmula completa

### Errores al importar módulos

- Asegúrate de estar en el directorio correcto
- Verifica que todos los archivos `.py` estén presentes
- Reinstala Pygame si es necesario

---

## 📚 Documentación Adicional

### Documentación por Fase

- **Fase 3:**
  - `FASE3_README.md` - Documentación técnica completa
  - `GUIA_RAPIDA_FASE3.md` - Guía de inicio rápido
  - `CHECKLIST_FASE3.md` - Lista de verificación y testing
  - `FASE3_COMPLETADA.md` - Resumen ejecutivo
  - `fase3_resumen.py` - Resumen técnico ejecutable

### Recursos en Línea

- Repositorio: [GitHub](URL_PENDIENTE)
- Issues: [GitHub Issues](URL_PENDIENTE)

---

## 👥 Contribuciones

Este es un proyecto educativo desarrollado como parte de un curso de Informática Gráfica.

### Desarrolladores

- **V.H** - Programación, diseño de niveles
- **R.** - Programación, arte y efectos visuales

### Tecnologías Utilizadas

- Python 3.10
- Pygame 2.6.1
- NumPy (para cálculos matemáticos en CUBO)

---

## 📄 Licencia

Uso Educativo - Proyecto de Informática Gráfica 2025

---

## 🎯 Roadmap

### ✅ Completado

- [x] Fase 1: Movimiento de CUBO
- [x] Fase 2: Sistema de piezas y magnetismo
- [x] Fase 3: Puntuación, niveles múltiples y pistas

### 🔄 En Desarrollo

- [ ] Fase 4: Meteoros y portales
- [ ] Fase 5: Sistema emocional avanzado

### 🔮 Futuro

- [ ] Guardado de progreso completo
- [ ] Tabla de clasificación global
- [ ] Logros y desbloqueos
- [ ] Modo multijugador cooperativo
- [ ] Editor de niveles personalizado
- [ ] Soporte para gamepad
- [ ] Sistema de sonido completo

---

## 🏆 Logros y Estadísticas

### Fase 3 Implementada

- **Líneas de código:** 800+ (logica_cubo_fase3.py)
- **Clases nuevas:** 3 (SistemaPuntuacion, SistemaPistas, GeneradorNiveles)
- **Niveles jugables:** 10
- **Tipos de pistas:** 2
- **Archivos de documentación:** 5
- **Tests definidos:** 39+

---

## 💡 Consejos Avanzados

### Para Obtener 3 Estrellas Consistentemente

1. Practica cada nivel en dificultad Fácil primero
2. Memoriza la posición de las piezas necesarias
3. Planea tu ruta antes de mover a CUBO
4. Evita usar pistas excepto en niveles muy difíciles
5. Apunta a completar en el primer 50% del tiempo límite

### Para Maximizar Puntuación

- Juega en dificultad Difícil (x2.0 multiplicador)
- No cometas ningún error (+200 puntos)
- Usa solo las piezas necesarias (+300 puntos)
- Completa lo más rápido posible (+hasta 500 puntos)
- No uses pistas (ahorra -300 puntos potenciales)

---

## 📞 Soporte

Para preguntas, bugs o sugerencias:

1. Consulta la documentación correspondiente
2. Revisa la sección de Solución de Problemas
3. Verifica el checklist de testing
4. Contacta a los desarrolladores

---

## ⭐ Agradecimientos

Agradecemos a:

- Profesores del curso de Informática Gráfica
- Comunidad de Pygame
- Testers y jugadores

---

**¡Disfruta construyendo con CUBO! 🎮🤖✨**

---

_Última actualización: Diciembre 2025_  
_Versión actual: 3.0.0_

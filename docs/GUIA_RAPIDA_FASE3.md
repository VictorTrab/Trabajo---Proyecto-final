# 🎮 Guía Rápida - Fase 3

## 🚀 Inicio Rápido

### 1. Ejecutar el Juego

```bash
python principal.py
```

### 2. Verificar la Fase Activa

El juego debe estar en **Fase 3**. Si no es así:

- Abre `estados_juego.py`
- Busca la línea `FASE_ACTIVA = 3`
- Asegúrate de que esté configurada en `3`

### 3. Seleccionar Nivel

- Usa las flechas ↑/↓ para navegar
- Presiona ENTER para seleccionar
- Elige dificultad (Fácil, Medio, Difícil)

---

## 🎯 Cómo Jugar

### Objetivo

Construye la figura objetivo usando las piezas geométricas disponibles.

### Controles Básicos

| Tecla | Acción                       |
| ----- | ---------------------------- |
| W/↑   | Mover CUBO arriba            |
| S/↓   | Mover CUBO abajo             |
| A/←   | Mover CUBO izquierda         |
| D/→   | Mover CUBO derecha           |
| E     | Recoger pieza más cercana    |
| Q     | Soltar pieza en construcción |

### Controles de Pistas (Nuevo en Fase 3)

| Tecla | Acción                     | Costo    |
| ----- | -------------------------- | -------- |
| H     | Mostrar siguiente pieza    | -100 pts |
| J     | Resaltar posición objetivo | -100 pts |

**Nota:** Solo tienes 3 pistas por nivel. ¡Úsalas sabiamente!

---

## 📊 Sistema de Puntuación

### Componentes de Puntuación

```
Puntos Base:            +1000
Bonus Tiempo:          +0 a +500  (más rápido = más puntos)
Bonus Precisión:       +0 a +300  (usar solo piezas necesarias)
Bonus Sin Errores:     +200       (si no cometes errores)
Penalización Errores:  -25        (por cada intento fallido)
Penalización Pistas:   -100       (por cada pista usada)
Multiplicador:         x1.0, x1.5, x2.0  (según dificultad)
```

### Sistema de Estrellas

- **⭐ (1 estrella)**: Nivel completado (>50% puntos base)
- **⭐⭐ (2 estrellas)**: Buena puntuación (>100% puntos base)
- **⭐⭐⭐ (3 estrellas)**: Excelente puntuación (>150% puntos base)

---

## 🎓 Estrategias para 3 Estrellas

### 1. Observa Primero

- Identifica las piezas necesarias ANTES de mover
- Localiza los distractores (piezas extra)
- Planea tu ruta

### 2. Sé Preciso

- Cada intento fallido cuesta 25 puntos
- Usar piezas extra reduce el bonus de precisión
- Solo usa las piezas que realmente necesitas

### 3. Optimiza el Tiempo

- Completa el nivel lo más rápido posible
- El bonus de tiempo es proporcional al tiempo restante
- Pero no sacrifiques precisión por velocidad

### 4. Evita las Pistas

- Cada pista cuesta 100 puntos
- Solo úsalas si realmente te has atascado
- Es mejor pensar un poco más que gastar una pista

### 5. Juega en Difícil

- Multiplicador x2.0 duplica tu puntuación
- Los niveles son los mismos, solo hay más distractores
- Más riesgo = más recompensa

---

## 📈 Progresión de Niveles

### Niveles 1-3 (Básicos)

- 2-4 piezas necesarias
- Figuras simples (casa, robot, torre)
- Ideal para aprender mecánicas

### Niveles 4-6 (Intermedios)

- 5 piezas necesarias
- Figuras más complejas (cohete, castillo, estrella)
- Más distractores

### Niveles 7-10 (Avanzados)

- Hasta 8 piezas necesarias
- Figuras generadas aleatoriamente
- Máximo desafío

---

## 🖥️ Interfaz de Usuario

### Panel Superior Izquierdo - Rendimiento

```
┌──────────────────────┐
│ RENDIMIENTO          │
│ Nivel: 1             │
│ Piezas: 2/2 🟢      │
│ Errores: 0 🟢       │
└──────────────────────┘
```

### Panel Inferior Izquierdo - Pistas

```
┌──────────────────────┐
│ PISTAS DISPONIBLES   │
│ 3/3 🟢              │
│ H: Siguiente pieza   │
│ J: Mostrar posición  │
└──────────────────────┘
```

### Panel Central - Resultado (al completar)

```
┌──────────────────────────┐
│ ¡NIVEL COMPLETADO!       │
│ ★★★                      │
│                          │
│ Desglose completo        │
│ de puntuación...         │
│                          │
│ PUNTUACIÓN TOTAL: 2925   │
└──────────────────────────┘
```

---

## 🔧 Personalización

### Modificar Constantes de Puntuación

Edita `constantes.py`:

```python
# Puntos base por completar un nivel
PUNTOS_BASE = 1000

# Bonus máximo por velocidad
BONUS_TIEMPO_MAX = 500

# Bonus máximo por precisión
BONUS_PRECISION_MAX = 300

# Bonus por no cometer errores
BONUS_SIN_ERRORES = 200

# Penalización por intento fallido
PENALIZACION_POR_INTENTO_FALLIDO = 25

# Penalización por usar pista
PENALIZACION_POR_PISTA = 100
```

### Modificar Sistema de Pistas

Edita `constantes.py`:

```python
# Número máximo de pistas por nivel
MAX_PISTAS_POR_NIVEL = 3

# Segundos que dura visible una pista
DURACION_PISTA = 5.0
```

---

## 🐛 Solución de Problemas

### No veo el panel de pistas

**Solución:** Verifica que estás ejecutando Fase 3. Revisa `estados_juego.py` línea 92.

### Las pistas no funcionan

**Solución:**

- Verifica que tengas pistas disponibles (mira el panel)
- Asegúrate de que aún queden piezas por colocar
- Las pistas solo funcionan durante el juego, no después de completar

### Mi puntuación es muy baja

**Solución:**

- Revisa el desglose al final del nivel
- Identifica qué te está restando puntos
- Lee las estrategias en esta guía
- Intenta de nuevo con un mejor plan

### El nivel no termina después de colocar todas las piezas

**Solución:**

- Verifica que las piezas estén CORRECTAMENTE colocadas
- Debe haber un círculo de verificación ✓ en cada pieza colocada
- Revisa el porcentaje de completitud en la interfaz

---

## 📊 Ejemplo de Puntuación Perfecta

**Escenario:** Nivel 1, Dificultad Difícil

```
Datos:
- Tiempo límite: 60 segundos
- Tiempo usado: 20 segundos
- Piezas necesarias: 2
- Piezas usadas: 2
- Intentos fallidos: 0
- Pistas usadas: 0

Cálculo:
Puntos base:              +1000
Bonus tiempo:             +333  (40s restantes de 60s = 67%)
Bonus precisión:          +300  (100% precisión)
Bonus sin errores:        +200
Penalización intentos:    -0
Penalización pistas:      -0
Subtotal:                 1833
Multiplicador (x2.0):     x2.0
──────────────────────────────
TOTAL:                    3666 puntos ⭐⭐⭐
```

---

## 🎯 Metas y Desafíos

### Desafío 1: Perfeccionista

- Completa cualquier nivel con 3 estrellas
- No uses pistas
- No cometas errores

### Desafío 2: Velocista

- Completa el nivel 1 en menos de 15 segundos
- Mantén 2 estrellas o más

### Desafío 3: Maestro del Caos

- Completa todos los niveles (1-10) con 3 estrellas
- En dificultad Difícil
- Promedio de menos de 1 pista por nivel

### Desafío 4: Sin Ayuda

- Completa el nivel 10 sin usar ninguna pista
- En dificultad Media o superior

---

## 📚 Documentación Adicional

- **FASE3_README.md**: Documentación técnica completa
- **fase3_resumen.py**: Resumen de implementación
- **logica_cubo_fase3.py**: Código fuente comentado

---

## 🎨 Próximas Funcionalidades

### Fase 4 (Planeada)

- Meteoros que caen como obstáculos
- Portales de teletransportación
- Zonas de gravedad que afectan las piezas

### Fase 5 (Planeada)

- Sistema emocional completo con efectos visuales
- Sonidos reactivos a emociones
- Narrativa dinámica

---

## 🏆 Créditos

**CUBO: Arquitecto del Caos - Fase 3**

- Desarrolladores: V.H & R.
- Proyecto de Informática Gráfica
- Año: 2025

---

**¡Diviértete construyendo y maximizando tu puntuación! 🚀**

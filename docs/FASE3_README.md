# CUBO: Arquitecto del Caos - Fase 3

## 🎮 Nuevas Funcionalidades

### Sistema de Puntuación

La Fase 3 introduce un **sistema completo de puntuación** que evalúa tu rendimiento basándose en múltiples factores:

#### Componentes de la Puntuación

1. **Puntos Base**: 1000 puntos por completar el nivel

2. **Bonus por Tiempo** (hasta 500 puntos)

   - Más rápido = más puntos
   - Se calcula según el tiempo restante del límite

3. **Bonus por Precisión** (hasta 300 puntos)

   - Usar solo las piezas necesarias = bonus completo
   - Cada pieza extra reduce el bonus en 20%

4. **Bonus Sin Errores** (200 puntos)

   - Solo se otorga si no cometes ningún intento fallido

5. **Penalizaciones**

   - -25 puntos por cada intento fallido de colocar una pieza
   - -100 puntos por cada pista utilizada

6. **Multiplicador de Dificultad**
   - Fácil: x1.0
   - Medio: x1.5
   - Difícil: x2.0

#### Sistema de Estrellas

Tu puntuación se convierte en una calificación de estrellas:

- ⭐ (1 estrella): Nivel completado
- ⭐⭐ (2 estrellas): Buena puntuación (100% de puntos base)
- ⭐⭐⭐ (3 estrellas): Excelente puntuación (150% de puntos base)

---

### Múltiples Niveles

La Fase 3 incluye **10 niveles predefinidos** con dificultad progresiva:

#### Niveles Básicos (1-3)

- **Nivel 1**: Casa simple (2 piezas)
- **Nivel 2**: Robot básico (4 piezas)
- **Nivel 3**: Torre (4 piezas)

#### Niveles Intermedios (4-6)

- **Nivel 4**: Cohete (5 piezas)
- **Nivel 5**: Castillo (5 piezas)
- **Nivel 6**: Estrella compuesta (5 piezas)

#### Niveles Avanzados (7-10)

- Figuras aleatorias complejas generadas dinámicamente
- Hasta 8 piezas por nivel
- Más piezas distractor según el nivel

#### Piezas Distractor

Cada nivel incluye piezas adicionales que NO son necesarias para completar la construcción:

- **Fácil**: 2 piezas extra + nivel/3
- **Medio**: 3 piezas extra + nivel/3
- **Difícil**: 5 piezas extra + nivel/3

---

### Sistema de Pistas

¿Atascado? Usa las **pistas** para obtener ayuda:

#### Pistas Disponibles (3 por nivel)

1. **Pista de Siguiente Pieza** (Tecla `H`)

   - Resalta la siguiente pieza que debes colocar
   - Muestra un círculo amarillo pulsante alrededor de la pieza
   - Indica con una flecha cuál pieza recoger

2. **Pista de Posición** (Tecla `J`)
   - Resalta la zona objetivo completa
   - Muestra un contorno verde brillante pulsante
   - Te ayuda a visualizar dónde deben ir las piezas

#### Costo de las Pistas

- Cada pista cuesta **100 puntos**
- Tienes un máximo de **3 pistas por nivel**
- Las pistas duran **5 segundos** en pantalla
- Usa las pistas estratégicamente para maximizar tu puntuación

---

## 🎯 Controles

### Controles Básicos (heredados de Fase 2)

- `W/↑`: Mover CUBO arriba
- `S/↓`: Mover CUBO abajo
- `A/←`: Mover CUBO izquierda
- `D/→`: Mover CUBO derecha
- `E`: Recoger pieza más cercana
- `Q`: Soltar pieza en zona de construcción

### Controles Nuevos (Fase 3)

- `H`: Usar pista de "Siguiente Pieza"
- `J`: Usar pista de "Posición Objetivo"

### Controles de Emociones (Testing)

- `1`: Emoción Feliz
- `2`: Emoción Triste
- `3`: Emoción Miedo
- `4`: Emoción Dolor
- `5`: Emoción Determinado

---

## 📊 Interfaz de Usuario

### Panel de Pistas (Esquina Inferior Izquierda)

- Muestra pistas disponibles (X/3)
- Instrucciones de teclas H y J
- Color verde cuando hay pistas disponibles
- Color gris cuando se agotaron

### Panel de Rendimiento (Esquina Superior Izquierda)

- **Nivel**: Número del nivel actual
- **Piezas**: Usadas vs Necesarias (verde si óptimo, naranja si hay extras)
- **Errores**: Número de intentos fallidos (verde si 0, naranja si >0)

### Panel de Puntuación Final (Al completar el nivel)

Muestra durante el retraso de 2 segundos:

- Título "¡NIVEL COMPLETADO!"
- Estrellas obtenidas (★★★)
- Desglose completo:
  - Puntos base
  - Bonus tiempo
  - Bonus precisión
  - Bonus sin errores
  - Penalizaciones
  - Pistas usadas (si aplica)
  - Multiplicador de dificultad
- **Puntuación Total** (grande y destacada)

---

## 🔧 Configuración Técnica

### Cambiar de Fase

En el archivo `estados_juego.py`, línea ~92:

```python
FASE_ACTIVA = 3  # Fase 3: Puntuación, niveles y pistas
```

Opciones:

- `0`: Juego original (geometría)
- `1`: Fase 1 (Movimiento CUBO)
- `2`: Fase 2 (Piezas y magnetismo)
- `3`: Fase 3 (Puntuación y niveles) ← **NUEVA**

### Personalizar Constantes

En `constantes.py`, puedes ajustar:

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

# Niveles
MAX_NIVELES_FASE3 = 10
```

---

## 🎓 Estrategias para Obtener 3 Estrellas

1. **Planifica Antes de Actuar**

   - Observa todas las piezas disponibles
   - Identifica las piezas necesarias antes de mover

2. **Minimiza los Errores**

   - El bonus de 200 puntos sin errores es valioso
   - Piensa bien antes de soltar una pieza

3. **Sé Eficiente**

   - Usa solo las piezas necesarias
   - Cada pieza extra reduce tu bonus de precisión

4. **Optimiza el Tiempo**

   - Completa el nivel rápido para maximizar el bonus de tiempo
   - Pero no sacrifiques precisión por velocidad

5. **Usa las Pistas con Sabiduría**
   - Cada pista cuesta 100 puntos
   - Úsalas solo cuando realmente las necesites
   - Mejor perder 100 puntos que cometer múltiples errores

---

## 🏆 Métricas de Rendimiento

Al completar un nivel, recibirás:

```json
{
  "nivel": 1,
  "completado": true,
  "puntuacion": 2450,
  "estrellas": 3,
  "tiempo_usado": 35.2,
  "intentos_fallidos": 0,
  "pistas_usadas": 1
}
```

Estas métricas se pueden usar para:

- Guardar progreso del jugador
- Generar tablas de clasificación
- Desbloquear niveles adicionales
- Mostrar estadísticas personales

---

## 📈 Próximas Fases

- **Fase 4**: Meteoros y portales (obstáculos dinámicos)
- **Fase 5**: Sistema emocional completo con efectos visuales

---

## 🐛 Solución de Problemas

### "No puedo usar pistas"

- Verifica que tengas pistas disponibles (mira el panel inferior izquierdo)
- Cada nivel solo tiene 3 pistas máximo

### "Las piezas no resaltan cuando uso H"

- Asegúrate de que aún queden piezas por colocar
- La pista solo funciona si hay piezas necesarias sin colocar

### "Mi puntuación es baja"

- Revisa el desglose de puntuación al final
- Identifica qué factores te están restando puntos
- Intenta completar el nivel de nuevo con una mejor estrategia

---

## 📝 Notas del Desarrollador

La Fase 3 hereda toda la funcionalidad de la Fase 2:

- Sistema de magnetismo (80px de radio)
- Partículas espectaculares al colocar piezas
- Animaciones de pulso, rotación y flotación
- Efectos de glow para piezas
- Validación de construcción con tolerancia de 30px
- Retraso de 2 segundos al completar para apreciar el resultado

Todo esto se mantiene mientras se añaden los nuevos sistemas de puntuación, niveles y pistas.

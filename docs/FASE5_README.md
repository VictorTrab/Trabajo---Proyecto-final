# 🎭 Fase 5: Sistema Emocional Avanzado

## 📋 Descripción General

La **Fase 5** implementa un sistema emocional avanzado que enriquece la experiencia de juego con efectos visuales dinámicos, audio reactivo, animaciones contextuales, narrativa dinámica, sistema de combos emocionales y ambiente reactivo.

---

## ✨ Características Principales

### 1. 🎨 Efectos Visuales Emocionales

El sistema de efectos visuales responde a la emoción actual de CUBO con:

#### **Partículas Emocionales**

- **Feliz** 💛: Explosiones de partículas amarillas brillantes
- **Triste** 💙: Gotas de lluvia azules cayendo
- **Miedo** 💜: Chispas púrpuras erráticas
- **Dolor** ❤️: Ondas pulsantes rojas
- **Determinado** 🧡: Estelas naranjas neón brillantes

#### **Filtros de Pantalla**

- **Feliz**: Overlay amarillo cálido (15% intensidad)
- **Triste**: Overlay azul oscuro (20% intensidad)
- **Miedo**: Temblor de pantalla (intensidad 4px)
- **Dolor**: Pulso rojo palpitante (25% intensidad)
- **Determinado**: Brillo naranja energético (15% intensidad)

#### **Eventos Especiales**

- **Éxito**: Triple explosión de felicidad
- **Daño**: Pulso de dolor inmediato
- **PowerUp**: Doble explosión amarilla

---

### 2. 🎵 Sistema de Audio Emocional

Sistema completo de música y efectos de sonido que se adaptan al contexto:

#### **Música Emocional**

Pistas diferentes según la emoción actual con transiciones suaves (fade in/out de 1.5s):

- `musica_feliz.mp3`
- `musica_triste.mp3`
- `musica_miedo.mp3`
- `musica_dolor.mp3`
- `musica_determinado.mp3`
- `musica_menu.mp3`

#### **Efectos de Sonido**

- **Eventos de nivel**: `sfx_exito.wav`, `sfx_fracaso.wav`
- **PowerUps**: `sfx_powerup.wav`
- **Daño**: `sfx_dano.wav`
- **UI**: `sfx_click.wav`, `sfx_hover.wav`
- **Gameplay**: `sfx_pieza_colocar.wav`, `sfx_pista.wav`
- **Fase 4**: `sfx_meteoro.wav`, `sfx_portal.wav`
- **Combos**: `sfx_combo.wav`

#### **Configuración**

```python
# Volúmenes ajustables
volumen_musica: 0.0 - 1.0 (default: 0.5)
volumen_efectos: 0.0 - 1.0 (default: 0.7)

# Habilitar/deshabilitar
habilitar_audio = True/False
```

**Nota**: Si los archivos de audio no existen, el sistema funciona sin errores (modo silencioso).

---

### 3. 🎬 Animaciones Contextuales

#### **Animaciones por Emoción (Continuas)**

- **Feliz**: Rebote flotante (amplitud 15px, frecuencia 10Hz)
- **Triste**: Caída lenta con gravedad simulada
- **Miedo**: Temblor errático (intensidad 8px, frecuencia 25Hz)
- **Dolor**: Sacudida violenta (intensidad 12px, frecuencia 20Hz)
- **Determinado**: Pulso de escala (escala máxima 1.15x, frecuencia 8Hz)

#### **Animaciones de Eventos**

- **Celebración (Éxito)**: Rotación 360° + saltos parabólicos (duración 1.5s)
- **Abatimiento (Fracaso)**: Caída lenta con fade (duración 1.2s)

#### **Animaciones Continuas Sutiles**

- Respiración normal (escala ±5%)
- Flotación feliz (±5px vertical)
- Oscilación tristeza (±3px)
- Vibración miedo (±2px errático)
- Latido dolor (pulso 8%)
- Energía determinación (pulso 10%)

---

### 4. 💬 Sistema de Narrativa Dinámica

Diálogos contextuales que aparecen según emoción y eventos del juego:

#### **Frases por Emoción**

Cada emoción tiene frases para diferentes contextos (inicio, progreso, eventos):

**Feliz**:

- "¡Qué bien me siento hoy!"
- "¡Excelente! Voy bien"
- "Me siento imparable"

**Determinado**:

- "¡Esta vez lo lograré!"
- "¡No me rendiré!"
- "¡Puedo hacerlo!"

**Triste**:

- "Esto se ve difícil..."
- "Sigo intentándolo"
- "No me rendiré"

**Miedo**:

- "¡Cuidado con eso!"
- "¡Por poco!"
- "Eso estuvo cerca"

**Dolor**:

- "¡Auch! Eso dolió"
- "Aguanta un poco más"
- "Puedo superarlo"

#### **Mensajes de Eventos**

- Nivel completado
- Nivel fallido
- PowerUp obtenido
- Combo alcanzado
- Pista usada
- Meteoro esquivado
- Portal usado

#### **Frases Motivacionales**

- "Tú puedes con esto"
- "Confía en ti mismo"
- "Cada intento cuenta"
- "El esfuerzo vale la pena"

#### **Tutoriales Contextuales**

- Movimiento
- Sistema de piezas
- Gestión emocional

---

### 5. 🔥 Sistema de Combos Emocionales

Recompensa por mantener emociones positivas (feliz, determinado):

#### **Niveles de Combo**

| Nivel   | Tiempo Requerido | Multiplicador | Bonus |
| ------- | ---------------- | ------------- | ----- |
| 1       | 3 segundos       | x1.2          | +10   |
| 2       | 8 segundos       | x1.5          | +25   |
| 3       | 15 segundos      | x2.0          | +50   |
| 4 (MAX) | 25 segundos      | x2.5          | +100  |

#### **Mecánicas**

- **Emociones positivas** (feliz, determinado): Aumentan combo
- **Emociones neutras**: Mantienen combo pero decrece lentamente (-50%/s)
- **Emociones negativas** (triste, miedo, dolor): Rompen el combo

#### **Bonus**

- Puntos extra al subir de nivel
- Multiplicador aplicado a todas las acciones
- Estadísticas de combo máximo alcanzado

#### **Visualización**

- Indicador de multiplicador con escala animada
- Barra de progreso hacia siguiente nivel
- Colores por nivel:
  - Nivel 1: Amarillo neón
  - Nivel 2: Verde neón
  - Nivel 3: Naranja neón
  - Nivel 4: Magenta brillante

---

### 6. 🌍 Ambiente Emocional Reactivo

El entorno del juego responde a las emociones:

#### **Partículas Ambientales** (máx 30)

- **Feliz**: Burbujas doradas flotantes ascendentes
- **Triste**: Lluvia continua de gotas azules
- **Miedo**: Chispas púrpuras erráticas
- **Dolor**: Centellas rojas dispersas
- **Determinado**: Destellos naranjas ascendentes

#### **Iluminación Emocional**

- **Brillo base**: Varía según emoción (0.7 a 1.15x)
- **Saturación**: Ajustada por emoción
- **Tinte de color**: Overlay emocional
- **Efectos especiales**:
  - Miedo: Parpadeo (flicker)
  - Dolor: Pulso rítmico

#### **Distorsión de Fondo**

- **Miedo**: Ondulación sutil (±2px)
- **Dolor**: Vibración rápida (±1.5px)

#### **Clima Emocional**

- **Triste**: Lluvia densa adicional
- **Miedo**: Sombras danzantes oscuras

#### **Fondo Dinámico con Gradientes**

Gradientes verticales personalizados por emoción:

- **Feliz**: Amarillo cálido → Naranja
- **Triste**: Azul oscuro → Azul profundo
- **Miedo**: Púrpura oscuro → Púrpura profundo
- **Dolor**: Rojo oscuro → Rojo profundo
- **Determinado**: Naranja oscuro → Marrón cálido
- **Neutral**: Gris azulado → Gris oscuro

---

## 🎮 Integración en GameCuboFase5

### **Inicialización**

```python
game = GameCuboFase5(
    screen=pantalla,
    level_number=1,
    difficulty="Medio",
    player=jugador,
    config={"habilitar_audio": True}
)
```

### **Sistemas Integrados**

1. **EfectosEmocionales**: Partículas y filtros visuales
2. **AudioEmocional**: Música y efectos de sonido
3. **AnimadorEmocional**: Animaciones de eventos
4. **AnimacionContinua**: Animaciones sutiles permanentes
5. **NarrativaDinamica**: Diálogos contextuales
6. **ComboEmocional**: Sistema de multiplicadores
7. **AmbienteEmocional**: Partículas y clima ambiental
8. **FondoDinamico**: Gradientes emocionales

### **Métodos Principales**

- `update(dt)`: Actualiza todos los sistemas
- `draw()`: Renderiza con efectos emocionales
- `pausar()`: Pausa música
- `reanudar()`: Reanuda música
- `reiniciar_nivel()`: Limpia sistemas emocionales
- `limpiar()`: Libera recursos de audio

---

## 🎯 Estrategias de Juego

### **Maximizar Combos**

1. Mantén a CUBO feliz o determinado
2. Evita daño para no romper el combo
3. Usa power-ups de escudo para proteger combos
4. Alcanza nivel 4 (x2.5) para máxima puntuación

### **Gestión Emocional**

1. **Feliz**: Ideal para exploración y progreso constante
2. **Determinado**: Mejor para desafíos difíciles
3. **Evita tristeza/miedo**: Reducen efectividad y rompen combos
4. **Dolor temporal**: Recupera rápido con determinación

### **Aprovecha la Narrativa**

- Lee los diálogos para pistas contextuales
- Las frases motivacionales aparecen en momentos clave
- Los tutoriales se activan automáticamente cuando es relevante

---

## 📊 Estadísticas Rastreadas

La Fase 5 rastrea:

- **Combo máximo alcanzado**
- **Total de bonus obtenido de combos**
- **Emoción actual**
- **Estado de audio** (habilitado/deshabilitado)

Accede con:

```python
stats = game.obtener_estadisticas_fase5()
# {
#     "combo_maximo": 4,
#     "bonus_total_combos": 185,
#     "audio_habilitado": True,
#     "emocion_actual": "determinado"
# }
```

---

## 🔧 Configuración Técnica

### **Requisitos**

- Python 3.10+
- Pygame 2.6.1+
- Archivos de audio (opcionales) en `assets/audio/`

### **Estructura de Archivos**

```
entidades/
├── efectos_emocionales.py    # Partículas y filtros visuales
├── audio_emocional.py          # Sistema de audio
├── animaciones_emocionales.py  # Animaciones contextuales
├── narrativa_dinamica.py       # Diálogos y mensajes
├── combo_emocional.py          # Sistema de combos
└── ambiente_emocional.py       # Ambiente reactivo

core/
└── logica_cubo_fase5.py        # Lógica principal Fase 5

assets/audio/ (opcional)
├── musica_*.mp3
└── sfx_*.wav
```

### **Rendimiento**

- Máximo 30 partículas ambientales simultáneas
- Sistema de caché para efectos de sonido
- Gradientes optimizados por línea
- Transparencias con SRCALPHA

---

## 🎨 Paleta de Colores Emocionales

| Emoción     | Color Principal | RGB           |
| ----------- | --------------- | ------------- |
| Feliz       | Amarillo Neón   | (255, 255, 0) |
| Triste      | Azul Neón       | (0, 255, 255) |
| Miedo       | Púrpura         | (128, 0, 128) |
| Dolor       | Rojo            | (255, 0, 0)   |
| Determinado | Naranja Neón    | (255, 165, 0) |

---

## 🐛 Notas de Compatibilidad

### **Audio Opcional**

Si los archivos de audio no existen:

- El sistema continúa funcionando
- No se muestran errores al usuario
- Solo aparecen logs en consola (opcional)

### **Herencia de Fases**

Fase 5 hereda todas las características de:

- **Fase 1**: Movimiento y emociones básicas
- **Fase 2**: Sistema de piezas y magnetismo
- **Fase 3**: Pistas y puntuación (3 niveles)
- **Fase 4**: Meteoros, portales y power-ups

---

## 🚀 Próximos Pasos

Posibles mejoras futuras:

- **Reconocimiento de voz** para cambiar emociones
- **Modo historia** con narrativa extendida
- **Efectos de partículas 3D** con shaders
- **Sistema de logros emocionales**
- **Multiplayer con emociones compartidas**

---

## 📝 Licencia y Créditos

**Fase 5** creada como parte del proyecto **CUBO: Arquitecto del Caos**.

Sistema emocional diseñado para enriquecer la experiencia jugable mediante feedback visual, auditivo y narrativo dinámico.

---

¡Disfruta explorando el mundo emocional de CUBO! 🎭✨

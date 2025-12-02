# 🎮 CUBO: Arquitecto del Caos - Fase 4

## 🌟 Meteoros y Portales

**Versión:** 4.0  
**Estado:** Completada ✅  
**Fecha:** Diciembre 2025

---

## 📖 Descripción General

La Fase 4 introduce **elementos dinámicos y desafiantes** al juego, transformando la experiencia de construcción en una aventura llena de acción. Ahora debes esquivar meteoros, usar portales estratégicamente y recolectar power-ups mientras construyes las figuras objetivo.

---

## 🆕 Nuevas Mecánicas

### 1. ☄️ Sistema de Meteoros

Los meteoros caen periódicamente desde el cielo, creando obstáculos dinámicos.

#### Características:

- **Advertencia visual:** 1 segundo antes del impacto
- **Línea de advertencia amarilla:** Indica dónde caerá el meteoro
- **Efectos de impacto:** Explosiones espectaculares al colisionar
- **Estela de fuego:** Rastro visual mientras cae

#### Comportamiento:

- **Impacto en CUBO:**

  - Sin escudo: CUBO recibe daño y suelta las piezas que lleva
  - Con escudo: Protección total, sin daño
  - Emoción de dolor (sin escudo) o determinación (con escudo)

- **Impacto en piezas:**
  - Las piezas no colocadas son empujadas
  - Las piezas colocadas no se ven afectadas

#### Frecuencia por Dificultad:

- **Fácil:** 8-12 segundos entre meteoros
- **Medio:** 5-8 segundos entre meteoros
- **Difícil:** 3-6 segundos entre meteoros

#### Velocidad:

- **Fácil:** 150-200 px/s
- **Medio:** 200-300 px/s
- **Difícil:** 250-400 px/s

---

### 2. 🌀 Sistema de Portales

Portales de teletransportación que conectan dos puntos del mapa.

#### Características:

- **Pares vinculados:** Cada portal tiene su pareja
- **Colores distintivos:** Hasta 5 colores diferentes
- **Efectos visuales:** Vórtices giratorios y anillos pulsantes
- **Líneas de conexión:** Líneas punteadas entre portales pareados
- **Cooldown:** 1 segundo para evitar loops infinitos

#### Tipos de Portal:

- **Entrada (↑):** Portal de origen
- **Salida (↓):** Portal de destino
- _Nota:_ Ambos son bidireccionales

#### Objetos que se Teletransportan:

- ✅ CUBO
- ✅ Piezas no colocadas
- ❌ Piezas ya colocadas en la figura

#### Uso Estratégico:

- Escapar rápidamente de meteoros
- Llegar a piezas distantes
- Evitar obstáculos
- Acceso rápido a la zona de construcción

---

### 3. ⚡ Power-Ups

Potenciadores temporales que mejoran las habilidades de CUBO.

#### Tipos de Power-Ups:

##### 🛡️ Escudo (Cian)

- **Duración:** 8 segundos
- **Efecto:** Inmunidad total a meteoros
- **Visual:** Anillo protector alrededor de CUBO
- **Bonus:** +150 puntos si completas sin recibir daño

##### ⚡ Velocidad (Amarillo)

- **Duración:** 6 segundos
- **Efecto:** Velocidad de movimiento x1.5
- **Visual:** Rastro amarillo al moverse
- **Uso:** Recolectar piezas rápidamente

##### 🧲 Magnetismo (Púrpura)

- **Duración:** 10 segundos
- **Efecto:** Radio de atracción x1.5 (de 80 a 120 px)
- **Visual:** Partículas púrpura alrededor del área
- **Uso:** Atraer piezas desde mayor distancia

#### Mecánica:

- **Aparición:** Cada 15-25 segundos (aleatorio)
- **Tiempo de vida:** 15 segundos antes de desaparecer
- **Advertencia:** Parpadeo en los últimos 3 segundos
- **Acumulación:** Los efectos pueden superponerse
- **Indicadores:** Panel en la parte superior derecha muestra power-ups activos

---

## 🎯 Estrategias de Juego

### Esquivar Meteoros

1. **Observa las advertencias:** Líneas amarillas indican dónde caerán
2. **Mantén el movimiento:** No te quedes estático
3. **Usa portales:** Teletransportación instantánea para escapar
4. **Recoge escudos:** Prioriza el power-up de escudo en dificultad alta

### Usar Portales Eficientemente

1. **Memoriza los pares:** Aprende qué portales están conectados por color
2. **Planifica rutas:** Usa portales para acortar distancias
3. **Escape rápido:** Entra a un portal si un meteoro viene hacia ti
4. **Cooldown:** Espera 1 segundo antes de re-usar el mismo portal

### Maximizar Power-Ups

1. **Prioridad:** Escudo > Magnetismo > Velocidad
2. **Timing:** Recoge velocidad cuando necesites recolectar muchas piezas
3. **Combos:** Magnetismo + Velocidad = recolección ultra-rápida
4. **Conserva el escudo:** Úsalo durante ráfagas de meteoros

### Puntuación Óptima

- **Esquiva perfecta:** +150 puntos (sin recibir daño)
- **Usa portales con sabiduría:** No afectan la puntuación
- **Minimiza power-ups:** Solo usa los necesarios
- **Velocidad:** Completa rápido para bonus de tiempo

---

## 📊 Sistema de Puntuación Actualizado

### Puntos Base (Fase 3)

```
Puntos = (Base + BonusTiempo + BonusPrecisión + BonusSinErrores - Penalizaciones) × Multiplicador - PenasPistas
```

### Bonificaciones de Fase 4

- **+150 puntos:** Esquiva perfecta (sin recibir daño de meteoros)
- **Sin penalización:** Uso de portales (estrategia válida)
- **Sin penalización:** Recolectar power-ups (ayuda legítima)

### Estadísticas Adicionales

- Meteoros esquivados
- Daño recibido
- Portales usados
- Power-ups recogidos

---

## 🎮 Controles

_Todos los controles de Fase 3 se mantienen._

### Movimiento

- `W` / `↑`: Mover arriba
- `S` / `↓`: Mover abajo
- `A` / `←`: Mover izquierda
- `D` / `→`: Mover derecha

### Piezas

- `E`: Recoger pieza
- `Q`: Soltar pieza

### Pistas

- `H`: Pista de siguiente pieza
- `J`: Pista de posición objetivo

### Sistema

- `ESC`: Pausar / Menú
- `SPACE`: Confirmar

---

## 🛠️ Implementación Técnica

### Arquitectura

```
entidades/
├── meteoro.py          # Sistema de meteoros
│   ├── Meteoro         # Clase individual
│   └── GeneradorMeteoros
├── portal.py           # Sistema de portales
│   ├── Portal          # Portal individual
│   └── SistemaPortales
└── powerup.py          # Sistema de power-ups
    ├── PowerUp         # Power-up individual
    └── SistemaPowerUps

core/
└── logica_cubo_fase4.py
    └── GameCuboFase4   # Hereda de Fase3
```

### Herencia

```
GameCuboFase2 (Base)
    ↓
GameCuboFase3 (Pistas + Puntuación)
    ↓
GameCuboFase4 (Meteoros + Portales + Power-Ups)
```

---

## 🐛 Características de Seguridad

### Anti-Loops

- **Cooldown de portales:** 1 segundo entre teletransportaciones
- **Tracking por objeto:** Evita loops infinitos

### Colisiones Optimizadas

- **Verificación eficiente:** Solo objetos activos
- **Áreas de impacto precisas:** Radio configurable
- **Validación de estado:** Meteoros en advertencia no dañan

### Balance Automático

- **Frecuencia adaptativa:** Según dificultad
- **Spawn aleatorio:** Evita patrones predecibles
- **Límite de entidades:** Gestión de memoria

---

## 📈 Estadísticas y Logros

### Métricas Rastreadas

- ✅ Meteoros esquivados totales
- ✅ Daño total recibido
- ✅ Portales utilizados
- ✅ Power-ups recogidos
- ✅ Esquivas perfectas (0 daño)

### Desafíos Sugeridos

- 🏆 **Ninja:** Completa 3 niveles sin recibir daño
- 🏆 **Portal Master:** Usa portales 50 veces
- 🏆 **Coleccionista:** Recoge 20 power-ups
- 🏆 **Invencible:** 10 esquivas perfectas

---

## 🔮 Próximas Mejoras

### Fase 5 (Planeada)

- Sistema emocional avanzado con efectos visuales
- Sonido emocional dinámico
- Narrativa contextual
- Animaciones de celebración mejoradas

### Mejoras Potenciales

- [ ] Más tipos de power-ups (tiempo extra, pista gratis)
- [ ] Meteoros que siguen a CUBO
- [ ] Portales unidireccionales
- [ ] Zonas de gravedad modificada
- [ ] Tabla de clasificación global

---

## 👥 Créditos

**Desarrolladores:** V.H & R.  
**Motor Gráfico:** Pygame 2.6.1  
**Lenguaje:** Python 3.10.0  
**Año:** 2025

---

## 📝 Changelog

### v4.0.0 - Fase 4 Completa

- ✅ Sistema de meteoros con advertencias visuales
- ✅ Portales de teletransportación bidireccionales
- ✅ 3 tipos de power-ups (Escudo, Velocidad, Magnetismo)
- ✅ Integración completa con Fase 3
- ✅ Balance de dificultad por nivel
- ✅ Efectos visuales espectaculares
- ✅ Sistema de puntuación ampliado

---

**¡Diviértete construyendo bajo la lluvia de meteoros! 🌠**

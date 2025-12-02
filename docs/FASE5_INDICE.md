# 📁 Índice de Archivos - Fase 5

## Estructura Completa de Archivos Fase 5

### 🆕 Archivos Nuevos Creados

#### **Entidades (entidades/)**

```
entidades/
├── efectos_emocionales.py          [370 líneas] - Partículas y filtros visuales
├── audio_emocional.py               [260 líneas] - Sistema de audio emocional
├── animaciones_emocionales.py       [280 líneas] - Animaciones contextuales
├── narrativa_dinamica.py            [330 líneas] - Diálogos y mensajes dinámicos
├── combo_emocional.py               [280 líneas] - Sistema de combos emocionales
└── ambiente_emocional.py            [260 líneas] - Ambiente reactivo
```

**Total nuevas entidades**: 6 archivos, ~1,780 líneas

#### **Core (core/)**

```
core/
└── logica_cubo_fase5.py             [300 líneas] - Lógica principal Fase 5
```

**Total core**: 1 archivo, ~300 líneas

#### **Documentación (docs/)**

```
docs/
├── FASE5_README.md                  [480 líneas] - Documentación completa
└── FASE5_RESUMEN.md                 [220 líneas] - Resumen de implementación
```

**Total documentación**: 2 archivos, ~700 líneas

---

### 📝 Archivos Modificados

#### **Core**

- `core/estados_juego.py` - Integración de Fase 5

#### **Configuración**

- `config/constantes.py` - Colores y constantes adicionales

#### **Documentación**

- `docs/README.md` - Actualización de estado de fases

---

### 📊 Resumen Estadístico

**Archivos Creados**: 8  
**Archivos Modificados**: 3  
**Total Líneas Nuevas**: ~2,500  
**Clases Nuevas**: 15  
**Métodos Nuevos**: 80+

---

### 🗂️ Organización por Sistema

#### **1. Sistema de Efectos Visuales**

- `entidades/efectos_emocionales.py`
  - Clase `Particula`
  - Clase `SistemaParticulas`
  - Clase `FiltroEmocional`
  - Clase `EfectosEmocionales`

#### **2. Sistema de Audio**

- `entidades/audio_emocional.py`
  - Clase `AudioEmocional`
  - Función `obtener_sistema_audio()`

#### **3. Sistema de Animaciones**

- `entidades/animaciones_emocionales.py`
  - Clase `AnimadorEmocional`
  - Clase `AnimacionContinua`

#### **4. Sistema de Narrativa**

- `entidades/narrativa_dinamica.py`
  - Clase `Dialogo`
  - Clase `NarrativaDinamica`

#### **5. Sistema de Combos**

- `entidades/combo_emocional.py`
  - Clase `ComboEmocional`
  - Clase `VisualizadorCombo`

#### **6. Sistema de Ambiente**

- `entidades/ambiente_emocional.py`
  - Clase `AmbienteEmocional`
  - Clase `FondoDinamico`

#### **7. Integración Central**

- `core/logica_cubo_fase5.py`
  - Clase `GameCuboFase5` (hereda de `GameCuboFase4`)

---

### 🔗 Dependencias entre Archivos

```
logica_cubo_fase5.py
├── efectos_emocionales.py
│   └── config/constantes.py
├── audio_emocional.py
│   └── pygame.mixer
├── animaciones_emocionales.py
│   └── pygame
├── narrativa_dinamica.py
│   └── config/constantes.py
├── combo_emocional.py
│   └── config/constantes.py
└── ambiente_emocional.py
    └── config/constantes.py
```

---

### 📂 Ubicación de Archivos en Proyecto

```
c:\Users\hugov\Documents\Trabajo - Proyecto final\
│
├── entidades/
│   ├── efectos_emocionales.py       ✅ NUEVO
│   ├── audio_emocional.py           ✅ NUEVO
│   ├── animaciones_emocionales.py   ✅ NUEVO
│   ├── narrativa_dinamica.py        ✅ NUEVO
│   ├── combo_emocional.py           ✅ NUEVO
│   ├── ambiente_emocional.py        ✅ NUEVO
│   ├── cubo.py
│   ├── meteoro.py
│   ├── portal.py
│   ├── powerup.py
│   └── ...
│
├── core/
│   ├── logica_cubo_fase5.py         ✅ NUEVO
│   ├── logica_cubo_fase4.py
│   ├── logica_cubo_fase3.py
│   ├── estados_juego.py             📝 MODIFICADO
│   └── ...
│
├── config/
│   ├── constantes.py                📝 MODIFICADO
│   └── ...
│
├── docs/
│   ├── FASE5_README.md              ✅ NUEVO
│   ├── FASE5_RESUMEN.md             ✅ NUEVO
│   ├── FASE5_INDICE.md              ✅ NUEVO (este archivo)
│   ├── README.md                    📝 MODIFICADO
│   └── ...
│
└── assets/ (opcional)
    └── audio/ (archivos de audio opcionales)
        ├── musica_feliz.mp3
        ├── musica_triste.mp3
        ├── musica_miedo.mp3
        ├── musica_dolor.mp3
        ├── musica_determinado.mp3
        ├── musica_menu.mp3
        ├── sfx_exito.wav
        ├── sfx_fracaso.wav
        ├── sfx_powerup.wav
        ├── sfx_dano.wav
        ├── sfx_click.wav
        ├── sfx_hover.wav
        ├── sfx_pieza_colocar.wav
        ├── sfx_pista.wav
        ├── sfx_meteoro.wav
        ├── sfx_portal.wav
        └── sfx_combo.wav
```

---

### 🎯 Archivos por Funcionalidad

#### **Renderizado Visual**

- `efectos_emocionales.py` - Partículas, filtros, overlays
- `ambiente_emocional.py` - Fondo, clima, iluminación

#### **Lógica de Juego**

- `combo_emocional.py` - Multiplicadores, bonos
- `logica_cubo_fase5.py` - Integración principal

#### **Feedback al Jugador**

- `narrativa_dinamica.py` - Diálogos, mensajes
- `audio_emocional.py` - Música, efectos de sonido

#### **Animación**

- `animaciones_emocionales.py` - Transformaciones, movimientos

#### **Documentación**

- `FASE5_README.md` - Guía completa
- `FASE5_RESUMEN.md` - Resumen ejecutivo
- `FASE5_INDICE.md` - Este índice

---

### 🔍 Búsqueda Rápida

**¿Necesitas modificar...?**

| Funcionalidad          | Archivo Principal            |
| ---------------------- | ---------------------------- |
| Partículas emocionales | `efectos_emocionales.py`     |
| Música/sonidos         | `audio_emocional.py`         |
| Animaciones            | `animaciones_emocionales.py` |
| Diálogos               | `narrativa_dinamica.py`      |
| Combos/multiplicadores | `combo_emocional.py`         |
| Fondo/ambiente         | `ambiente_emocional.py`      |
| Integración general    | `logica_cubo_fase5.py`       |
| Estados del juego      | `estados_juego.py`           |
| Constantes/colores     | `constantes.py`              |

---

### 📋 Checklist de Implementación

✅ Efectos visuales emocionales  
✅ Sistema de audio completo  
✅ Animaciones contextuales  
✅ Narrativa dinámica  
✅ Sistema de combos  
✅ Ambiente reactivo  
✅ Integración en GameCuboFase5  
✅ Actualización de estados del juego  
✅ Documentación completa  
✅ Testing y validación

---

### 🚀 Cómo Usar Este Índice

1. **Buscar funcionalidad**: Usa la tabla de búsqueda rápida
2. **Entender estructura**: Revisa la organización por sistema
3. **Modificar código**: Localiza el archivo en la estructura
4. **Ver documentación**: Consulta `FASE5_README.md`
5. **Revisar implementación**: Lee `FASE5_RESUMEN.md`

---

**Última actualización**: Fase 5 completada  
**Total archivos nuevos**: 8  
**Total líneas agregadas**: ~2,500

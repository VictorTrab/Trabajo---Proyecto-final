# 🔊 Lista de Sonidos - CUBO: Arquitecto del Caos

## ✅ Sonidos Existentes (Integrados)

### 📁 Ubicación: `songs/`

| #   | Archivo                        | Uso en el Juego                            | Estado       |
| --- | ------------------------------ | ------------------------------------------ | ------------ |
| 1   | `SongMenu.mp3`                 | Música del menú principal                  | ✅ Integrado |
| 2   | `SongGameStart.mp3`            | Música de inicio de juego                  | ✅ Integrado |
| 3   | `SongFacil.mp3`                | Música para niveles en dificultad Fácil    | ✅ Integrado |
| 4   | `SongMedia.mp3`                | Música para niveles en dificultad Media    | ✅ Integrado |
| 5   | `SongDificil.mp3`              | Música para niveles en dificultad Difícil  | ✅ Integrado |
| 6   | `SongJugarNivel.mp3`           | Música genérica de juego / Completar nivel | ✅ Integrado |
| 7   | `SongGameOver.mp3`             | Música de Game Over / Nivel fallido        | ✅ Integrado |
| 8   | `SongCreditos.mp3`             | Música de créditos                         | ✅ Integrado |
| 9   | `SongClick.mp3`                | Efecto de click de botón / Colocar pieza   | ✅ Integrado |
| 10  | `SongRotarFigura.mp3`          | Efecto de rotar pieza                      | ✅ Integrado |
| 11  | `SongExplotarFigura.mp3`       | Efecto de explosión / Meteoro              | ✅ Integrado |
| 12  | `SongColisionBordeVentana.mp3` | Colisión de CUBO con bordes                | ✅ Integrado |
| 13  | `SongSalirDeNivel.mp3`         | Salir de un nivel                          | ✅ Integrado |

**Total existentes**: 13 archivos

---

## ❌ Sonidos Faltantes (Por Crear)

### 🎮 Efectos de Gameplay General

| #   | Nombre Sugerido     | Descripción                                        | Duración | Tipo |
| --- | ------------------- | -------------------------------------------------- | -------- | ---- |
| 1   | **sfx_exito.wav**   | Sonido de éxito general (campana, fanfarria corta) | 0.5-1s   | WAV  |
| 2   | **sfx_fracaso.wav** | Sonido de fracaso (tono descendente, buzz)         | 0.5-1s   | WAV  |
| 3   | **sfx_hover.wav**   | Hover sobre botones del menú (sutil, suave)        | 0.1-0.2s | WAV  |

### 🧩 Efectos de Piezas (Fase 2-3)

| #   | Nombre Sugerido          | Descripción                              | Duración | Tipo |
| --- | ------------------------ | ---------------------------------------- | -------- | ---- |
| 4   | **sfx_pieza_soltar.wav** | Soltar pieza sin colocarla correctamente | 0.2-0.3s | WAV  |
| 5   | **sfx_pista.wav**        | Usar pista (sonido de revelación, chime) | 0.4-0.6s | WAV  |

### ⚡ Efectos de PowerUps (Fase 4)

| #   | Nombre Sugerido        | Descripción                                     | Duración | Tipo |
| --- | ---------------------- | ----------------------------------------------- | -------- | ---- |
| 6   | **sfx_powerup.wav**    | Recoger power-up genérico (power-up positivo)   | 0.3-0.5s | WAV  |
| 7   | **sfx_escudo.wav**     | Activar escudo protector (whoosh + ding)        | 0.4-0.6s | WAV  |
| 8   | **sfx_velocidad.wav**  | Activar velocidad aumentada (zoom, aceleración) | 0.3-0.5s | WAV  |
| 9   | **sfx_magnetismo.wav** | Activar magnetismo (zap eléctrico, atracción)   | 0.3-0.5s | WAV  |

### 🌠 Efectos de Fase 4 (Meteoros y Portales)

| #   | Nombre Sugerido     | Descripción                                   | Duración | Tipo |
| --- | ------------------- | --------------------------------------------- | -------- | ---- |
| 10  | **sfx_meteoro.wav** | Impacto de meteoro (crash, impacto fuerte)    | 0.4-0.7s | WAV  |
| 11  | **sfx_portal.wav**  | Usar portal (whoosh espacial, teletransporte) | 0.5-0.8s | WAV  |

### 💥 Efectos de Daño y Dolor

| #   | Nombre Sugerido  | Descripción                          | Duración | Tipo |
| --- | ---------------- | ------------------------------------ | -------- | ---- |
| 12  | **sfx_dano.wav** | Recibir daño (impacto, golpe, dolor) | 0.2-0.4s | WAV  |

### 🔥 Efectos de Combos (Fase 5)

| #   | Nombre Sugerido   | Descripción                                     | Duración | Tipo |
| --- | ----------------- | ----------------------------------------------- | -------- | ---- |
| 13  | **sfx_combo.wav** | Alcanzar nuevo nivel de combo (jingle positivo) | 0.4-0.6s | WAV  |

**Total faltantes**: 13 archivos

---

## 📊 Resumen de Integración

### Mapeo de Eventos a Sonidos

#### **Música de Fondo (ループ)**

```python
"menu" → SongMenu.mp3
"inicio_juego" → SongGameStart.mp3 (no loop)
"nivel_facil" → SongFacil.mp3
"nivel_medio" → SongMedia.mp3
"nivel_dificil" → SongDificil.mp3
"jugando" → SongJugarNivel.mp3
"game_over" → SongGameOver.mp3
"creditos" → SongCreditos.mp3
```

#### **Emociones → Música**

```python
"feliz" → SongFacil.mp3
"triste" → SongGameOver.mp3
"miedo" → SongDificil.mp3
"dolor" → SongGameOver.mp3
"determinado" → SongMedia.mp3
```

#### **Efectos de Sonido (Existentes)**

```python
"click" → SongClick.mp3
"pieza_colocar" → SongClick.mp3
"pieza_rotar" → SongRotarFigura.mp3
"explotar" → SongExplotarFigura.mp3
"cubo_colision" → SongColisionBordeVentana.mp3
"salir_nivel" → SongSalirDeNivel.mp3
"nivel_completado" → SongJugarNivel.mp3
"nivel_fallido" → SongGameOver.mp3
"meteoro_explosion" → SongExplotarFigura.mp3
```

#### **Efectos de Sonido (Faltantes)**

```python
"hover" → sfx_hover.wav
"exito" → sfx_exito.wav
"fracaso" → sfx_fracaso.wav
"pieza_soltar" → sfx_pieza_soltar.wav
"pista" → sfx_pista.wav
"powerup" → sfx_powerup.wav
"escudo_activar" → sfx_escudo.wav
"velocidad_activar" → sfx_velocidad.wav
"magnetismo" → sfx_magnetismo.wav
"meteoro" → sfx_meteoro.wav
"portal" → sfx_portal.wav
"dano" → sfx_dano.wav
"combo" → sfx_combo.wav
```

---

## 🎨 Sugerencias de Creación de Sonidos

### Herramientas Recomendadas

1. **Gratuitas**:

   - [Audacity](https://www.audacityteam.org/) - Editor de audio
   - [SFXR](http://www.drpetter.se/project_sfxr.html) - Generador de SFX retro
   - [ChipTone](https://sfbgames.itch.io/chiptone) - Generador de SFX chiptune
   - [Bfxr](https://www.bfxr.net/) - Generador de SFX mejorado

2. **Online**:

   - [Freesound.org](https://freesound.org/) - Banco de sonidos libres
   - [Zapsplat](https://www.zapsplat.com/) - SFX gratuitos

3. **Con IA**:
   - [ElevenLabs Sound Effects](https://elevenlabs.io/) - Generador con IA
   - [Soundraw](https://soundraw.io/) - Música con IA

### Especificaciones Técnicas

**Formato**: WAV (sin compresión, mayor calidad para efectos cortos)  
**Tasa de muestreo**: 44100 Hz  
**Bits**: 16-bit  
**Canales**: Mono (efectos) / Stereo (música)  
**Duración típica**: 0.1s - 1s para efectos

### Características por Categoría

#### **1. Efectos de UI (hover, click)**

- Tono: Agudo, limpio
- Volumen: Bajo-medio
- Estilo: Minimalista, no invasivo
- Referencia: Beeps electrónicos suaves

#### **2. Efectos de Piezas (soltar, pista)**

- Tono: Medio
- Volumen: Medio
- Estilo: Mecánico pero agradable
- Referencia: Puzzle games (Tetris, Portal)

#### **3. Efectos de PowerUps (escudo, velocidad, magnetismo)**

- Tono: Variado por tipo
  - Escudo: Grave, protector (whoosh + ding)
  - Velocidad: Agudo, rápido (zoom)
  - Magnetismo: Medio, eléctrico (zap)
- Volumen: Medio-alto
- Estilo: Energético, positivo
- Referencia: Mario Kart, Sonic

#### **4. Efectos de Fase 4 (meteoro, portal)**

- Tono:
  - Meteoro: Grave, impactante
  - Portal: Medio-agudo, espacial
- Volumen: Alto
- Estilo: Dramático, sci-fi
- Referencia: Portal, Halo

#### **5. Efectos de Daño (dano)**

- Tono: Medio-grave
- Volumen: Medio-alto
- Estilo: Negativo pero no excesivo
- Referencia: Zelda (damage sound)

#### **6. Efectos de Combos (combo)**

- Tono: Agudo, ascendente
- Volumen: Medio
- Estilo: Positivo, recompensa
- Referencia: Fighting games (Street Fighter)

---

## 🎵 Nombres de Archivos Sugeridos (Estilo Actual)

Si prefieres mantener el estilo de nomenclatura actual (`Song*`):

### Alternativas con prefijo "Song"

```
SongExito.mp3
SongFracaso.mp3
SongHover.mp3
SongSoltarPieza.mp3
SongPista.mp3
SongPowerUp.mp3
SongEscudo.mp3
SongVelocidad.mp3
SongMagnetismo.mp3
SongMeteoro.mp3
SongPortal.mp3
SongDano.mp3
SongCombo.mp3
```

### Recomendación

Usar prefijo **`sfx_`** para efectos cortos (< 1s) y **`Song`** para música/efectos largos, para diferenciarlos claramente en el código y explorador de archivos.

---

## 📝 Checklist de Creación

### Prioridad Alta (Más usados)

- [ ] **sfx_hover.wav** - Se activa constantemente en menús
- [ ] **sfx_powerup.wav** - Parte central de Fase 4
- [ ] **sfx_combo.wav** - Retroalimentación importante de Fase 5
- [ ] **sfx_dano.wav** - Feedback crítico de gameplay

### Prioridad Media

- [ ] **sfx_escudo.wav**
- [ ] **sfx_velocidad.wav**
- [ ] **sfx_magnetismo.wav**
- [ ] **sfx_pista.wav**
- [ ] **sfx_pieza_soltar.wav**

### Prioridad Baja (Pueden usar existentes temporalmente)

- [ ] **sfx_exito.wav** - Puede usar SongJugarNivel temporalmente
- [ ] **sfx_fracaso.wav** - Puede usar SongGameOver temporalmente
- [ ] **sfx_meteoro.wav** - Puede usar SongExplotarFigura temporalmente
- [ ] **sfx_portal.wav** - Puede usar SongRotarFigura temporalmente

---

## 🚀 Cómo Agregar Nuevos Sonidos

1. **Crear/Descargar el archivo de audio**
2. **Convertir a formato WAV (si es necesario)**
   ```bash
   ffmpeg -i archivo.mp3 archivo.wav
   ```
3. **Copiar a la carpeta `songs/`**
4. **El sistema ya está configurado** - Los sonidos se cargarán automáticamente

**Nota**: El sistema funciona en modo silencioso si los archivos no existen, por lo que puedes agregar sonidos progresivamente sin romper el juego.

---

## 📊 Estadísticas Finales

- **Sonidos existentes**: 13
- **Sonidos faltantes**: 13
- **Total necesario**: 26 archivos de audio
- **Porcentaje completado**: 50%

**Estado de integración**: ✅ Sistema de audio completamente integrado y funcional

---

**Última actualización**: Fase 5 - Integración de Audio Completa

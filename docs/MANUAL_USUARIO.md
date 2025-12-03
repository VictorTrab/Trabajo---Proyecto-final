# 📖 Manual de Usuario - CUBO: Arquitecto del Caos

## 🎮 Guía Completa del Jugador

---

## 📑 Índice

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Inicio del Juego](#inicio-del-juego)
4. [Controles](#controles)
5. [Cómo Jugar](#cómo-jugar)
6. [Elementos del Juego](#elementos-del-juego)
7. [Sistema de Puntuación](#sistema-de-puntuación)
8. [Consejos y Estrategias](#consejos-y-estrategias)
9. [Preguntas Frecuentes](#preguntas-frecuentes)
10. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Introducción

**CUBO: Arquitecto del Caos** es un juego de puzzle geométrico donde controlas a CUBO, un personaje robótico que debe recolectar y ensamblar piezas para completar figuras objetivo mientras evita obstáculos dinámicos.

### Objetivo del Juego

Completa cada nivel ensamblando correctamente las piezas geométricas según la figura objetivo mostrada en pantalla, antes de que se agote el tiempo.

---

## 💿 Instalación

### Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, Linux, macOS
- **Python:** Versión 3.10.0 o superior
- **RAM:** Mínimo 2 GB
- **Espacio en Disco:** 100 MB

### Pasos de Instalación

1. **Descargar el juego:**

   - Descarga el archivo del proyecto desde el repositorio

2. **Instalar Python:**

   - Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org)
   - Durante la instalación, marca la opción "Add Python to PATH"

3. **Instalar dependencias:**

   ```bash
   # Abrir terminal en la carpeta del juego
   pip install -r requirements.txt
   ```

4. **Ejecutar el juego:**
   ```bash
   python principal.py
   ```

---

## 🚀 Inicio del Juego

### Pantalla Principal

Al iniciar el juego, verás el menú principal con las siguientes opciones:

```
┌─────────────────────────────┐
│  CUBO: Arquitecto del Caos  │
├─────────────────────────────┤
│  ▶ JUGAR                    │
│    PERFIL DEL JUGADOR       │
│    ACERCA DE                │
│    SALIR                    │
└─────────────────────────────┘
```

- **JUGAR:** Accede a la selección de niveles
- **PERFIL DEL JUGADOR:** Ver estadísticas y progreso
- **ACERCA DE:** Información del juego y créditos
- **SALIR:** Cerrar el juego

---

## 🎮 Controles

### Controles Básicos

| Acción              | Tecla(s)                         |
| ------------------- | -------------------------------- |
| **Mover CUBO**      | ↑ ↓ ← → o W A S D                |
| **Arrastrar pieza** | Click izquierdo + Mover mouse    |
| **Soltar pieza**    | Soltar click izquierdo           |
| **Rotar pieza**     | R (mientras sostienes una pieza) |
| **Usar pista**      | H (3 pistas disponibles)         |
| **Pausar/Salir**    | ESC                              |

### Controles en Menús

| Acción                 | Control              |
| ---------------------- | -------------------- |
| **Seleccionar opción** | Click izquierdo      |
| **Navegar**            | Mover mouse          |
| **Volver**             | ESC o botón "Volver" |

**Nota:** Escucharás un sonido de "click" al seleccionar cualquier opción en los menús.

---

## 🎲 Cómo Jugar

### Paso a Paso para Principiantes

#### 1. Selecciona un Nivel

En la pantalla de selección de niveles:

- **Nivel 1:** Fácil (2-3 piezas)
- **Nivel 2:** Medio (4-5 piezas)
- **Nivel 3:** Difícil (6-8 piezas)

Los niveles se desbloquean progresivamente. Debes completar el Nivel 1 para acceder al Nivel 2, y así sucesivamente.

#### 2. Comprende la Pantalla de Juego

```
┌────────────────────────────────────────────┐
│ Nivel: 1    Tiempo: 01:45    Piezas: 5/8  │ ← Información superior
├────────────────────────────────────────────┤
│ Puntos: 1500                               │
│ Intentos: 3/10        ┌──────────┐        │
│ Pistas: 2/3           │  FIGURA  │        │ ← Figura objetivo
│ Vidas: 2/2            │ OBJETIVO │        │
│                       └──────────┘        │
│                                            │
│         🟦 ← CUBO                          │
│                                            │
│    △  ▢  ●  ◆  ▭  (Piezas disponibles)    │
│                                            │
│              ☄️ ← Meteoro                  │
│                                            │
│         🌀 ← Portal                        │
└────────────────────────────────────────────┘
```

#### 3. Recolecta Piezas

1. Mueve a CUBO cerca de una pieza usando las flechas o WASD
2. Haz click sobre la pieza y arrástrala
3. CUBO la recogerá automáticamente

#### 4. Ensambla la Figura

1. Arrastra la pieza hacia la zona de la figura objetivo (centro-derecha)
2. Rota la pieza con **R** si es necesario
3. Suelta la pieza cuando esté en la posición correcta
4. Si la pieza encaja, verás un efecto visual de confirmación ✅
5. Si no encaja, la pieza volverá al pool disponible ❌

#### 5. Completa el Nivel

- Ensambla todas las piezas correctamente
- Evita meteoros (te quitan vida)
- Usa portales para moverte rápidamente
- Recoge power-ups para ventajas temporales

---

## 🧩 Elementos del Juego

### Piezas Geométricas

| Forma          | Símbolo | Descripción                     |
| -------------- | ------- | ------------------------------- |
| **Cuadrado**   | ▢       | Pieza básica de 4 lados iguales |
| **Triángulo**  | △       | Pieza de 3 lados                |
| **Círculo**    | ●       | Pieza redonda                   |
| **Rombo**      | ◆       | Cuadrado rotado 45°             |
| **Rectángulo** | ▭       | Pieza alargada                  |

**Nota:** Hay piezas "distractor" que no pertenecen a la figura objetivo. Ignóralas.

### CUBO (Personaje)

**Estados Emocionales:**

- 😊 **Feliz:** Cuando colocas piezas correctamente
- 😢 **Triste:** Cuando fallas múltiples intentos
- 😰 **Neutral:** Estado normal
- 🤕 **Dolor:** Al recibir daño de meteoros

Los estados emocionales afectan las animaciones y efectos visuales.

### Obstáculos

#### ☄️ Meteoros

- **Aparición:** Cada 5-8 segundos
- **Efecto:** Quitan 1 punto de vida al impactar
- **Advertencia:** Línea de trayectoria antes de caer
- **Estrategia:** Observa la advertencia y muévete a un lugar seguro

#### 🚧 Límites de Pantalla

- CUBO no puede salir de los bordes de la pantalla

### Elementos Útiles

#### 🌀 Portales

- **Función:** Teletransportación instantánea
- **Ubicación:** Aparecen en pares (entrada → salida)
- **Uso:** Mueve a CUBO sobre un portal para teletransportarte
- **Cooldown:** 2 segundos entre usos

#### 🎁 Power-ups

Power-ups aparecen aleatoriamente durante el juego:

| Power-up       | Icono | Efecto                         | Duración    |
| -------------- | ----- | ------------------------------ | ----------- |
| **Escudo**     | 🛡️    | Protección contra meteoros     | 10 segundos |
| **Velocidad**  | ⚡    | Movimiento más rápido          | 8 segundos  |
| **Magnetismo** | 🧲    | Atracción automática de piezas | 12 segundos |

#### 💡 Pistas

- **Cantidad:** 3 por nivel
- **Activación:** Presiona **H**
- **Efecto:** Muestra qué pieza colocar a continuación
- **Penalización:** -100 puntos por pista usada

---

## 🏆 Sistema de Puntuación

### Puntos Base

- **Inicio:** 1000 puntos

### Bonificaciones

| Bonus           | Máximo   | Condición               |
| --------------- | -------- | ----------------------- |
| **Tiempo**      | +500 pts | Completar rápidamente   |
| **Precisión**   | +300 pts | Usar menos piezas extra |
| **Sin Errores** | +200 pts | Cero intentos fallidos  |

### Penalizaciones

| Penalización        | Cantidad |
| ------------------- | -------- |
| **Intento Fallido** | -25 pts  |
| **Pista Usada**     | -100 pts |

### Cálculo Final

```
Puntuación = 1000 + Bonus Tiempo + Bonus Precisión + Bonus Sin Errores
             - (Intentos Fallidos × 25) - (Pistas Usadas × 100)
```

### Ejemplo

```
Puntos Base:           1000
Bonus Tiempo:          +350
Bonus Precisión:       +250
Bonus Sin Errores:     +200
Intentos Fallidos:     -75  (3 intentos)
Pistas Usadas:         -200 (2 pistas)
─────────────────────
TOTAL:                 1525 puntos
```

---

## 💪 Consejos y Estrategias

### Para Principiantes

1. **📋 Observa Primero**

   - Estudia la figura objetivo antes de empezar
   - Identifica qué piezas necesitas

2. **⏰ No te Apresures**

   - Tienes 2 minutos (120 segundos)
   - Es mejor ser preciso que rápido

3. **🔄 Usa la Rotación**

   - Presiona **R** para rotar piezas
   - Algunas piezas necesitan orientación específica

4. **💡 Usa Pistas con Moderación**
   - Reserva las pistas para momentos difíciles
   - Recuerda que restan 100 puntos cada una

### Estrategias Avanzadas

1. **🎯 Orden de Colocación**

   - Coloca primero las piezas centrales
   - Luego completa los bordes

2. **🌀 Domina los Portales**

   - Úsalos para escapar de meteoros
   - Aprovecha el cooldown de 2 segundos

3. **☄️ Predice Meteoros**

   - Observa las líneas de advertencia
   - Calcula trayectorias antes de moverse

4. **🎁 Prioriza Power-ups**

   - **Escudo:** Perfecto cuando hay muchos meteoros
   - **Velocidad:** Útil para recolectar piezas rápidamente
   - **Magnetismo:** Facilita el ensamblaje

5. **📊 Maximiza Puntos**
   - Completa sin errores para +200 puntos
   - Termina rápido para bonus de tiempo
   - No uses piezas extra (bonus de precisión)

### Errores Comunes a Evitar

❌ **No hacer:** Intentar colocar piezas sin rotar  
✅ **Hacer:** Verificar orientación antes de soltar

❌ **No hacer:** Ignorar meteoros hasta último momento  
✅ **Hacer:** Mantenerse en movimiento constantemente

❌ **No hacer:** Usar todas las pistas al principio  
✅ **Hacer:** Reservarlas para piezas complicadas

---

## ❓ Preguntas Frecuentes

### ¿Cómo guardo mi progreso?

El juego guarda automáticamente al completar cada nivel. No necesitas hacer nada especial.

### ¿Puedo cambiar el volumen?

Sí, en el menú principal hay una opción de configuración donde puedes ajustar:

- Volumen de música
- Volumen de efectos de sonido

### ¿Qué pasa si pierdo todas las vidas?

Game Over. Puedes:

- **Reintentar:** Volver a jugar el mismo nivel
- **Volver al Menú:** Regresar a la selección de niveles

### ¿Cómo desbloqueo niveles?

Los niveles se desbloquean automáticamente al completar el nivel anterior. No puedes saltar niveles.

### ¿Puedo reiniciar mi progreso?

Sí, en la pantalla de **Perfil del Jugador** hay un botón para **Reiniciar Progreso**. Esto borrará todos tus datos guardados.

### ¿Qué pasa si se agota el tiempo?

Si el cronómetro llega a 0:00, pierdes el nivel automáticamente (Game Over).

### ¿Cuántos intentos fallidos puedo tener?

Máximo **10 intentos fallidos** por nivel. Cada intento fallido ocurre cuando sueltas una pieza en un lugar incorrecto.

---

## 🔧 Solución de Problemas

### El juego no inicia

**Problema:** Error al ejecutar `python principal.py`

**Solución:**

1. Verifica que Python esté instalado: `python --version`
2. Instala dependencias: `pip install -r requirements.txt`
3. Asegúrate de estar en la carpeta correcta

### Sin audio

**Problema:** No se escucha música ni efectos

**Solución:**

1. Verifica que los archivos en la carpeta `songs/` existan
2. Comprueba el volumen del sistema
3. Revisa la consola por mensajes de error del tipo `[AudioDinamico]`
4. Verifica que pygame.mixer esté correctamente inicializado

**Nota:** El juego usa `audio_dinamico.py` que valida archivos antes de reproducir. Si falta un archivo de audio, verás un mensaje en consola pero el juego continuará funcionando.

### El juego va lento (FPS bajos)

**Problema:** Movimientos entrecortados

**Solución:**

1. Cierra otros programas pesados
2. Reduce la resolución de pantalla (si es posible)
3. Verifica que tu PC cumpla los requisitos mínimos

### No se guardan los datos

**Problema:** El progreso no se guarda

**Solución:**

1. Verifica que tengas permisos de escritura en la carpeta del juego
2. Busca el archivo `save_game.json` - debe existir
3. No cierres el juego abruptamente (usa ESC → Salir)

### Las piezas no se pueden arrastrar

**Problema:** No puedo mover piezas con el mouse

**Solución:**

1. Verifica que estés haciendo click directamente sobre la pieza
2. Mantén presionado el botón izquierdo mientras mueves
3. Asegúrate de que CUBO esté cerca de la pieza

---

## 📞 Soporte

Si experimentas problemas no listados aquí:

1. Revisa la documentación técnica en `docs/`
2. Verifica que todos los archivos del juego estén presentes
3. Reinstala las dependencias: `pip install --force-reinstall -r requirements.txt`

---

## 🎓 Créditos

**Desarrolladores:** V.H & R.  
**Versión:** 3.6  
**Año:** 2025  
**Propósito:** Proyecto Académico - Informática Gráfica

---

## 📚 Más Información

Para información técnica adicional, consulta:

- `docs/RESUMEN_PROYECTO.md` - Resumen académico
- `docs/ARQUITECTURA_TECNICA.md` - Arquitectura del software
- `docs/GUIA_DESARROLLO.md` - Guía para desarrolladores

---

**¡Disfruta jugando CUBO: Arquitecto del Caos!** 🎮✨

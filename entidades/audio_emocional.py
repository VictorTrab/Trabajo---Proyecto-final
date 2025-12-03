"""
Sistema de Audio Emocional - Fase 5
Gestión de música y efectos de sonido según emoción
"""

import pygame
from typing import Dict, Optional
from pathlib import Path


class AudioEmocional:
    """Sistema de audio que responde a estados emocionales"""

    def __init__(self, habilitar_audio: bool = True):
        self.habilitado = habilitar_audio
        self.inicializado = False

        # Configuración de volumen
        self.volumen_musica = 0.5
        self.volumen_efectos = 0.7

        # Estado actual
        self.emocion_actual = None
        self.musica_actual = None

        # Diccionario de rutas de audio (usando archivos existentes en songs/)
        self.rutas_musica = {
            "menu": "songs/SongMenu.mp3",
            "inicio_juego": "songs/SongGameStart.mp3",
            "nivel_facil": "songs/SongFacil.mp3",
            "nivel_medio": "songs/SongMedia.mp3",
            "nivel_dificil": "songs/SongDificil.mp3",
            "jugando": "songs/SongMenu.mp3",  # Usar música del menú temporalmente
            "game_over": "songs/SongGameOver.mp3",
            "creditos": "songs/SongCreditos.mp3",
            # Mapeo de emociones a canciones existentes
            "neutral": "songs/SongFacil.mp3",  # Emoción neutral usa música fácil
            "feliz": "songs/SongFacil.mp3",
            "triste": "songs/SongGameOver.mp3",
            "miedo": "songs/SongDificil.mp3",
            "dolor": "songs/SongGameOver.mp3",
            "determinado": "songs/SongMedia.mp3",
        }

        self.rutas_efectos = {
            # Efectos existentes en songs/
            "click": "songs/SongClick.mp3",
            "rotar": "songs/SongRotarFigura.mp3",
            "explotar": "songs/SongExplotarFigura.mp3",
            "colision_borde": "songs/SongColisionBordeVentana.mp3",
            "salir_nivel": "songs/SongSalirDeNivel.mp3",
            # Mapeo de eventos de UI a sonidos existentes
            "ui_navigate": "songs/SongRotarFigura.mp3",  # Sonido de navegación
            "ui_select": "songs/SongClick.mp3",  # Sonido de selección
            "ui_back": "songs/SongSalirDeNivel.mp3",  # Sonido de retroceder
            # Mapeo de eventos a sonidos existentes
            "pieza_colocar": "songs/SongClick.mp3",
            "pieza_rotar": "songs/SongRotarFigura.mp3",
            "boton_click": "songs/SongClick.mp3",
            "nivel_completado": "songs/SongGameStart.mp3",
            "nivel_fallido": "songs/SongGameOver.mp3",
            "cubo_colision": "songs/SongColisionBordeVentana.mp3",
            # Efectos que necesitan crearse (se marcarán como faltantes)
            "exito": "songs/sfx_exito.wav",
            "fracaso": "songs/sfx_fracaso.wav",
            "powerup": "songs/sfx_powerup.wav",
            "dano": "songs/sfx_dano.wav",
            "hover": "songs/sfx_hover.wav",
            "pista": "songs/sfx_pista.wav",
            "meteoro": "songs/sfx_meteoro.wav",
            "portal": "songs/sfx_portal.wav",
            "combo": "songs/sfx_combo.wav",
            "magnetismo": "songs/sfx_magnetismo.wav",
            "pieza_soltar": "songs/sfx_pieza_soltar.wav",
            "escudo_activar": "songs/sfx_escudo.wav",
            "velocidad_activar": "songs/sfx_velocidad.wav",
        }

        # Caché de sonidos cargados
        self.sonidos_cargados: Dict[str, pygame.mixer.Sound] = {}

        if self.habilitado:
            self._inicializar()

    def _inicializar(self):
        """Inicializa pygame.mixer si es posible"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

            pygame.mixer.music.set_volume(self.volumen_musica)
            self.inicializado = True
            print("[AudioEmocional] Sistema de audio inicializado")
        except pygame.error as e:
            print(f"[AudioEmocional] No se pudo inicializar audio: {e}")
            self.habilitado = False
            self.inicializado = False

    def _verificar_archivo(self, ruta: str) -> bool:
        """Verifica si un archivo de audio existe"""
        return Path(ruta).exists()

    def reproducir_musica(self, emocion: str, loop: bool = True, fade_ms: int = 1500):
        """Reproduce música emocional con transición suave"""
        if not self.habilitado or not self.inicializado:
            return

        # Solo evitar reproducir si es la MISMA emoción Y está REALMENTE sonando
        if self.emocion_actual == emocion and pygame.mixer.music.get_busy():
            return

        ruta = self.rutas_musica.get(emocion)
        if not ruta:
            print(f"[AudioEmocional] Emoción no encontrada: {emocion}")
            return

        if not self._verificar_archivo(ruta):
            print(f"[AudioEmocional] Archivo no encontrado: {ruta}")
            return

        try:
            # Detener música actual completamente antes de cargar nueva
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.time.wait(50)

            # Cargar y reproducir nueva música
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1 if loop else 0)

            # Aplicar volumen
            pygame.mixer.music.set_volume(self.volumen_musica)

            self.emocion_actual = emocion
            self.musica_actual = ruta

        except pygame.error as e:
            print(f"[AudioEmocional] Error al reproducir música: {e}")

        except pygame.error as e:
            print(f"[AudioEmocional] Error al reproducir música: {e}")

    def reproducir_efecto(self, nombre_efecto: str):
        """Reproduce un efecto de sonido"""
        if not self.habilitado or not self.inicializado:
            return

        ruta = self.rutas_efectos.get(nombre_efecto)
        if not ruta:
            print(f"[AudioEmocional] Efecto de sonido no definido: {nombre_efecto}")
            return

        # Usar caché si ya se cargó
        if nombre_efecto in self.sonidos_cargados:
            sonido = self.sonidos_cargados[nombre_efecto]
        else:
            # Verificar que existe
            if not self._verificar_archivo(ruta):
                print(f"[AudioEmocional] Archivo de efecto no encontrado: {ruta}")
                return

            try:
                sonido = pygame.mixer.Sound(ruta)
                sonido.set_volume(self.volumen_efectos)
                self.sonidos_cargados[nombre_efecto] = sonido
                print(
                    f"[AudioEmocional] Efecto cargado exitosamente: {nombre_efecto} -> {ruta}"
                )
            except pygame.error as e:
                print(f"[AudioEmocional] Error al cargar efecto {nombre_efecto}: {e}")
                return

        try:
            sonido.play()
            print(f"[AudioEmocional] Reproduciendo efecto: {nombre_efecto}")
        except pygame.error as e:
            print(f"[AudioEmocional] Error al reproducir efecto {nombre_efecto}: {e}")

    def pausar_musica(self):
        """Pausa la música actual"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.pause()

    def reanudar_musica(self):
        """Reanuda la música pausada"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.unpause()

    def detener_musica(self, fade_ms: int = 1000):
        """Detiene la música con fade out"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.fadeout(fade_ms)
            self.emocion_actual = None
            self.musica_actual = None

    def cambiar_volumen_musica(self, volumen: float):
        """Cambia el volumen de la música (0.0 a 1.0)"""
        self.volumen_musica = max(0.0, min(1.0, volumen))
        if self.habilitado and self.inicializado:
            pygame.mixer.music.set_volume(self.volumen_musica)

    def cambiar_volumen_efectos(self, volumen: float):
        """Cambia el volumen de efectos (0.0 a 1.0)"""
        self.volumen_efectos = max(0.0, min(1.0, volumen))
        # Actualizar volumen de sonidos ya cargados
        for sonido in self.sonidos_cargados.values():
            sonido.set_volume(self.volumen_efectos)

    def actualizar_emocion(self, nueva_emocion: str):
        """Actualiza música según cambio de emoción"""
        if nueva_emocion != self.emocion_actual:
            self.reproducir_musica(nueva_emocion)

    def reproducir_musica_por_dificultad(self, dificultad: str):
        """Reproduce música según la dificultad del nivel"""
        mapeo_dificultad = {
            "Fácil": "nivel_facil",
            "Medio": "nivel_medio",
            "Difícil": "nivel_dificil",
        }

        tipo_musica = mapeo_dificultad.get(dificultad, "jugando")
        self.reproducir_musica(tipo_musica)

    def reproducir_musica_menu(self):
        """Reproduce música del menú principal"""
        self.reproducir_musica("menu")

    def reproducir_musica_creditos(self):
        """Reproduce música de créditos"""
        self.reproducir_musica("creditos")

    def reproducir_musica_inicio_juego(self):
        """Reproduce música de inicio de juego"""
        self.reproducir_musica("inicio_juego", loop=False)

    def reproducir_musica_jugando(self):
        """Reproduce música genérica de juego"""
        self.reproducir_musica("jugando")

    def evento_juego(self, tipo_evento: str):
        """Reproduce efecto según evento del juego"""
        efectos_eventos = {
            # Eventos de nivel
            "nivel_completado": "nivel_completado",
            "nivel_fallido": "nivel_fallido",
            "salir_nivel": "salir_nivel",
            # Eventos de piezas
            "pieza_colocada": "pieza_colocar",
            "pieza_rotada": "pieza_rotar",
            "pieza_soltar": "pieza_soltar",
            "pieza_explotar": "explotar",
            # Eventos de CUBO
            "cubo_colision_borde": "cubo_colision",
            "dano_recibido": "dano",
            # PowerUps (Fase 4)
            "powerup_obtenido": "powerup",
            "escudo_activado": "escudo_activar",
            "velocidad_activada": "velocidad_activar",
            "magnetismo_activado": "magnetismo",
            # Fase 4: Meteoros y Portales
            "meteoro_impacto": "meteoro",
            "meteoro_explosion": "explotar",
            "portal_usado": "portal",
            # Fase 3: Pistas
            "pista_usada": "pista",
            # Fase 5: Combos
            "combo_alcanzado": "combo",
            # UI
            "boton_click": "click",
            "menu_hover": "hover",
            # Éxito/Fracaso general
            "exito": "exito",
            "fracaso": "fracaso",
        }

        efecto = efectos_eventos.get(tipo_evento)
        if efecto:
            self.reproducir_efecto(efecto)

    def obtener_estado(self) -> Dict:
        """Obtiene información del estado del audio"""
        return {
            "habilitado": self.habilitado,
            "inicializado": self.inicializado,
            "emocion_actual": self.emocion_actual,
            "musica_actual": self.musica_actual,
            "volumen_musica": self.volumen_musica,
            "volumen_efectos": self.volumen_efectos,
            "musica_reproduciendo": (
                pygame.mixer.music.get_busy() if self.inicializado else False
            ),
        }

    def limpiar(self):
        """Limpia recursos de audio"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.stop()
            for sonido in self.sonidos_cargados.values():
                sonido.stop()
            self.sonidos_cargados.clear()

        self.emocion_actual = None
        self.musica_actual = None


# Singleton global (opcional)
_instancia_audio: Optional[AudioEmocional] = None


def obtener_sistema_audio(habilitar: bool = True) -> AudioEmocional:
    """Obtiene la instancia singleton del sistema de audio"""
    global _instancia_audio
    if _instancia_audio is None:
        _instancia_audio = AudioEmocional(habilitar_audio=habilitar)
    return _instancia_audio

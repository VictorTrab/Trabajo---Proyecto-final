"""
Sistema de Audio Dinámico
Gestión de música y efectos de sonido para jugabilidad
"""

import pygame
from pathlib import Path


class AudioDinamico:
    """Sistema de audio enfocado en jugabilidad"""

    def __init__(self):
        """Inicializa el sistema de audio"""
        self.habilitado = True
        self.inicializado = False

        # Volúmenes
        self.volumen_musica = 0.5
        self.volumen_efectos = 0.7

        # Estado
        self.musica_actual = None

        # Rutas de música por contexto
        self.rutas_musica = {
            "menu": "songs/SongMenu.mp3",
            "nivel1": "songs/Nivel1.mp3",
            "nivel2": "songs/Nivel2.mp3",
            "nivel3": "songs/Nivel3.mp3",
            "completado": "songs/SongGameStart.mp3",
            "game_over": "songs/SongGameOver.mp3",
            "creditos": "songs/SongCreditos.mp3",
        }

        # Rutas de efectos de jugabilidad
        self.rutas_efectos = {
            # Efectos de piezas
            "click": "songs/SongClick.mp3",
            "rotar": "songs/SongRotarFigura.mp3",
            "colocar": "songs/SongClick.mp3",
            "explotar": "songs/SongExplocion.mp3",
            # Efectos de colisión/error
            "colision_borde": "songs/SongColisionBordeVentana.mp3",
            "error": "songs/SongColisionBordeVentana.mp3",
            # Efectos de navegación
            "salir_nivel": "songs/SongSalirDeNivel.mp3",
            "iniciar_nivel": "songs/SongGameStart.mp3",
        }

        # Caché de efectos cargados
        self.efectos_cargados = {}

        # Inicializar
        self._inicializar()

    def _inicializar(self):
        """Inicializa pygame.mixer"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

            pygame.mixer.music.set_volume(self.volumen_musica)
            self.inicializado = True
            print("[AudioDinamico] Sistema de audio inicializado")
        except pygame.error as e:
            print(f"[AudioDinamico] Error al inicializar audio: {e}")
            self.habilitado = False

    def _verificar_archivo(self, ruta):
        """Verifica si existe un archivo"""
        return Path(ruta).exists()

    def reproducir_musica(self, tipo):
        """
        Reproduce música de fondo

        Args:
            tipo: Tipo de música ("menu", "nivel1", "nivel2", "nivel3", etc.)
        """
        if not self.habilitado or not self.inicializado:
            return

        if not pygame.mixer.get_init():
            return

        # Si ya está sonando esta música, no hacer nada
        if self.musica_actual == tipo and pygame.mixer.music.get_busy():
            return

        ruta = self.rutas_musica.get(tipo)
        if not ruta or not self._verificar_archivo(ruta):
            return

        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.volumen_musica)

            self.musica_actual = tipo
        except pygame.error as e:
            print(f"[AudioDinamico] Error al reproducir música '{tipo}': {e}")
            self.musica_actual = None

    def reproducir_efecto(self, nombre):
        """
        Reproduce un efecto de sonido

        Args:
            nombre: Nombre del efecto ("click", "rotar", "explotar", etc.)
        """
        if not self.habilitado or not self.inicializado:
            return

        ruta = self.rutas_efectos.get(nombre)
        if not ruta or not self._verificar_archivo(ruta):
            return

        # Usar caché si ya se cargó
        if nombre in self.efectos_cargados:
            sonido = self.efectos_cargados[nombre]
        else:
            try:
                sonido = pygame.mixer.Sound(ruta)
                sonido.set_volume(self.volumen_efectos)
                self.efectos_cargados[nombre] = sonido
            except pygame.error as e:
                print(f"[AudioDinamico] Error al cargar efecto '{nombre}': {e}")
                return

        try:
            sonido.play()
        except pygame.error as e:
            print(f"[AudioDinamico] Error al reproducir efecto '{nombre}': {e}")

    def reproducir_musica_nivel(self, nivel_numero):
        """
        Reproduce música según número de nivel

        Args:
            nivel_numero: Número del nivel (1, 2, 3)
        """
        tipo_musica = f"nivel{nivel_numero}"
        self.reproducir_musica(tipo_musica)

    def detener_musica(self):
        """Detiene la música actual"""
        if self.habilitado and self.inicializado and pygame.mixer.get_init():
            pygame.mixer.music.stop()
            self.musica_actual = None

    def pausar_musica(self):
        """Pausa la música actual"""
        if self.habilitado and self.inicializado and pygame.mixer.get_init():
            pygame.mixer.music.pause()

    def reanudar_musica(self):
        """Reanuda la música"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.unpause()

    def cambiar_volumen_musica(self, volumen):
        """Cambia el volumen de la música (0.0 a 1.0)"""
        self.volumen_musica = max(0.0, min(1.0, volumen))
        if self.habilitado and self.inicializado:
            pygame.mixer.music.set_volume(self.volumen_musica)

    def cambiar_volumen_efectos(self, volumen):
        """Cambia el volumen de efectos (0.0 a 1.0)"""
        self.volumen_efectos = max(0.0, min(1.0, volumen))
        for sonido in self.efectos_cargados.values():
            sonido.set_volume(self.volumen_efectos)

    def limpiar(self):
        """Limpia recursos de audio"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.stop()
            for sonido in self.efectos_cargados.values():
                sonido.stop()
            self.efectos_cargados.clear()

        self.musica_actual = None

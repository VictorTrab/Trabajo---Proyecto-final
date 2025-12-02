"""
Sistema de Audio Simple
Solo maneja música de fondo y efectos básicos
"""

import pygame
from pathlib import Path


class AudioSimple:
    """Clase simple para manejar audio del juego"""

    def __init__(self):
        """Inicializa el sistema de audio simple"""
        self.habilitado = True
        self.inicializado = False

        # Volúmenes
        self.volumen_musica = 0.5
        self.volumen_efectos = 0.7

        # Estado
        self.musica_actual = None

        # Rutas de música
        self.rutas_musica = {
            "menu": "songs/SongMenu.mp3",
            "juego": "songs/SongFacil.mp3",
            "completado": "songs/SongGameStart.mp3",
            "game_over": "songs/SongGameOver.mp3",
        }

        # Rutas de efectos
        self.rutas_efectos = {
            "click": "songs/SongClick.mp3",
            "rotar": "songs/SongRotarFigura.mp3",
            "colocar": "songs/SongClick.mp3",
            "error": "songs/SongColisionBordeVentana.mp3",
        }

        # Caché de efectos cargados
        self.efectos_cargados = {}

        # Inicializar pygame.mixer
        self._inicializar()

    def _inicializar(self):
        """Inicializa pygame.mixer"""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

            pygame.mixer.music.set_volume(self.volumen_musica)
            self.inicializado = True
            print("[AudioSimple] Sistema de audio inicializado")
        except pygame.error as e:
            print(f"[AudioSimple] Error al inicializar audio: {e}")
            self.habilitado = False

    def _verificar_archivo(self, ruta):
        """Verifica si existe un archivo"""
        return Path(ruta).exists()

    def reproducir_musica(self, tipo):
        """
        Reproduce música de fondo

        Args:
            tipo: Tipo de música ("menu", "juego", "completado", "game_over")
        """
        if not self.habilitado or not self.inicializado:
            return

        # Si ya está sonando esta música, no hacer nada
        if self.musica_actual == tipo and pygame.mixer.music.get_busy():
            return

        ruta = self.rutas_musica.get(tipo)
        if not ruta or not self._verificar_archivo(ruta):
            return

        try:
            # Detener música actual
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.time.wait(50)

            # Cargar y reproducir
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1)  # Loop infinito
            pygame.mixer.music.set_volume(self.volumen_musica)

            self.musica_actual = tipo
        except pygame.error as e:
            print(f"[AudioSimple] Error al reproducir música: {e}")

    def reproducir_efecto(self, nombre):
        """
        Reproduce un efecto de sonido

        Args:
            nombre: Nombre del efecto ("click", "rotar", "colocar", "error")
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
            except pygame.error:
                return

        try:
            sonido.play()
        except pygame.error:
            pass

    def detener_musica(self):
        """Detiene la música actual"""
        if self.habilitado and self.inicializado:
            pygame.mixer.music.stop()
            self.musica_actual = None

    def pausar_musica(self):
        """Pausa la música"""
        if self.habilitado and self.inicializado:
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

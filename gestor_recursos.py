import pygame


class AssetManager:
    """Gestor centralizado de recursos (fuentes, imagenes, sonidos)"""

    _fonts = {}

    @staticmethod
    def get_font(size):
        """Obtiene una fuente de tamano especifico, cargandola si es necesario"""
        if size not in AssetManager._fonts:
            AssetManager._fonts[size] = pygame.font.Font(None, size)
        return AssetManager._fonts[size]

    @staticmethod
    def clear():
        """Limpia la cache de recursos"""
        AssetManager._fonts.clear()

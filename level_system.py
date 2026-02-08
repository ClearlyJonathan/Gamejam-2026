import pygame
from ldtk import Ldtk

class LevelSystem:
    def __init__(self, project_file, tileset_path):
        
        self.project = Ldtk.from_file(project_file)
        self.tileset = pygame.image.load(tileset_path).convert_alpha()

        self.tile_size = 16
        self.current_level = None

    def load_level(self, level_name):

        for level in self.project.levels:
            if level.identifier == level_name:
                self.current_level = level
                return
            
#        raise ValueError(f"Level '{level_name}' not found")

    def draw(self, surface):
        
        if not self.current_level:
            return
        
        for layer in self.current_level.layers:
            
            if not layer.tiles:
                continue

            for tile in layer.tiles:

                x, y = tile.px
                src_x, src_y = tile.src

                rect = pygame.Rect(
                    src_x,
                    src_y,
                    self.tile_size,
                    self.tile_size
                )

                surface.blit(self.tileset, (x, y), rect)
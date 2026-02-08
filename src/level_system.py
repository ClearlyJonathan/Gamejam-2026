import json
import pygame

#Laster in LDtk prosjektfil og laster alle levler.
#Tegner tiles på skjermen

import json
import pygame


class LevelSystem:

    def __init__(self, tileset_path):

        self.tileset = pygame.image.load(tileset_path).convert_alpha()
        self.current_level = None
        self.tile_size = 64

    def load_level(self, level_file):

        with open(level_file, "r", encoding="utf-8") as f:
            self.current_level = json.load(f)

    def draw(self, surface):

        if not self.current_level:
            return

        layers = self.current_level.get("layerInstances", [])

        for layer in layers:

            tiles = (
                layer.get("gridTiles")
                or layer.get("autoLayerTiles")
                or []
            )

            for tile in tiles:

                x, y = tile["px"]
                src_x, src_y = tile["src"]

                rect = pygame.Rect(
                    src_x,
                    src_y,
                    self.tile_size,
                    self.tile_size
                )

                surface.blit(self.tileset, (x, y), rect)

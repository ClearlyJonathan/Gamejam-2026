import json
import os
import pygame


class LevelSystem:

    def __init__(self, project_file, tileset_path):

        with open(project_file, "r", encoding="utf-8") as f:
            self.project = json.load(f)

        self.project_dir = os.path.dirname(project_file)

        self.tileset = pygame.image.load(tileset_path).convert_alpha()

        self.level_index = 0
        self.current_level = None
        self.tile_size = 64
        
    def load_level(self, index):
        level_meta = self.project["levels"][index]

        # Sjekk om nivået er eksternt
        if self.project.get("externalLevels", False) and level_meta.get("externalRelPath"):
            rel = level_meta["externalRelPath"]
            path = os.path.join(self.project_dir, rel)
            print("Loading external level:", path)
            with open(path, "r", encoding="utf-8") as f:
                self.current_level = json.load(f)
        else:
            print("Loading internal level:", level_meta["identifier"])
            # Kopier nivået og sett layerInstances til tom liste hvis det er None
            self.current_level = level_meta.copy()
            if self.current_level["layerInstances"] is None:
                self.current_level["layerInstances"] = []

        self.level_index = index



    def next_level(self):

        self.level_index += 1

        if self.level_index >= len(self.project["levels"]):
            self.level_index = 0

        self.load_level(self.level_index)

    def draw(self, surface):

        if not self.current_level:
            return

        for layer in self.current_level["layerInstances"]:

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

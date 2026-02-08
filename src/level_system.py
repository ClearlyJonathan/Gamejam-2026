# src/level_system.py
import os
import json
import pygame


class LevelSystem:
    def __init__(self, project_file, tileset_path):
        with open(project_file, "r", encoding="utf-8") as f:
            self.project = json.load(f)

        self.project_dir = os.path.dirname(project_file)
        self.tileset = pygame.image.load(tileset_path).convert_alpha()

        self.current_level = None

    def load_level(self, level_name):
        print("Available levels:")
        for lvl in self.project["levels"]:
            print(lvl["identifier"])

        for lvl in self.project["levels"]:
            if lvl["identifier"] == level_name:
                ext = lvl.get("externalRelPath")
                if ext:
                    path = os.path.join(self.project_dir, ext)
                    with open(path, "r", encoding="utf-8") as f:
                        self.current_level = json.load(f)
                else:
                    self.current_level = lvl
                return

        raise ValueError(f"Level '{level_name}' not found")

    def draw(self, surface):
        if not self.current_level:
            return

        layers = self.current_level.get("layerInstances", [])

        for layer in layers:
            layer_name = layer.get("__identifier")

            if layer.get("__identifier") == "StretchTerrain":
                continue

            tile_size = layer["__gridSize"]
            tiles = layer.get("gridTiles") or layer.get("autoLayerTiles") or []

            for tile in tiles:
                x, y = tile["px"]
                src_x, src_y = tile["src"]

                src_rect = pygame.Rect(src_x, src_y, tile_size, tile_size)
                surface.blit(self.tileset, (x, y), src_rect)

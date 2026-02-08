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
        
        # Check if this is a project file or a standalone level file
        self.is_standalone_level = "layerInstances" in self.project

    def load_level(self, level_name):
        # If it's a standalone level file, just use it directly
        if self.is_standalone_level:
            self.current_level = self.project
            print(f"Loaded standalone level: {self.project.get('identifier', 'Unknown')}")
            return
        
        # Otherwise, search through the levels array in the project
        print("Available levels:")
        for lvl in self.project["levels"]:
            print(lvl["identifier"])

        for lvl in self.project["levels"]:
            if lvl["identifier"] == level_name:
                ext = lvl.get("externalRelPath")
                if ext:
                    path = os.path.join(self.project_dir, ext)
                    # Try to load external file, but fall back to map files if it doesn't exist
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            self.current_level = json.load(f)
                        print(f"✓ Loaded external level: {level_name}")
                        return
                    except FileNotFoundError:
                        print(f"⚠ External file not found: {path}")
                        # Fall back to corresponding map file
                        if "World_Level_1" in level_name:
                            fallback_path = os.path.join(self.project_dir, "map1.json")
                        elif "World_Level_2" in level_name:
                            fallback_path = os.path.join(self.project_dir, "map2.json")
                        else:
                            fallback_path = None
                        
                        if fallback_path and os.path.exists(fallback_path):
                            print(f"  → Falling back to: {fallback_path}")
                            with open(fallback_path, "r", encoding="utf-8") as f:
                                fallback_project = json.load(f)
                                # Use the level from the fallback file
                                self.current_level = fallback_project
                                return
                        else:
                            raise FileNotFoundError(f"Level '{level_name}' not found and no fallback available")
                else:
                    self.current_level = lvl
                    print(f"✓ Loaded embedded level: {level_name}")
                    return

        raise ValueError(f"Level '{level_name}' not found")

    def draw(self, surface):
        if not self.current_level:
            return

        layers = self.current_level.get("layerInstances", [])

        for layer in layers:
            layer_name = layer.get("__identifier")

            # Skip the stretchable layer - it's drawn via world.drawables
            if layer_name == "Tiles":
                continue

            tile_size = layer["__gridSize"]
            tiles = layer.get("gridTiles") or layer.get("autoLayerTiles") or []

            for tile in tiles:
                x, y = tile["px"]
                src_x, src_y = tile["src"]

                src_rect = pygame.Rect(src_x, src_y, tile_size, tile_size)
                surface.blit(self.tileset, (x, y), src_rect)

# src/ldtk_collision_builder.py
import pygame
from collections import deque
from src.objects import Wall, StretchGroup


def _build_stretch_groups(level_system, layer):
    tile_size = layer["__gridSize"]
    tiles = layer.get("gridTiles") or layer.get("autoLayerTiles") or []

    # map grid cell -> tile
    tile_map = {}
    for t in tiles:
        px, py = t["px"]
        tx, ty = px // tile_size, py // tile_size
        tile_map[(tx, ty)] = t

    visited = set()
    groups = []

    def neighbors(c):
        x, y = c
        return ((x+1,y), (x-1,y), (x,y+1), (x,y-1))

    for start in tile_map:
        if start in visited:
            continue

        # flood-fill connected component
        q = deque([start])
        visited.add(start)
        component = []

        while q:
            c = q.popleft()
            component.append(c)
            for nb in neighbors(c):
                if nb in tile_map and nb not in visited:
                    visited.add(nb)
                    q.append(nb)

        # bounding box (grid)
        xs = [c[0] for c in component]
        ys = [c[1] for c in component]
        min_tx, max_tx = min(xs), max(xs)
        min_ty, max_ty = min(ys), max(ys)

        # bounding box (pixels)
        min_px = min_tx * tile_size
        min_py = min_ty * tile_size
        w = (max_tx - min_tx + 1) * tile_size
        h = (max_ty - min_ty + 1) * tile_size

        rect = pygame.Rect(min_px, min_py, w, h)

        # bake tiles into one surface
        base = pygame.Surface((w, h), pygame.SRCALPHA)
        for (tx, ty) in component:
            t = tile_map[(tx, ty)]
            src_x, src_y = t["src"]

            tile_img = level_system.tileset.subsurface(
                pygame.Rect(src_x, src_y, tile_size, tile_size)
            )
            dx = tx * tile_size - min_px
            dy = ty * tile_size - min_py
            base.blit(tile_img, (dx, dy))

        groups.append(StretchGroup(rect, base))

    return groups


def build_ldtk_collision(world, level_system):
    level = level_system.current_level
    if not level:
        return

    for layer in level.get("layerInstances", []):
        name = layer["__identifier"]
        layer_id = layer.get("layerDefUid")

        # -------------------------------
        # Stretchable terrain layer (ID: 112)
        # -------------------------------
        if name == "StretchTerrain":  # Only the "StretchTerrain" layer is stretchable
            groups = _build_stretch_groups(level_system, layer)
            print(f"Layer '{name}' (ID: {layer_id}): found {len(groups)} stretchable groups")
            for group in groups:
                world.add_drawable(group)   # selectable + stretchable
                world.add_solid(group)      # one big rect collider
            continue

        # Non-stretchable layers are skipped (they stay in level_system.draw)

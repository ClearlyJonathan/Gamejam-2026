from src.objects import Wall


def build_ldtk_collision(world, level_system):

    level = level_system.current_level
    if not level:
        return []

    spawn_positions = []

    for layer in level.get("layerInstances", []):

        name = layer["__identifier"]

        # velg hvilke layers som skal gi collision
        if name not in ("Collision", "StretchTerrain", "Door", "Killer"):
            continue

        # stretch flag
        stretchable = name == "StretchTerrain"

        tile_size = layer["__gridSize"]

        tiles = (
            layer.get("gridTiles")
            or layer.get("autoLayerTiles")
            or []
        )

        # Spawn layer: collect player spawn positions
        if name == "Spawn":
            for tile in tiles:
                x, y = tile["px"]
                spawn_positions.append((x, y))
            continue

        for tile in tiles:
            x, y = tile["px"]

            wall = Wall(x, y, tile_size, tile_size)

            world.add_solid(wall)

            # stretchable terrain must be drawable/selectable
            if stretchable:
                world.add_drawable(wall)
    return spawn_positions

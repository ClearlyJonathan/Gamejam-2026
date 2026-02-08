from src.objects import Wall


def build_ldtk_collision(world, level_system):

    level = level_system.current_level
    if not level:
        return

    for layer in level.get("layerInstances", []):

        name = layer["__identifier"]

        # velg hvilke layers som skal gi collision
        if name not in ("Collision", "StretchTerrain"):
            continue

        # stretch flag
        stretchable = name == "StretchTerrain"

        tile_size = layer["__gridSize"]

        tiles = (
            layer.get("gridTiles")
            or layer.get("autoLayerTiles")
            or []
        )

        for tile in tiles:

            x, y = tile["px"]

            wall = Wall(x, y, tile_size, tile_size)

            world.add_solid(wall)

            # stretchable terrain må være drawable
            if stretchable:
                world.add_drawable(wall)

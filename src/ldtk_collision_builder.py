from src.objects import Wall

def build_ldtk_collision(world, level_system):
    level = level_system.current_level
    if not level:
        return
    
    #henter tilesize definert i levelsystem
    tile_size = level_system.tile_size

    for layer in level.get("layerInstances",[]):
        
        name = layer["__identifier"]

        #Stretchable tiles
        if name == "StrechTerrain":
            strechable = True

        #Vanlige tiles
        elif name == "Collision":
            stretchable = False

        else:
            continue

        tiles = (layer.get("gritTiles") or layer.get("autoLayerTiles") or [])

        for tile in tiles:
            
            x,y = tile["px"]

            wall = Wall(x, y, tile_size, tile_size)

            world.add_solid(wall)

            if stretchable:
                world.add_drawable(wall)


    

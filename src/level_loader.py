from src.objects import Wall

def build_test_level(world):
    walls = [
        Wall(300, 150, 200, 40),
        Wall(200, 350, 400, 40),
        Wall(100, 200, 40, 250),
    ]

    for wall in walls:
        world.solids.append(wall)   # player collides with these

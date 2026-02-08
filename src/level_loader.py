import pygame
from src.objects import Wall

def build_test_level(world):
    # ground (as a Wall object so you can stretch it too)
    ground = Wall(0, world.height - 80, world.width, 80)
    world.add_solid(ground)
    world.add_drawable(ground)

    # some blocks
    blocks = [
        Wall(300, 150, 220, 45),
        Wall(220, 360, 420, 55),
        Wall(100, 220, 45, 260),
        Wall(700, 260, 240, 45),
    ]

    for b in blocks:
        world.add_solid(b)
        world.add_drawable(b)

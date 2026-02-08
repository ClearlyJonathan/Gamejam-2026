### Here we put what objects are collidable

import pygame

class World:
    def __init__(self, width: int, height: int, gravity: float = 1800.0):
        self.width = width
        self.height = height
        self.gravity = gravity

        self.solids: list[pygame.Rect] = []   # things that block movement
        self.triggers = []                    # things that overlap (optional)
        self.entities = []                    # enemies/npcs (optional)

    def add_solid(self, rect_or_obj):
        # Accept either pygame.Rect or object with .rect
        r = rect_or_obj.rect if hasattr(rect_or_obj, "rect") else rect_or_obj
        self.solids.append(r)

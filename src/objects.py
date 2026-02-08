import pygame

GRAY = (120, 120, 120)

# Here we define our objects. You can just copy paste the class wall and rename it 

class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)

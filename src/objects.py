import pygame

GRAY = (120, 120, 120)

class Wall:
    """Basic terrain block: has a rect + can draw itself."""
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

        # minimum size so you can’t invert it into negative sizes
        self.min_w = 16
        self.min_h = 16

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

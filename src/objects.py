# src/objects.py
import pygame

GRAY = (120, 120, 120)


class Wall:
    """Basic terrain block: has a rect + can draw itself (debug)."""
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_w = 16
        self.min_h = 16

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)


class StretchGroup:
    """
    ONE clickable/stretchable object made from a connected chunk of tiles.
    - rect is used for clicking + stretching
    - base_surface is the baked sprite of the whole chunk at original size
    - draw() scales base_surface to rect.size
    """
    def __init__(self, rect: pygame.Rect, base_surface: pygame.Surface):
        self.rect = rect

        self.min_w = 16
        self.min_h = 16

        self.base_surface = base_surface.convert_alpha()
        self._cached_size = (rect.w, rect.h)
        self._scaled = pygame.transform.scale(self.base_surface, self._cached_size)

    def draw(self, screen: pygame.Surface):
        size = (self.rect.w, self.rect.h)
        if size != self._cached_size:
            self._cached_size = size
            self._scaled = pygame.transform.scale(self.base_surface, size)
        screen.blit(self._scaled, self.rect.topleft)

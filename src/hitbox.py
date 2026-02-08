import pygame

# Dillu code but made it into a class so that anything can have Hitbox easily?

class Hitbox:
    def __init__(self, x, y, w, h, offset=(0, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.offset = pygame.Vector2(offset)

    def move_and_collide(self, dx, dy, solids):
        collisions = {"left": False, "right": False, "top": False, "bottom": False}
        solid_rects = [s.rect if hasattr(s, "rect") else s for s in solids]
        
        # --- X axis ---
        self.rect.x += dx
        for r in solid_rects:
            if self.rect.colliderect(r):
                if dx > 0:
                    self.rect.right = r.left
                    collisions["right"] = True
                elif dx < 0:
                    self.rect.left = r.right
                    collisions["left"] = True

        # --- Y axis ---
        self.rect.y += dy
        for r in solid_rects:
            if self.rect.colliderect(r):
                if dy > 0:
                    self.rect.bottom = r.top
                    collisions["bottom"] = True
                elif dy < 0:
                    self.rect.top = r.bottom
                    collisions["top"] = True

        return collisions

    def sync_owner_rect(self, owner_rect: pygame.Rect):
        """
        Places the owner's rect relative to hitbox rect using the offset.
        If your hitbox is inset inside the sprite, offset should be negative.
        """
        owner_rect.topleft = (self.rect.x + self.offset.x, self.rect.y + self.offset.y)

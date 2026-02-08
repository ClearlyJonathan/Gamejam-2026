import pygame

class Stretcher:
    """
    Resize the selected object (anything with .rect).
    Controls:
      - Q / E: left / right edge
      - Z / C: top / bottom edge
      - Shift: invert (shrink instead of grow)
      - Click: select
    """
    def __init__(self, speed: int = 5):
        self.speed = speed
        self.target = None

    def select(self, obj):
        self.target = obj

    def select_at_point(self, targets, pos):
        # last drawn should be considered "top-most"
        for t in reversed(targets):
            if hasattr(t, "rect") and t.rect.collidepoint(pos):
                self.target = t
                return t
        return None

    def update(self, keys):
        if not self.target:
            return None

        rect = self.target.rect
        min_w = getattr(self.target, "min_w", 1)
        min_h = getattr(self.target, "min_h", 1)

        # either shift key = shrink mode
        shrink = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        before = rect.copy()

        left_delta   = +self.speed if shrink else -self.speed
        right_delta  = -self.speed if shrink else +self.speed
        top_delta    = +self.speed if shrink else -self.speed
        bottom_delta = -self.speed if shrink else +self.speed

        if keys[pygame.K_q]:
            rect.update(self._resize_left(rect, left_delta, min_w))
        if keys[pygame.K_e]:
            rect.update(self._resize_right(rect, right_delta, min_w))
        if keys[pygame.K_z]:
            rect.update(self._resize_top(rect, top_delta, min_h))
        if keys[pygame.K_c]:
            rect.update(self._resize_bottom(rect, bottom_delta, min_h))

        if rect != before:
            return "shrink" if shrink else "stretch"
        return None


    def draw_gizmo(self, screen):
        if self.target:
            pygame.draw.rect(screen, (255, 255, 255), self.target.rect, 2)

    @staticmethod
    def _resize_left(r: pygame.Rect, delta: int, min_w: int):
        out = r.copy()
        new_x = out.x + delta
        new_w = out.width - delta
        if new_w < min_w:
            right = out.right
            new_w = min_w
            new_x = right - new_w
        out.x, out.width = new_x, new_w
        return out

    @staticmethod
    def _resize_right(r: pygame.Rect, delta: int, min_w: int):
        out = r.copy()
        out.width = max(min_w, out.width + delta)
        return out

    @staticmethod
    def _resize_top(r: pygame.Rect, delta: int, min_h: int):
        out = r.copy()
        new_y = out.y + delta
        new_h = out.height - delta
        if new_h < min_h:
            bottom = out.bottom
            new_h = min_h
            new_y = bottom - new_h
        out.y, out.height = new_y, new_h
        return out

    @staticmethod
    def _resize_bottom(r: pygame.Rect, delta: int, min_h: int):
        out = r.copy()
        out.height = max(min_h, out.height + delta)
        return out

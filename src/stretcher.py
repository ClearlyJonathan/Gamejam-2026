import pygame

class Resizable:
    def __init__(self, rect: pygame.Rect, min_w=1, min_h=1):
        self.rect = rect
        self.min_w = min_w
        self.min_h = min_h



class NineSlice:
    """
    9-slice renderer.
    - border: pixel thickness of the corners/edges
    - tile: if True, tile edges/center; if False, stretch them
    """

    def __init__(self, image: pygame.Surface | str, border: int, tile: bool = True):
        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        else:
            self.image = image.convert_alpha()

        self.border = int(border)
        self.tile = bool(tile)

        iw, ih = self.image.get_size()
        if iw < self.border * 2 or ih < self.border * 2:
            raise ValueError("border is too large for the source image.")

        self._slices = self._slice_9(self.image, self.border)

    @property
    def min_size(self) -> tuple[int, int]:
        # minimum drawable size so corners don't overlap
        m = self.border * 2 + 1
        return (m, m)

    def draw(self, dst: pygame.Surface, rect: pygame.Rect):
        x, y, w, h = rect
        min_w, min_h = self.min_size
        w = max(w, min_w)
        h = max(h, min_h)

        s = self._slices
        b = self.border

        # corners
        dst.blit(s["tl"], (x, y))
        dst.blit(s["tr"], (x + w - b, y))
        dst.blit(s["bl"], (x, y + h - b))
        dst.blit(s["br"], (x + w - b, y + h - b))

        # edges + center
        if self.tile:
            self._blit_tile(dst, s["top"],    pygame.Rect(x + b, y,         w - 2*b, b))
            self._blit_tile(dst, s["bottom"], pygame.Rect(x + b, y + h - b, w - 2*b, b))
            self._blit_tile(dst, s["left"],   pygame.Rect(x,     y + b,     b,       h - 2*b))
            self._blit_tile(dst, s["right"],  pygame.Rect(x + w - b, y + b, b,       h - 2*b))
            self._blit_tile(dst, s["center"], pygame.Rect(x + b, y + b,     w - 2*b, h - 2*b))
        else:
            # stretch instead of tile
            dst.blit(pygame.transform.scale(s["top"],    (w - 2*b, b)),       (x + b, y))
            dst.blit(pygame.transform.scale(s["bottom"], (w - 2*b, b)),       (x + b, y + h - b))
            dst.blit(pygame.transform.scale(s["left"],   (b, h - 2*b)),       (x, y + b))
            dst.blit(pygame.transform.scale(s["right"],  (b, h - 2*b)),       (x + w - b, y + b))
            dst.blit(pygame.transform.scale(s["center"], (w - 2*b, h - 2*b)), (x + b, y + b))

    @staticmethod
    def _slice_9(image: pygame.Surface, b: int) -> dict[str, pygame.Surface]:
        w, h = image.get_size()
        return {
            "tl": image.subsurface((0, 0, b, b)),
            "tr": image.subsurface((w - b, 0, b, b)),
            "bl": image.subsurface((0, h - b, b, b)),
            "br": image.subsurface((w - b, h - b, b, b)),
            "top": image.subsurface((b, 0, w - 2*b, b)),
            "bottom": image.subsurface((b, h - b, w - 2*b, b)),
            "left": image.subsurface((0, b, b, h - 2*b)),
            "right": image.subsurface((w - b, b, b, h - 2*b)),
            "center": image.subsurface((b, b, w - 2*b, h - 2*b)),
        }

    @staticmethod
    def _blit_tile(dst: pygame.Surface, tile: pygame.Surface, dst_rect: pygame.Rect):
        x0, y0, w, h = dst_rect
        if w <= 0 or h <= 0:
            return

        tw, th = tile.get_size()
        if tw <= 0 or th <= 0:
            return

        y = y0
        while y < y0 + h:
            x = x0
            blit_h = min(th, (y0 + h) - y)
            while x < x0 + w:
                blit_w = min(tw, (x0 + w) - x)
                if blit_w != tw or blit_h != th:
                    dst.blit(tile, (x, y), area=pygame.Rect(0, 0, blit_w, blit_h))
                else:
                    dst.blit(tile, (x, y))
                x += tw
            y += th


    """
    A tool/controller that resizes the currently selected target (any object with .rect).
    Controls:
      - Q/E: left/right edge
      - Z/C: top/bottom edge
      - Shift: invert (shrink instead of grow)
      - Mouse click: select target under cursor (optional helper)
    """
    def __init__(self, speed: int = 5):
        self.speed = speed
        self.target = None  # object with .rect

    def select(self, target):
        self.target = target

    def select_at_point(self, targets, pos):
        """Pick the top-most target under the mouse."""
        for t in reversed(targets):
            if t.rect.collidepoint(pos):
                self.target = t
                return t
        return None

    def update(self, keys):
        if not self.target:
            return

        r = self.target.rect
        min_w = getattr(self.target, "min_w", 1)
        min_h = getattr(self.target, "min_h", 1)

        shrink = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        # same delta logic you had
        left_delta   = +self.speed if shrink else -self.speed
        right_delta  = -self.speed if shrink else +self.speed
        top_delta    = +self.speed if shrink else -self.speed
        bottom_delta = -self.speed if shrink else +self.speed

        if keys[pygame.K_q]:
            self.target.rect = self._resize_left(r, left_delta, min_w)
        if keys[pygame.K_e]:
            self.target.rect = self._resize_right(r, right_delta, min_w)
        if keys[pygame.K_z]:
            self.target.rect = self._resize_top(r, top_delta, min_h)
        if keys[pygame.K_c]:
            self.target.rect = self._resize_bottom(r, bottom_delta, min_h)

    def draw_gizmo(self, surface):
        """Draw a highlight around the selected target."""
        if not self.target:
            return
        pygame.draw.rect(surface, (255, 255, 255), self.target.rect, 2)

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
    

    class UIPanel:
        def __init__(self, rect, skin):
            self.rect = rect
            self.skin = skin
            self.min_w, self.min_h = skin.min_size  # so corners never overlap

        def draw(self, screen):
            self.skin.draw(screen, self.rect)

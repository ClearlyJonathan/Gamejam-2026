# src/menu.py
import pygame

_BG_IMAGE = None
_BG_PATH = "assets/menu background.png"  # change if needed


# Music shit
pygame.mixer.init()



def _get_bg(screen: pygame.Surface) -> pygame.Surface:
    """Lazy-load + cache background after display is initialized."""
    global _BG_IMAGE
    if _BG_IMAGE is None:
        img = pygame.image.load(_BG_PATH)
        img = pygame.transform.scale(img, screen.get_size())
        _BG_IMAGE = img.convert()  # display is initialized by the time we call this
    return _BG_IMAGE


class _Menu:
    def __init__(self, title: str, items: list[tuple[str, str]]):
        # items: [(label, result_key), ...]
        self.title = title
        self.items = items
        self.selected = 0

        self.font_title = pygame.font.Font(None, 80)
        self.font_item = pygame.font.Font(None, 46)
        self.font_hint = pygame.font.Font(None, 28)

    def move(self, direction: int):
        self.selected = (self.selected + direction) % len(self.items)

    def current_result(self) -> str:
        return self.items[self.selected][1]

    def draw(self, screen: pygame.Surface, hint_text: str):
        w, h = screen.get_size()
        cx = w // 2

        # background
        screen.blit(_get_bg(screen), (0, 0))

        # dark overlay for readability
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        # title
        title_surf = self.font_title.render(self.title, True, (245, 245, 245))
        title_rect = title_surf.get_rect(center=(cx, h // 2 - 170))
        screen.blit(title_surf, title_rect)

        # items
        start_y = h // 2 - 40
        for i, (label, _) in enumerate(self.items):
            is_sel = (i == self.selected)
            color = (255, 255, 255) if is_sel else (170, 170, 170)
            prefix = "> " if is_sel else "  "
            surf = self.font_item.render(prefix + label, True, color)
            rect = surf.get_rect(center=(cx, start_y + i * 56))
            screen.blit(surf, rect)

        # hint
        hint_surf = self.font_hint.render(hint_text, True, (140, 140, 140))
        hint_rect = hint_surf.get_rect(center=(cx, h - 40))
        screen.blit(hint_surf, hint_rect)


def run_menu(screen: pygame.Surface, clock: pygame.time.Clock, title: str = "Suck and Blow") -> str:
    """
    Main menu (blocking). Returns: "start" | "quit"
    """
    menu = _Menu(title, [
        ("Start", "start"),
        ("Quit", "quit"),
    ])

    hint = "↑/↓ select   Enter confirm   Esc quit"

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.move(-1)
                elif event.key == pygame.K_DOWN:
                    menu.move(+1)
                elif event.key == pygame.K_RETURN:
                    return menu.current_result()
                elif event.key == pygame.K_ESCAPE:
                    return "quit"

        menu.draw(screen, hint)
        pygame.display.flip()


def run_pause_menu(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """
    Pause menu (blocking). Returns:
      - "resume"  (go back to game)
      - "menu"    (quit to main menu)
      - "quit"    (exit game)
    """
    menu = _Menu("Paused", [
        ("Resume", "resume"),
        ("Quit to Menu", "menu"),
        ("Quit Game", "quit"),
    ])

    hint = "↑/↓ select   Enter confirm   Esc resume"

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.move(-1)
                elif event.key == pygame.K_DOWN:
                    menu.move(+1)
                elif event.key == pygame.K_RETURN:
                    return menu.current_result()
                elif event.key == pygame.K_ESCAPE:
                    return "resume"

        menu.draw(screen, hint)
        pygame.display.flip()

# level_transition.py
import pygame

def run_transition(screen, clock, image_path="next_level.png", duration=2.0):
    """
    Viser en transition med et bilde.
    image_path: Filen som skal vises (bruk start-image eller next-level-image)
    duration: Hvor lenge den vises i sekunder
    """
    # Last inn bildet
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
    rect = image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    timer = 0
    while timer < duration:
        dt = clock.tick(60) / 1000.0
        timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill((0, 0, 0))
        screen.blit(image, rect)
        pygame.display.flip()

    return True

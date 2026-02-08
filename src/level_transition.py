
import pygame


def run_transition(screen, clock):

    font = pygame.font.Font(None, 80)
    text = font.render("NEXT LEVEL", True, (255, 255, 255))

    timer = 0

    while timer < 2.0:

        dt = clock.tick(60) / 1000.0
        timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill((0, 0, 0))
        screen.blit(text, (400, 300))

        pygame.display.flip()

    return True

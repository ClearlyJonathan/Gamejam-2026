import pygame

def run_transition(screen, clock):
    # Last inn bildet du vil vise som "Next Level"
    next_level_image = pygame.image.load("assets/menu background.png").convert_alpha()
    
    # Hent størrelsen på bildet for å sentrere det
    image_rect = next_level_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    timer = 0

    while timer < 2.0:
        dt = clock.tick(60) / 1000.0
        timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill((0, 0, 0))  # Bakgrunn
        screen.blit(next_level_image, image_rect)  # Tegn bildet

        pygame.display.flip()

    return True

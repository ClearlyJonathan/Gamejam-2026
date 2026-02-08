import pygame

# Player A
jump_a  = pygame.mixer.Sound("assets/sounds/jump.mp3")
hit_a   = pygame.mixer.Sound("assets/sounds/damage.wav")
death_a = pygame.mixer.Sound("assets/sounds/death.mp3")

# Player B
jump_b  = pygame.mixer.Sound("assets/sounds/jump.mp3")
hit_b   = pygame.mixer.Sound("assets/sounds/damage.wav")
death_b = pygame.mixer.Sound("assets/sounds/death.mp3")

jump_a.set_volume(0.4)
hit_a.set_volume(0.5)
death_a.set_volume(0.7)

jump_b.set_volume(0.4)
hit_b.set_volume(0.5)
death_b.set_volume(0.7)

import pygame
from level_system import LevelSystem
import src.playercontroller


# pygame setup do not touch - Just temporarily so i can see my playerr
pygame.init()
W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Suck and blow")
running = True
dt = 0
FPS = 60
GROUND_Y = 600

# Don't touch player controller, just modify from here if needed.
src.playercontroller.W = W
src.playercontroller.H = H
src.playercontroller.GROUND_Y = GROUND_Y
src.playercontroller.GRAVITY = 1800
#playerA = src.playercontroller.playerA
#playerB = src.playercontroller.playerB



#midlertidig for playtesting
playerA = src.playercontroller.Player(
    100, 100,
    (200, 40, 40),
    {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w}
)
#midlertidig for playtesting
playerB = src.playercontroller.Player(
    300, 100,
    (40, 40, 200),
    {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP}
)

#Starte/Loade levelsene:
levels = LevelSystem(
    "ldtk.json",
    "assets/tilesetResize.png")

#Laster første level
levels.load_level("Level_0")

running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Input + friction handling ---
    # Player A
    playerA.handle_input(keys, dt)
    if not (keys[playerA.controls["left"]] or keys[playerA.controls["right"]]):
        playerA.apply_friction(dt)

    # Player B
    playerB.handle_input(keys, dt)
    if not (keys[playerB.controls["left"]] or keys[playerB.controls["right"]]):
        playerB.apply_friction(dt)

    # --- Update physics ---
    playerA.update(dt)
    playerB.update(dt)

    # --- Draw ---
    screen.fill((20, 22, 28))

    #Renderer levelet
    levels.draw(screen)

    # ground
    pygame.draw.rect(screen, (60, 65, 75), (0, GROUND_Y, W, H - GROUND_Y))

    playerA.draw(screen)
    playerB.draw(screen)

    pygame.display.flip()

pygame.quit()
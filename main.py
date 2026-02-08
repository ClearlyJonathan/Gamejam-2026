import pygame
import src.playercontroller as pc
from src.stretcher import NineSlice
import src.world as wd
import src.level_loader as level


from level_system import LevelSystem


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
world = wd.World(W,H, 1800.0)
# Example of how to add a collidable
ground = pygame.Rect(0, GROUND_Y, W, H - GROUND_Y)
world.add_solid(ground)
level.build_test_level(world)
# Don't touch player controller, just modify from here if needed.

pc.W = W
pc.H = H
pc.GROUND_Y = GROUND_Y
pc.SHOULD_APPLY_GRAVITY = True
playerA = pc.playerA
playerB = pc.playerB



# Test
panel_skin = NineSlice("assets/brick.png", border=16, tile=True)
panel_rect = pygame.Rect(250, 160, 260, 180)

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
    playerA.update(dt, world)
    playerB.update(dt, world)

    # --- Draw ---
    screen.fill((20, 22, 28))
    for solid in world.solids:
        if hasattr(solid, "draw"):
            solid.draw(screen)
    
    panel_skin.draw(screen, panel_rect)

    #Renderer levelet
    levels.draw(screen)

    # ground
    pygame.draw.rect(screen, (60, 65, 75), (0, GROUND_Y, W, H - GROUND_Y))

    playerA.draw(screen)
    playerB.draw(screen)

    pygame.display.flip()

pygame.quit()



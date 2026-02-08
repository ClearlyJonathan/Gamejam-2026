import pygame
import src.playercontroller as pc

from src.world import World
from src.level_loader import build_test_level
from src.stretcher import Stretcher
from src.level_system import LevelSystem
from src.menu import run_menu

from src.ldtk_collision_builder import build_ldtk_collision


pygame.init()


# Music shit
pygame.mixer.init()
MENU_MUSIC = "assets/music/New Composition #1.mp3"
GAME_MUSIC = "assets/music/Jungle and Rainforest Sound Effects - Tropical Forest Ambiences from Costa Rica.mp3"
pygame.mixer.music.load(MENU_MUSIC)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)




W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Suck and blow")
FPS = 60


#Menu
choice = run_menu(screen, clock, "Suck and Blow")
if choice == "quit":
    pygame.quit()
    raise SystemExit

pygame.mixer.music.fadeout(1)
pygame.mixer.music.load(GAME_MUSIC)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


# World + level
world = World(W, H, gravity=1800.0)
#build_test_level(world)  # fills world.solids with Wall objects :contentReference[oaicite:1]{index=1}
#hei
# Make sure the same objects are drawable + selectable
# (only do this if your loader doesn't already add drawables)
for obj in world.solids:
    if obj not in world.drawables:
        world.add_drawable(obj)

GROUND_Y = 600
# Two players (from your existing file)
pc.W = W
pc.H = H
pc.GROUND_Y = GROUND_Y
pc.GRAVITY = 1800
playerA = pc.playerA
playerB = pc.playerB

# Stretch tool
stretcher = Stretcher(speed=6)

#Starte/Loade levelsene:
levels = LevelSystem(
    "map2.json",
    "assets/tilesetResizeResize.png")

#Laster fÃ¸rste level
levels.load_level("AutoLayers_advanced_demo")
build_ldtk_collision(world, levels)



running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left click to select a terrain object to stretch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            stretcher.select_at_point(world.drawables, event.pos)

    keys = pygame.key.get_pressed()

    # Stretch selected object (Q/E/Z/C + Shift)
    stretcher.update(keys)

    # Player input
    playerA.handle_input(keys, dt)
    if not (keys[playerA.controls["left"]] or keys[playerA.controls["right"]]):
        playerA.apply_friction(dt)

    playerB.handle_input(keys, dt)
    if not (keys[playerB.controls["left"]] or keys[playerB.controls["right"]]):
        playerB.apply_friction(dt)

    # Physics + collision vs world.solids (this is the important part)
    playerA.update(dt, world)  # needs update(dt, world) :contentReference[oaicite:2]{index=2}
    playerB.update(dt, world)

    # Draw
    screen.fill((20, 22, 28))

    for obj in world.drawables:
        # draw terrain blocks
        obj.draw(screen)

    # highlight selection so you know what you're stretching
    stretcher.draw_gizmo(screen)
    levels.draw(screen)

    playerA.draw(screen)
    playerB.draw(screen)

    pygame.display.flip()

pygame.quit()


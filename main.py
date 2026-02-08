import pygame
import src.playercontroller as pc

from src.world import World
from src.level_loader import build_test_level
from src.stretcher import Stretcher
from src.level_system import LevelSystem

from src.ldtk_collision_builder import build_ldtk_collision

from src.level_events import LevelEvents
from src.level_transition import run_transition


pygame.init()

W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Suck and blow")

FPS = 60

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
#pc.SHOULD_APPLY_GRAVITY = False

# Stretch tool
stretcher = Stretcher(speed=6)

#Starte/Loade levelsene:
levels = LevelSystem("assets/tilesetResizeResize.png")

level_list = [
    "src/levels/map2.json",
    "src/levels/map2.json",
]

current_level_index = 0

levels.load_level(level_list[current_level_index])

events = LevelEvents()
events.build(levels.current_level)

build_ldtk_collision(world, levels)

print(levels.current_level.keys())

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

    next_level = events.check([playerA, playerB])

    if next_level:

        if not run_transition(screen, clock):
            running = False

        current_level_index += 1

        if current_level_index >= len(level_list):
            current_level_index = 0

        world.solids.clear()
        world.drawables.clear()

        levels.load_level(level_list[current_level_index])

        events.build(levels.current_level)
        build_ldtk_collision(world, levels)
                
                
        playerA.pos.xy = (200, 200)
        playerA.hitbox.topleft = (200, 200)

        playerB.pos.xy = (400, 200)
        playerB.hitbox.topleft = (400, 200)


    # Draw
    screen.fill((20, 22, 28))

    levels.draw(screen)

    for obj in world.drawables:
        # draw terrain blocks
        obj.draw(screen)

    # highlight selection so you know what you're stretching
    stretcher.draw_gizmo(screen)

    playerA.draw(screen)
    playerB.draw(screen)

    pygame.display.flip()

pygame.quit()

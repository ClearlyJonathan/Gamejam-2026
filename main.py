import pygame

from src.world import World
from src.level_loader import build_test_level
from src.stretcher import Stretcher
from src.level_system import LevelSystem
from src.menu import run_menu

from src.ldtk_collision_builder import build_ldtk_collision

from src.level_events import LevelEvents
from src.level_transition import run_transition

from src.KillerZones import KillerZones  # <-- NY

pygame.init()
pygame.mixer.init()

import src.sound as sound
import src.playercontroller as pc

hp_font = pygame.font.Font(None, 28)

# Music
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

# Menu
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
# build_test_level(world)

for obj in world.solids:
    if obj not in world.drawables:
        world.add_drawable(obj)

GROUND_Y = 600
pc.W = W
pc.H = H
pc.GROUND_Y = GROUND_Y
pc.GRAVITY = 1800
playerA = pc.playerA
playerB = pc.playerB

stretcher = Stretcher(speed=6)

# Level system
levels = LevelSystem(
    "assets/ADAM.json",
    "assets/tilesetResizeResize.png"
)

levels.load_level(0)

events = LevelEvents()
events.build(levels.current_level)

# ---- NEW: killer zones ----
killer = KillerZones("Killer")
killer.rebuild_from_level(levels)  # bygg killer-rects fra current level

build_ldtk_collision(world, levels)

print(levels.current_level.keys())

running = True
game_over = False

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            stretcher.select_at_point(world.drawables, event.pos)

    keys = pygame.key.get_pressed()

    # Stretch selected object
    action = stretcher.update(keys)
    if action == "stretch":
        playerA.take_damage(1)
    elif action == "shrink":
        playerB.take_damage(1)

    # Player input
    playerA.handle_input(keys, dt)
    if not (keys[playerA.controls["left"]] or keys[playerA.controls["right"]]):
        playerA.apply_friction(dt)

    playerB.handle_input(keys, dt)
    if not (keys[playerB.controls["left"]] or keys[playerB.controls["right"]]):
        playerB.apply_friction(dt)

    # Physics + collision vs solids
    playerA.update(dt, world)
    playerB.update(dt, world)

    # ---- NEW: killer check (if one dies, both lose) ----
    if killer.update(dt, [playerA, playerB]):
        game_over = True
        running = False
        break

    # Door/event-based next level
    next_level = events.check([playerA, playerB])

    if next_level:
        if not run_transition(screen, clock):
            running = False
            break

        levels.next_level()

        # clear old world
        world.solids.clear()
        world.drawables.clear()
        world.triggers.clear()
        world.entities.clear()

        events.build(levels.current_level)
        build_ldtk_collision(world, levels)

        # rebuild killer zones for new level
        killer.rebuild_from_level(levels)

        # reset player positions
        playerA.pos.xy = (200, 200)
        playerA.hitbox.topleft = (200, 200)
        playerA.vel.xy = (0, 0)

        playerB.pos.xy = (200, 200)
        playerB.hitbox.topleft = (200, 200)
        playerB.vel.xy = (0, 0)

        print("Loaded level:", levels.current_level.get("identifier"))
        print("Solids:", len(world.solids))
        print("Layers:", len(levels.current_level.get("layerInstances", [])))

    # Draw
    screen.fill((20, 22, 28))

    for obj in world.drawables:
        obj.draw(screen)

    levels.draw(screen)
    stretcher.draw_gizmo(screen)

    # Optional debug: show killer tiles
    # killer.draw_debug(screen)

    playerA.draw(screen, hp_font)
    playerB.draw(screen, hp_font)

    pygame.display.flip()

pygame.quit()

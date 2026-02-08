import pygame

from src.world import World
from src.level_loader import build_test_level
from src.stretcher import Stretcher
from src.level_system import LevelSystem
from src.menu import run_menu

from src.ldtk_collision_builder import build_ldtk_collision

from src.level_events import LevelEvents
from src.level_transition import run_transition


pygame.init()
pygame.mixer.init()
import src.sound as sound
import src.playercontroller as pc
hp_font = pygame.font.Font(None, 28)
timer_font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()  # ms since pygame.init()




# Music shit
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
#pc.SHOULD_APPLY_GRAVITY = False

# Stretch tool
stretcher = Stretcher(speed=6)

#Starte/Loade levelsene:
levels = LevelSystem(
    "assets/ADAM.ldtk",
    "assets/tilesetResizeResize.png"
)

levels.load_level(0)

events = LevelEvents()
events.build(levels.current_level)

spawn_positions = build_ldtk_collision(world, levels)

# initial spawn placement: center players on spawn tiles
if len(spawn_positions) >= 2:
    ts = getattr(levels, "tile_size", 64)
    ax = spawn_positions[0][0] + ts // 2 - playerA.hitbox.width // 2
    ay = spawn_positions[0][1] + ts - playerA.hitbox.height

    bx = spawn_positions[1][0] + ts // 2 - playerB.hitbox.width // 2
    by = spawn_positions[1][1] + ts - playerB.hitbox.height

    playerA.pos.x, playerA.pos.y = ax, ay
    playerA.hitbox.topleft = (ax, ay)
    playerA.rect.topleft = playerA.hitbox.topleft

    playerB.pos.x, playerB.pos.y = bx, by
    playerB.hitbox.topleft = (bx, by)
    playerB.rect.topleft = playerB.hitbox.topleft


print(levels.current_level.keys())

running = True
# Keep track of where to respawn players
respawnA = None  # (x, y)
respawnB = None  # (x, y)

# ✅ CHANGE: set initial respawn points (so respawn works on level 0)
respawnA = (playerA.hitbox.x, playerA.hitbox.y)
respawnB = (playerB.hitbox.x, playerB.hitbox.y)

def respawn_players():
    # reset hp
    playerA.hp = playerA.max_hp
    playerB.hp = playerB.max_hp

    # reset velocity so they don't keep momentum
    playerA.vel.xy = (0, 0)
    playerB.vel.xy = (0, 0)

    # move to respawn positions
    if respawnA is not None:
        ax, ay = respawnA
        playerA.pos.xy = (ax, ay)
        playerA.hitbox.topleft = (ax, ay)
        playerA.rect.topleft = playerA.hitbox.topleft

    if respawnB is not None:
        bx, by = respawnB
        playerB.pos.xy = (bx, by)
        playerB.hitbox.topleft = (bx, by)
        playerB.rect.topleft = playerB.hitbox.topleft

    # ✅ CHANGE: removed these lines (they crash / don't work):
    # playerA.pos.x, playerA.pos.y = ax, ay
    # playerB.pos.x, playerB.pos.y = bx, by
    # respawnA = (ax, ay)
    # respawnB = (bx, by)

respawn_cooldown = 0.0


while running:
    dt = clock.tick(FPS) / 1000.0
    respawn_cooldown = max(0.0, respawn_cooldown - dt)
    if (playerA.hp == 0 or playerB.hp == 0) and respawn_cooldown == 0.0:
        respawn_players()
        respawn_cooldown = 1.0  # 1 second delay before another respawn can happen


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left click to select a terrain object to stretch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            stretcher.select_at_point(world.drawables, event.pos)

    keys = pygame.key.get_pressed()

    # Stretch selected object (Q/E/Z/C + Shift)
    action = stretcher.update(keys)

    if action == "stretch":
        playerA.take_damage(1)
    elif action == "shrink":
        playerB.take_damage(1)

    # ✅ CHANGE: removed duplicate respawn (it bypassed cooldown)
    # if playerA.hp == 0 or playerB.hp == 0:
    #     respawn_players()

    
    #print(playerA.hp)

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
    # Switch level when both are within 1 player-width of the right edge

    next_level = events.check([playerA, playerB])

        

    if next_level:
        # ✅ CHANGE: removed these lines (ax/ay might be stale here)
        # respawnA = (ax, ay)
        # respawnB = (bx, by)

        if not run_transition(screen, clock):
            running = False

        # advance to next level once
        levels.next_level()

        # clear world objects before loading the new level
        world.solids.clear()
        world.drawables.clear()
        if hasattr(world, 'triggers'):
            world.triggers.clear()

        events.build(levels.current_level)
        spawn_positions = build_ldtk_collision(world, levels)

        # center players on the new level's spawn tiles if available
        if len(spawn_positions) >= 2:
            ts = getattr(levels, "tile_size", 64)
            ax = spawn_positions[0][0] + ts // 2 - playerA.hitbox.width // 2
            ay = spawn_positions[0][1] + ts - playerA.hitbox.height

            bx = spawn_positions[1][0] + ts // 2 - playerB.hitbox.width // 2
            by = spawn_positions[1][1] + ts - playerB.hitbox.height

            playerA.pos.x, playerA.pos.y = ax, ay
            playerA.hitbox.topleft = (ax, ay)
            playerA.rect.topleft = playerA.hitbox.topleft

            playerB.pos.x, playerB.pos.y = bx, by
            playerB.hitbox.topleft = (bx, by)
            playerB.rect.topleft = playerB.hitbox.topleft

            # ✅ CHANGE: set respawn points for the new level
            respawnA = (ax, ay)
            respawnB = (bx, by)

        else:
            playerA.pos.xy = (200, 200)
            playerA.hitbox.topleft = (200, 200)
            playerB.pos.xy = (200, 200)
            playerB.hitbox.topleft = (200, 200)
            respawnA = (200, 200)
            respawnB = (200, 200)


        print("Solids:", len(world.solids))
        print("Layers:", len(levels.current_level["layerInstances"]))



    # Draw
    screen.fill((20, 22, 28))

    for obj in world.drawables:
        # draw terrain blocks
        obj.draw(screen)

    # draw door debug outlines (from LevelEvents)
    if hasattr(events, 'doors'):
        for d in events.doors:
            pygame.draw.rect(screen, (0, 180, 255), d, 3)

    levels.draw(screen)

    # highlight selection so you know what you're stretching
    stretcher.draw_gizmo(screen)

    playerA.draw(screen, hp_font)
    playerB.draw(screen, hp_font)

    # ----- TIMER (top-left) -----
    elapsed_ms = pygame.time.get_ticks() - start_time
    elapsed_sec = elapsed_ms // 1000
    minutes = elapsed_sec // 60
    seconds = elapsed_sec % 60

    timer_surf = timer_font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
    screen.blit(timer_surf, (10, 10))

    pygame.display.flip()

pygame.quit()


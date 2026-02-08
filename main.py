
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
gameover_image = None



# Music shit
MENU_MUSIC = "assets/music/New Composition #1.mp3"
GAME_MUSIC = "assets/music/Jungle and Rainforest Sound Effects - Tropical Forest Ambiences from Costa Rica.mp3"
pygame.mixer.music.load(MENU_MUSIC)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)




W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pygame.display.set_caption("Grow And Degrow")
FPS = 60

# load gameover image (scaled to window) if available
try:
    _go = pygame.image.load("assets/gameover_screen.png").convert_alpha()
    gameover_image = pygame.transform.smoothscale(_go, (W, H))
except Exception:
    gameover_image = None


#Menu
choice = run_menu(screen, clock, "Grow And Degrow")
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
    "assets/ADAM.json",
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
    # reset player state on level load
    playerA.vel = pygame.Vector2(0, 0)
    playerA.on_ground = False
    playerA.hp = playerA.max_hp
    playerB.pos.x, playerB.pos.y = bx, by
    playerB.hitbox.topleft = (bx, by)
    playerB.rect.topleft = playerB.hitbox.topleft
    playerB.vel = pygame.Vector2(0, 0)
    playerB.on_ground = False
    playerB.hp = playerB.max_hp



print(levels.current_level.keys())

running = True
game_over = False
winner = None

def restart_current_level():
    # clear world objects and reload the current level, then place players on spawn
    world.solids.clear()
    world.drawables.clear()
    if hasattr(world, 'triggers'):
        world.triggers.clear()

    # reload the same level index
    levels.load_level(levels.level_index)
    events.build(levels.current_level)
    sp = build_ldtk_collision(world, levels)

    # center players on spawn tiles if available
    if len(sp) >= 2:
        ts = getattr(levels, "tile_size", 64)
        ax = sp[0][0] + ts // 2 - playerA.hitbox.width // 2
        ay = sp[0][1] + ts - playerA.hitbox.height

        bx = sp[1][0] + ts // 2 - playerB.hitbox.width // 2
        by = sp[1][1] + ts - playerB.hitbox.height

        playerA.pos.x, playerA.pos.y = ax, ay
        playerA.hitbox.topleft = (ax, ay)
        playerA.rect.topleft = playerA.hitbox.topleft
        playerA.vel = pygame.Vector2(0, 0)
        playerA.on_ground = False
        playerA.hp = playerA.max_hp

        playerB.pos.x, playerB.pos.y = bx, by
        playerB.hitbox.topleft = (bx, by)
        playerB.rect.topleft = playerB.hitbox.topleft
        playerB.vel = pygame.Vector2(0, 0)
        playerB.on_ground = False
        playerB.hp = playerB.max_hp
    else:
        playerA.pos.xy = (200, 200)
        playerA.hitbox.topleft = (200, 200)
        playerB.pos.xy = (200, 200)
        playerB.hitbox.topleft = (200, 200)

    return sp

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # When game is over we only listen for restart
        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # restart current level
                spawn_positions = restart_current_level()
                game_over = False
                winner = None
            continue

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

    if playerA.hp == 0 or playerB.hp == 0:
        # set game-over state instead of blitting raw image here —
        # drawing continues later in the loop and would overwrite a direct blit.
        winner = "B" if playerA.hp == 0 else "A"
        print(f"Game Over! Player {winner} won!")
        game_over = True
        
    
    # Only update players / physics / level events when not game over
    if not game_over:
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
                playerA.vel = pygame.Vector2(0, 0)
                playerA.on_ground = False
                playerA.hp = playerA.max_hp

                playerB.pos.x, playerB.pos.y = bx, by
                playerB.hitbox.topleft = (bx, by)
                playerB.rect.topleft = playerB.hitbox.topleft
                playerB.vel = pygame.Vector2(0, 0)
                playerB.on_ground = False
                playerB.hp = playerB.max_hp
            else:
                playerA.pos.xy = (200, 200)
                playerA.hitbox.topleft = (200, 200)
                playerB.pos.xy = (200, 200)
                playerB.hitbox.topleft = (200, 200)

            print("Solids:", len(world.solids))
            print("Layers:", len(levels.current_level["layerInstances"]))



    # Draw
    screen.fill((20, 22, 28))

    for obj in world.drawables:
        # draw terrain blocks
        obj.draw(screen)
        # highlight stretchable objects with a subtle grey outline
        if hasattr(obj, "min_w") or hasattr(obj, "min_h"):
            pygame.draw.rect(screen, (120, 120, 120), obj.rect, 2)

    # draw door debug outlines (from LevelEvents)
    if hasattr(events, 'doors'):
        for d in events.doors:
            pygame.draw.rect(screen, (0, 180, 255), d, 3)

    levels.draw(screen)

    # highlight selection so you know what you're stretching
    stretcher.draw_gizmo(screen)

    playerA.draw(screen, hp_font)
    playerB.draw(screen, hp_font)

    # Game over overlay
    if game_over:
        if gameover_image:
            screen.blit(gameover_image, (0, 0))
        else:
            overlay = pygame.Surface((W, H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            msg = f"Game Over! Player {winner} won! Press R to restart"
            txt = hp_font.render(msg, True, (255, 255, 255))
            tr = txt.get_rect(center=(W // 2, H // 2))
            screen.blit(txt, tr)

    pygame.display.flip()

pygame.quit()


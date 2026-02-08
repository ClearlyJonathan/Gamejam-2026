
import pygame
import json
import src.playercontroller as pc

from src.world import World
from src.level_loader import build_test_level
from src.stretcher import Stretcher
from src.level_system import LevelSystem
from src.menu import run_menu

from src.ldtk_collision_builder import build_ldtk_collision


pygame.init()
hp_font = pygame.font.Font(None, 28)


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
#pc.SHOULD_APPLY_GRAVITY = False

# Stretch tool
stretcher = Stretcher(speed=6)

# Initialize level system
levels_system = LevelSystem(
    "src/fullmaps.json",
    "assets/tilesetResizeResize.png")

# Load fullmaps project and auto-detect level sequence
with open("src/fullmaps.json", "r", encoding="utf-8") as f:
    fullmaps_project = json.load(f)

# Extract level names (skip editor/demo levels, get only World_Level_* in order)
level_sequence = [lvl["identifier"] for lvl in fullmaps_project.get("levels", []) 
                  if "World_Level" in lvl["identifier"]]
level_sequence.sort()  # Sort to ensure proper order
print(f"Loaded {len(level_sequence)} levels: {level_sequence}")

def load_level(level_name):
    """Load a new level from fullmaps.json and setup the world"""
    global world, stretcher, levels_system
    
    # Clear world for new level
    world = World(W, H, gravity=1800.0)
    stretcher = Stretcher(speed=6)
    
    # Use the already-loaded fullmaps project
    levels_system.load_level(level_name)
    spawn_positions = build_ldtk_collision(world, levels_system)
    
    # Reset players
    playerA.vel = pygame.Vector2(0, 0)
    playerB.vel = pygame.Vector2(0, 0)
    playerA.on_ground = False
    playerB.on_ground = False
    playerA.hp = playerA.max_hp
    playerB.hp = playerB.max_hp
    
    # Spawn players
    if len(spawn_positions) >= 2:
        playerA.pos[0], playerA.pos[1] = spawn_positions[0][0], spawn_positions[0][1] - 50
        playerB.pos[0], playerB.pos[1] = spawn_positions[1][0], spawn_positions[1][1] - 50
        playerA.rect.topleft = playerA.pos
        playerB.rect.topleft = playerB.pos
        playerA.hitbox.topleft = playerA.pos
        playerB.hitbox.topleft = playerB.pos
        print(f"✓ Level '{level_name}' loaded. Players spawned at: A={spawn_positions[0]}, B={spawn_positions[1]}")
    
    return levels_system

# Load first level
current_level_index = 0
levels_system.project = fullmaps_project  # Assign the project
load_level(level_sequence[0])

running = True
level_complete = False

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left click to select a terrain object to stretch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            result = stretcher.select_at_point(world.drawables, event.pos)

    keys = pygame.key.get_pressed()

    # Stretch selected object (Q/E/Z/C + Shift)
    action = stretcher.update(keys)

    if action == "stretch":
        playerA.take_damage(1)
    elif action == "shrink":
        playerB.take_damage(1)

    if playerA.hp == 0 or playerB.hp == 0:
        print(f"Game Over! Player {'B' if playerA.hp == 0 else 'A'} won!")
        running = False
    
    # Player input
    playerA.handle_input(keys, dt)
    if not (keys[playerA.controls["left"]] or keys[playerA.controls["right"]]):
        playerA.apply_friction(dt)

    playerB.handle_input(keys, dt)
    if not (keys[playerB.controls["left"]] or keys[playerB.controls["right"]]):
        playerB.apply_friction(dt)

    # Physics + collision vs world.solids
    playerA.update(dt, world)
    playerB.update(dt, world)

    # Check trigger zones
    for trigger in world.triggers:
        trigger_type = trigger.get("type")
        trigger_rect = trigger.get("rect")
        
        # Killer trigger - deplete HP
        if trigger_type == "Killer":
            if playerA.rect.colliderect(trigger_rect):
                playerA.take_damage(1)
            if playerB.rect.colliderect(trigger_rect):
                playerB.take_damage(1)
        
        # Door trigger - level complete when both players overlap
        if trigger_type == "Door":
            if playerA.rect.colliderect(trigger_rect) and playerB.rect.colliderect(trigger_rect):
                level_complete = True

    # Handle level transition
    if level_complete:
        current_level_index += 1
        if current_level_index >= len(level_sequence):
            print("✓ Game Complete! All levels finished!")
            running = False
        else:
            next_level = level_sequence[current_level_index]
            print(f"\n→ Loading next level: {next_level}...")
            load_level(next_level)
            level_complete = False

    # Draw
    screen.fill((20, 22, 28))

    for obj in world.drawables:
        # draw terrain blocks
        obj.draw(screen)

    levels_system.draw(screen)

    # highlight selection so you know what you're stretching
    stretcher.draw_gizmo(screen)
    
    # Hover effect: show which tiles are clickable
    mouse_pos = pygame.mouse.get_pos()
    for obj in world.drawables:
        if hasattr(obj, 'rect') and obj.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (100, 255, 100), obj.rect, 3)  # green outline on hover
    
    playerA.draw(screen, hp_font)
    playerB.draw(screen, hp_font)

    pygame.display.flip()

pygame.quit()


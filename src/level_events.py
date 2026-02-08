import pygame

class LevelEvents:
    def __init__(self):
        self.doors = []
        self.killers = []

    def build(self, level_data):
        self.doors.clear()
        self.killers.clear()

        for layer in level_data.get("layerInstances") or []:
            name = layer["__identifier"]
            size = layer["__gridSize"]
            tiles = layer.get("gridTiles") or layer.get("autoLayerTiles") or []

            for tile in tiles:
                x, y = tile["px"]
                rect = pygame.Rect(x, y, size, size)

                if name == "Door":
                    self.doors.append(rect)
                elif name == "Killer":
                    self.killers.append(rect)

        # Debug: list door rects
        if self.doors:
            print("[LevelEvents] Built doors:")
            for i, d in enumerate(self.doors):
                print(f"  door[{i}] = {d}")

    def check(self, players):
        # First, check killers
        for p in players:
            player_rect = p.hitbox
            for k in self.killers:
                if player_rect.colliderect(k):
                    p.hp = 0

        # Require every player to be overlapping a door (they may share the same door)
        # Debug: report door counts and each player's overlap
        # (print statements help us see why triggers don't fire)
        print(f"[LevelEvents] doors={len(self.doors)}, killers={len(self.killers)}")
        players_on = []
        # inflate doors slightly for more forgiving overlap detection
        inflate_px = 8
        for i, p in enumerate(players):
            player_rect = p.hitbox
            on_any = any(player_rect.colliderect(d.inflate(inflate_px, inflate_px)) for d in self.doors)
            players_on.append(on_any)
            print(f"[LevelEvents] Player {i} on_door={on_any} rect={player_rect}")

        all_on = all(players_on) and len(players) > 0
        if all_on:
            print("[LevelEvents] All players on door -> next level")
        return all_on


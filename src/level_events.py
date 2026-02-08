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

    def check(self, players):
        # Sett for å lagre hvilke dører som har spillere på seg
        doors_with_players = set()

        for p in players:
            player_rect = p.hitbox

            # Sjekk killers først
            for k in self.killers:
                if player_rect.colliderect(k):
                    p.hp = 0

            # Sjekk dører
            for i, d in enumerate(self.doors):
                if player_rect.colliderect(d):
                    doors_with_players.add(i)

        # Bytt nivå hvis alle spillere står på unike dører
        next_level = len(doors_with_players) >= len(players)
        return next_level

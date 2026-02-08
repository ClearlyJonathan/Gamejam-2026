import pygame

class LevelEvents:

    def __init__(self):
        self.doors = []
        self.killers = []

    def build(self, level_data):

        self.doors.clear()
        self.killers.clear()

        for layer in level_data.get("layerInstances", []):

            name = layer["__identifier"]
            size = layer["__gridSize"]

            tiles = (
                layer.get("gridTiles")
                or layer.get("autoLayerTiles")
                or []
            )

            for tile in tiles:

                x, y = tile["px"]
                rect = pygame.Rect(x, y, size, size)

                if name == "Door":
                    self.doors.append(rect)

                elif name == "Killer":
                    self.killers.append(rect)

    def check(self, players):

        next_level = False

        for p in players:

            player_rect = p.hitbox

            for k in self.killers:
                if player_rect.colliderect(k):
                    p.hp = 0

            for d in self.doors:
                if player_rect.colliderect(d):
                    next_level = True

        return next_level

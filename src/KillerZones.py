# src/killer_zones.py
import pygame


class KillerZones:
    """
    Leser LDtk Tiles-layer 'Killer' og gjør det til dødelige trigger-rects.
    Hvis en spiller overlapper en killer-tile -> game over for begge.
    """

    def __init__(self, killer_layer_name: str = "Killer", cooldown_s: float = 0.0):
        self.killer_layer_name = killer_layer_name
        self.rects: list[pygame.Rect] = []
        self._cooldown = 0.0
        self.cooldown_s = cooldown_s

    def rebuild_from_level(self, level_system):
        """Kall etter levels.load_level(...). Bygger rects fra Killer-layer."""
        self.rects.clear()

        level = level_system.current_level
        if not level:
            return

        for layer in level.get("layerInstances", []):
            if layer.get("__identifier") != self.killer_layer_name:
                continue

            tile_size = layer["__gridSize"]
            tiles = layer.get("gridTiles") or layer.get("autoLayerTiles") or []

            for t in tiles:
                x, y = t["px"]
                self.rects.append(pygame.Rect(x, y, tile_size, tile_size))

    def update(self, dt: float, players) -> bool:
        """
        Returnerer True hvis noen treffer killer.
        players: liste [playerA, playerB] (må ha .hitbox eller .rect)
        """
        if self._cooldown > 0:
            self._cooldown -= dt
            return False

        if not self.rects:
            return False

        for p in players:
            hitbox = p.hitbox if hasattr(p, "hitbox") else p.rect
            for r in self.rects:
                if hitbox.colliderect(r):
                    self._cooldown = self.cooldown_s
                    return True

        return False

    def draw_debug(self, screen: pygame.Surface):
        """Valgfritt: tegn killer-soner som røde ruter."""
        for r in self.rects:
            pygame.draw.rect(screen, (255, 60, 60), r, 2)

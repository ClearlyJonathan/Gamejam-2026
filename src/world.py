class World:
    def __init__(self, width: int, height: int, gravity: float = 1800.0):
        self.width = width
        self.height = height
        self.gravity = gravity

        # IMPORTANT: store objects (or rects), not copied rect snapshots
        self.solids = []     # blocking collision
        self.triggers = []   # overlap zones (optional)
        self.entities = []   # enemies/npcs (optional)
        self.drawables = []  # stuff we draw + click on

    def add_solid(self, obj_or_rect):
        self.solids.append(obj_or_rect)

    def add_drawable(self, obj):
        self.drawables.append(obj)

    def add_trigger(self, trigger):
        self.triggers.append(trigger)

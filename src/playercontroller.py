import pygame



clock = pygame.time.Clock()
# These values should be set in main.py
GROUND_Y = 0 # Size of ground for collision
W, H = 0, 0 # Width and height

# Physics tuning - Lowkey copied from a random stack overflow. but we can adjust phyiscs as needed
GRAVITY = 1800.0          # px/s^2
MOVE_ACCEL = 3500.0       # px/s^2
MAX_SPEED = 420.0         # px/s
FRICTION = 12.0           # higher = more “snappy” stop
JUMP_VEL = 720.0          # px/s upward
SHOULD_APPLY_GRAVITY = False # This is for debugging, gravity since I'm not sure if we have physics yet

class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.color = color
        self.controls = controls

        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

        # IMPORTANT- For debugging.
        if SHOULD_APPLY_GRAVITY == False:
            GRAVITY = False

    def handle_input(self, keys, dt):
        ax = 0.0

        left = keys[self.controls["left"]]
        right = keys[self.controls["right"]]
        jump = keys[self.controls["jump"]]

        if left and not right:
            ax = -MOVE_ACCEL
        elif right and not left:
            ax = MOVE_ACCEL
        else:
            ax = 0.0

        # Apply horizontal acceleration
        self.vel.x += ax * dt

        # Clamp horizontal speed
        if self.vel.x > MAX_SPEED: self.vel.x = MAX_SPEED
        if self.vel.x < -MAX_SPEED: self.vel.x = -MAX_SPEED

        # Jump (only when grounded) - We might change if players can jump on each other when they stretcvh
        if jump and self.on_ground:
            self.vel.y = -JUMP_VEL
            self.on_ground = False

    def apply_friction(self, dt):
        self.vel.x -= self.vel.x * min(1.0, FRICTION * dt)
        if abs(self.vel.x) < 5:
            self.vel.x = 0

    def update(self, dt):
        # Gravity
        self.vel.y += GRAVITY * dt

        self.pos += self.vel * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Simple ground collision - Change when a better one has been made
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.pos.y = self.rect.y
            self.vel.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Keep on screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
            self.vel.x = 0
        if self.rect.right > W:
            self.rect.right = W
            self.pos.x = self.rect.x
            self.vel.x = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)






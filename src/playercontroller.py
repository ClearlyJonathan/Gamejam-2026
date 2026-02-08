import pygame



clock = pygame.time.Clock()
# These values should be set in main.py
GROUND_Y = 0 # Size of ground for collision
W, H = 0, 0 # Width and height

# Physics tuning - Lowkey copied from a random stack overflow. but we can adjust phyiscs as needed
GRAVITY = 1800.0          # px/s^2
MOVE_ACCEL = 3500.0       # px/s^2
MAX_SPEED = 300.0         # px/s
FRICTION = 12.0           # higher = more “snappy” stop
JUMP_VEL = 720.0          # px/s upward
SHOULD_APPLY_GRAVITY = True # This is for debugging, gravity since I'm not sure if we have physics yet

# Important for collision
"""
    solids = walls + crates + platforms   # things that block movement
    triggers = coins + checkpoints        # things that overlap (not added yet)
    enemies = enemy_list                  # special handling

"""

class Player:
    def __init__(self, x, y, color, controls):
        self.images_right = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f"src/sprites/green_jump{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 60))
            self.images_right.append(img_right)
        self.image = self.images_right[self.index]
        self.rect = pygame.Rect(x, y, 40, 60)         # visual
        self.hitbox = pygame.Rect(x + 4, y + 6, 40, 60) # collision (tweak)

        self.color = color
        self.controls = controls

        self.pos = pygame.Vector2(self.hitbox.topleft) # track hitbox pos using dillu hitbox system
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.hp = 100
        self.max_hp = 100

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

    # Important function do not touch. If you want to add collidables, add it using the world class.
    def _move_and_collide(self, dt, solids):
        # --- X axis ---
        self.pos.x += self.vel.x * dt
        self.hitbox.x = round(self.pos.x)

        for s in solids:
            r = s.rect if hasattr(s, "rect") else s  # normalize to pygame.Rect
            if self.hitbox.colliderect(r):
                if self.vel.x > 0:
                    self.hitbox.right = r.left
                elif self.vel.x < 0:
                    self.hitbox.left = r.right
                self.pos.x = self.hitbox.x
                self.vel.x = 0


        # --- Y axis ---
        self.pos.y += self.vel.y * dt
        self.hitbox.y = round(self.pos.y)

        self.on_ground = False
        for s in solids:
            r = s.rect if hasattr(s, "rect") else s  # normalize to pygame.Rect

            if self.hitbox.colliderect(r):
                if self.vel.y > 0:
                    # falling down, hit the top of something
                    self.hitbox.bottom = r.top
                    self.on_ground = True
                elif self.vel.y < 0:
                    # moving up, hit the bottom of something
                    self.hitbox.top = r.bottom

                self.pos.y = self.hitbox.y
                self.vel.y = 0


    def update(self, dt, world):
        if SHOULD_APPLY_GRAVITY:
            self.vel.y += world.gravity * dt

        self._move_and_collide(dt, world.solids)
        if self.hitbox.left < 0:
            self.hitbox.left = 0
            self.pos.x = self.hitbox.x
            self.vel.x = 0
        if self.hitbox.right > world.width:
            self.hitbox.right = world.width
            self.pos.x = self.hitbox.x
            self.vel.x = 0

        #handle animation
        walk_cooldown = 5
        if self.vel.x > 0 or self.vel.x < 0:
            self.counter += 1
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.image = self.images_right[self.index]
        if self.vel.x == 0 and self.vel.y == 0:
            self.counter = 0
            self.index = 0
            self.image = self.images_right[self.index]

        self.rect.midbottom = self.hitbox.midbottom

    def draw(self, surf, font):
        surf.blit(self.image, self.rect)

         # draw hp above head
        # ---- HP BAR ----
        bar_width = self.rect.width
        bar_height = 6
        padding = 8

        # position above head
        x = self.rect.left
        y = self.rect.top - padding - bar_height

        # background (missing hp)
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(surf, (80, 80, 80), bg_rect)

        # current hp
        hp_ratio = self.hp / self.max_hp
        hp_rect = pygame.Rect(x, y, int(bar_width * hp_ratio), bar_height)

        # color changes with hp
        if hp_ratio > 0.6:
            color = (0, 220, 0)
        elif hp_ratio > 0.3:
            color = (240, 200, 0)
        else:
            color = (220, 40, 40)

        pygame.draw.rect(surf, color, hp_rect)

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

class Player1:
    def __init__(self, x, y, color, controls):
        self.images_right = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f"src/sprites/pink_jump{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 60))
            self.images_right.append(img_right)
        self.image = self.images_right[self.index]
        self.rect = pygame.Rect(x, y, 40, 60)         # visual
        self.hitbox = pygame.Rect(x + 4, y + 6, 40, 60) # collision (tweak)

        self.color = color
        self.controls = controls

        self.pos = pygame.Vector2(self.hitbox.topleft) # track hitbox pos using dillu hitbox system
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.hp = 100
        self.max_hp = 100

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

    # Important function do not touch. If you want to add collidables, add it using the world class.
    def _move_and_collide(self, dt, solids):
        # --- X axis ---
        self.pos.x += self.vel.x * dt
        self.hitbox.x = round(self.pos.x)

        for s in solids:
            r = s.rect if hasattr(s, "rect") else s  # normalize to pygame.Rect
            if self.hitbox.colliderect(r):
                if self.vel.x > 0:
                    self.hitbox.right = r.left
                elif self.vel.x < 0:
                    self.hitbox.left = r.right
                self.pos.x = self.hitbox.x
                self.vel.x = 0


        # --- Y axis ---
        self.pos.y += self.vel.y * dt
        self.hitbox.y = round(self.pos.y)

        self.on_ground = False
        for s in solids:
            r = s.rect if hasattr(s, "rect") else s  # normalize to pygame.Rect

            if self.hitbox.colliderect(r):
                if self.vel.y > 0:
                    # falling down, hit the top of something
                    self.hitbox.bottom = r.top
                    self.on_ground = True
                elif self.vel.y < 0:
                    # moving up, hit the bottom of something
                    self.hitbox.top = r.bottom

                self.pos.y = self.hitbox.y
                self.vel.y = 0


    def update(self, dt, world):
        if SHOULD_APPLY_GRAVITY:
            self.vel.y += world.gravity * dt

        self._move_and_collide(dt, world.solids)
        if self.hitbox.left < 0:
            self.hitbox.left = 0
            self.pos.x = self.hitbox.x
            self.vel.x = 0
        if self.hitbox.right > world.width:
            self.hitbox.right = world.width
            self.pos.x = self.hitbox.x
            self.vel.x = 0

        #handle animation
        walk_cooldown = 5
        if self.vel.x > 0 or self.vel.x < 0:
            self.counter += 1
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.image = self.images_right[self.index]
        if self.vel.x == 0 and self.vel.y == 0:
            self.counter = 0
            self.index = 0
            self.image = self.images_right[self.index]

        self.rect.midbottom = self.hitbox.midbottom

    def draw(self, surf, font):
        surf.blit(self.image, self.rect)

         # draw hp above head
        # ---- HP BAR ----
        bar_width = self.rect.width
        bar_height = 6
        padding = 8

        # position above head
        x = self.rect.left
        y = self.rect.top - padding - bar_height

        # background (missing hp)
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(surf, (80, 80, 80), bg_rect)

        # current hp
        hp_ratio = self.hp / self.max_hp
        hp_rect = pygame.Rect(x, y, int(bar_width * hp_ratio), bar_height)

        # color changes with hp
        if hp_ratio > 0.6:
            color = (0, 220, 0)
        elif hp_ratio > 0.3:
            color = (240, 200, 0)
        else:
            color = (220, 40, 40)

        pygame.draw.rect(surf, color, hp_rect)

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

playerA = Player1(
    x=200, y=500, color=(200, 60, 60),
    controls={"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w},
)

playerB = Player(
    x=900, y=500, color=(60, 120, 220),
    controls={"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP},
)




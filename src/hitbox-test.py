import pygame
import sys

# bruk awsd for å bevege player
# overlapper ikke når den treffer veggen

# setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hitbox Example")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE  = (50, 100, 255)
GRAY  = (120, 120, 120)
RED   = (255, 0, 0)

# wall 
class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)

# eksempel player
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 60)   # player body
        self.hitbox = pygame.Rect(x + 8, y + 10, 34, 45)  # mindre hitbox

        self.speed = 4
        self.vx = 0
        self.vy = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = 0
        self.vy = 0

        if keys[pygame.K_a]:
            self.vx = -self.speed
        if keys[pygame.K_d]:
            self.vx = self.speed
        if keys[pygame.K_w]:
            self.vy = -self.speed
        if keys[pygame.K_s]:
            self.vy = self.speed

    def move(self, walls):
        # X movement 
        self.hitbox.x += self.vx
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if self.vx > 0:
                    self.hitbox.right = wall.rect.left
                if self.vx < 0:
                    self.hitbox.left = wall.rect.right

        # y movement
        self.hitbox.y += self.vy
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if self.vy > 0:
                    self.hitbox.bottom = wall.rect.top
                if self.vy < 0:
                    self.hitbox.top = wall.rect.bottom

        # Sync visual rect with hitbox
        self.rect.topleft = (self.hitbox.x - 8, self.hitbox.y - 10)

    def update(self, walls):
        self.handle_input()
        self.move(walls)

    def draw(self, surface):
        # draw player body
        pygame.draw.rect(surface, BLUE, self.rect)
        # draw hitbox 
        pygame.draw.rect(surface, RED, self.hitbox, 2)

# Game ovjects
player = Player(100, 100)

walls = [
    Wall(300, 150, 200, 40),
    Wall(200, 350, 400, 40),
    Wall(100, 200, 40, 250),
]

# mainloop?
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(walls)

    # tegn
    screen.fill(WHITE)
    for wall in walls:
        wall.draw(screen)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()

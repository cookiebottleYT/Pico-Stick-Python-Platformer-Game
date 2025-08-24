import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pico Stick Platformer")
clock = pygame.time.Clock()
FPS = 60

# Colors
CORNSILK = (255, 248, 220)
ORANGE = (255, 165, 0)
PLAYER_COLOR = (0, 100, 255)
FLAG_COLOR = (255, 0, 0)
BLOCK_COLOR = (150, 75, 0)
MOVING_PLATFORM_COLOR = (255, 200, 0)

# Player
player_width, player_height = 40, 40
player_speed = 5
jump_power = 15  # Normal jump power
gravity = 1

class MovingPlatform:
    def __init__(self, rect, dx=0, dy=0, bounds=None):
        self.rect = pygame.Rect(rect)
        self.dx = dx
        self.dy = dy
        self.bounds = bounds

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.bounds:
            x1, y1, x2, y2 = self.bounds
            if self.rect.left < x1 or self.rect.right > x2:
                self.dx *= -1
            if self.rect.top < y1 or self.rect.bottom > y2:
                self.dy *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, MOVING_PLATFORM_COLOR, self.rect)

class PushBlock:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

    def push(self, dx, platforms):
        self.rect.x += dx
        for p in platforms:
            if self.rect.colliderect(p):
                if dx > 0:
                    self.rect.right = p.left
                elif dx < 0:
                    self.rect.left = p.right

    def draw(self, surface):
        pygame.draw.rect(surface, BLOCK_COLOR, self.rect)

# ---------------------- LEVEL DATA ----------------------
level_data = [
    # Level 1
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (200, 450, 200, 20)],
        "moving_platforms": [((400, 350, 150, 20), 0, 2, (400, 350, 400, 500))],
        "push_blocks": [(300, HEIGHT - 80, 40, 40)],
        "flag": (350, 410, 40, 40)
    },
    # Level 2
    {
        "start": (50, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (150, 500, 200, 20), (400, 400, 150, 20)],
        "moving_platforms": [((600, 350, 100, 20), 0, 2, (600, 350, 600, 500))],
        "push_blocks": [(200, 460, 40, 40)],
        "flag": (430, 360, 40, 40)
    },
    # Level 3
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (200, 480, 150, 20), (400, 400, 150, 20), (600, 330, 150, 20)],
        "moving_platforms": [((350, 450, 100, 20), 2, 0, (350, 450, 550, 450))],
        "push_blocks": [(250, 440, 40, 40), (450, 370, 40, 40)],
        "flag": (630, 290, 40, 40)
    },
    # Level 4
    {
        "start": (50, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (200, 500, 100, 20), (350, 450, 150, 20), (550, 400, 150, 20)],
        "moving_platforms": [((500, 300, 100, 20), 0, 3, (500, 300, 500, 450))],
        "push_blocks": [(220, 460, 40, 40)],
        "flag": (580, 360, 40, 40)
    },
    # Level 5
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (150, 500, 200, 20), (400, 450, 150, 20), (600, 380, 150, 20)],
        "moving_platforms": [((300, 400, 100, 20), 2, 0, (300, 400, 500, 400))],
        "push_blocks": [(200, 460, 40, 40)],
        "flag": (650, 340, 40, 40)
    },
    # Level 6
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (200, 500, 150, 20), (400, 420, 150, 20), (600, 350, 150, 20), (600, 450, 50, 20)],
        "moving_platforms": [((350, 380, 100, 20), 0, 2, (350, 380, 350, 500))],
        "push_blocks": [(220, 460, 40, 40), (450, 400, 40, 40)],
        "flag": (630, 320, 40, 40)
    },
    # Level 7
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (150, 500, 150, 20), (350, 450, 150, 20), (550, 400, 150, 20)],
        "moving_platforms": [((200, 350, 100, 20), 2, 0, (200, 350, 400, 350)), ((600, 300, 100, 20), 0, 2, (600, 300, 600, 450))],
        "push_blocks": [(220, 460, 40, 40), (500, 370, 40, 40)],
        "flag": (580, 360, 40, 40)
    },
    # Level 8
    {
        "start": (50, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (150, 500, 200, 20), (400, 400, 150, 20)],
        "moving_platforms": [((300, 350, 100, 20), 0, 3, (300, 350, 300, 500))],
        "push_blocks": [(200, 460, 40, 40)],
        "flag": (430, 360, 40, 40)
    },
    # Level 9
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (200, 500, 150, 20), (400, 420, 150, 20)],
        "moving_platforms": [((350, 380, 100, 20), 2, 0, (350, 380, 550, 380))],
        "push_blocks": [(250, 460, 40, 40)],
        "flag": (630, 390, 40, 40)
    },
    # Level 10
    {
        "start": (100, 500),
        "platforms": [(0, HEIGHT - 40, WIDTH, 40), (150, 500, 150, 20), (350, 450, 150, 20), (550, 400, 150, 20)],
        "moving_platforms": [((200, 350, 100, 20), 2, 0, (200, 350, 400, 350)), ((500, 300, 100, 20), 0, 2, (500, 300, 500, 450))],
        "push_blocks": [(220, 460, 40, 40), (450, 370, 40, 40)],
        "flag": (580, 360, 40, 40)
    }
]

# ---------------------- GAME STATE ----------------------
current_level = 0
player_x, player_y = level_data[current_level]["start"]
y_velocity = 0
on_ground = False

# Pre-create platforms, moving platforms, push blocks, and flags per level
levels_objects = []
for l in level_data:
    platforms = [pygame.Rect(*p) for p in l["platforms"]]
    moving_platforms = [MovingPlatform(mp[0], mp[1], mp[2], mp[3]) for mp in l.get("moving_platforms", [])]
    push_blocks = [PushBlock(pb) for pb in l.get("push_blocks", [])]
    flag = pygame.Rect(*l["flag"])
    levels_objects.append({
        "platforms": platforms,
        "moving_platforms": moving_platforms,
        "push_blocks": push_blocks,
        "flag": flag,
        "start": l["start"]
    })

# ---------------------- MAIN LOOP ----------------------
while True:
    clock.tick(FPS)
    screen.fill(CORNSILK)

    # Get current level objects
    objs = levels_objects[current_level]
    platforms = objs["platforms"]
    moving_platforms = objs["moving_platforms"]
    push_blocks = objs["push_blocks"]
    flag = objs["flag"]

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_a]:
        dx = -player_speed
    if keys[pygame.K_d]:
        dx = player_speed
    if keys[pygame.K_UP] and on_ground:
        y_velocity = -jump_power
        on_ground = False

    # Horizontal movement
    player_x += dx
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Push blocks
    for block in push_blocks:
        if player_rect.colliderect(block.rect):
            block.push(dx, platforms)
            if dx > 0:
                player_x = block.rect.left - player_width
            elif dx < 0:
                player_x = block.rect.right

    # Gravity
    y_velocity += gravity
    player_y += y_velocity
    player_rect.y = player_y

    # Collision with static platforms
    on_ground = False
    for p in platforms:
        if player_rect.colliderect(p):
            if y_velocity > 0 and player_rect.bottom <= p.bottom:
                player_y = p.top - player_height
                y_velocity = 0
                on_ground = True

    # Collision with moving platforms
    for mp in moving_platforms:
        mp.update()
        if player_rect.colliderect(mp.rect):
            if y_velocity > 0 and player_rect.bottom <= mp.rect.bottom:
                player_y = mp.rect.top - player_height
                y_velocity = 0
                on_ground = True
                player_x += mp.dx

    # Flag collision → next level
    if player_rect.colliderect(flag):
        current_level += 1
        if current_level >= len(level_data):
            print("All 10 levels complete!")
            pygame.quit()
            sys.exit()
        player_x, player_y = levels_objects[current_level]["start"]
        y_velocity = 0
        on_ground = False

    # Draw everything
    for p in platforms:
        pygame.draw.rect(screen, ORANGE, p)
    for mp in moving_platforms:
        mp.draw(screen)
    for pb in push_blocks:
        pb.draw(screen)
    pygame.draw.rect(screen, FLAG_COLOR, flag)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    pygame.display.flip()

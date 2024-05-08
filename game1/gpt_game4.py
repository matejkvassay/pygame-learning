import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Shooter Game with Sprites")

# Load sprites
player_image = pygame.image.load('./assets/player.png').convert_alpha()
enemy_image = pygame.image.load('./assets/zumbi.png').convert_alpha()

# Get sprite dimensions
player_size = player_image.get_rect().size
enemy_size = enemy_image.get_rect().size

# Player settings
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Bullet settings
bullet_speed = 50
bullets = []

# Burst settings
burst_count = 3
burst_delay = 0.1  # Delay between each bullet in a burst
burst_in_progress = False
burst_bullets = []  # To track burst bullets

# Enemy settings
enemy_speed = 2
enemies = []

# Game loop
running = True
clock = pygame.time.Clock()


# Function to spawn enemies at random locations at screen edges
def spawn_enemy():
    spawn_edge = random.choice(["top", "bottom", "left", "right"])
    if spawn_edge == "top":
        x = random.randint(0, SCREEN_WIDTH - enemy_size[0])
        y = -enemy_size[1]
    elif spawn_edge == "bottom":
        x = random.randint(0, SCREEN_WIDTH - enemy_size[0])
        y = SCREEN_HEIGHT
    elif spawn_edge == "left":
        x = -enemy_size[0]
        y = random.randint(0, SCREEN_HEIGHT - enemy_size[1])
    elif spawn_edge == "right":
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT - enemy_size[1])

    return [x, y]


# Initial enemy spawn
enemies.append(spawn_enemy())

while running:
    current_time = time.time()  # Current time for burst timing

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not burst_in_progress:
                burst_in_progress = True
                burst_start_time = current_time  # Record when the burst started
                burst_bullets = [0]  # Track bullets in the burst

    # Key input for player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Keep the player within screen bounds
    player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - player_size[0]))
    player_pos[1] = max(0, min(player_pos[1], SCREEN_HEIGHT - player_size[1]))

    # Shooting logic for burst bullets
    if burst_in_progress:
        if len(burst_bullets) < burst_count:
            if current_time - burst_start_time >= burst_delay * len(burst_bullets):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                base_direction = math.atan2(mouse_y - player_pos[1], mouse_x - player_pos[0])
                angle_spread = math.radians(10)  # Spread angle

                bullet_offset = len(burst_bullets) - 1  # Adjust index for each bullet

                bullets.append({
                    "pos": [player_pos[0] + player_size[0] // 2, player_pos[1] + player_size[1] // 2],
                    "dir": base_direction + bullet_offset * angle_spread
                })

                burst_bullets.append(len(burst_bullets))
        else:
            burst_in_progress = False

    # Update bullet positions
    bullets = [
        {
            "pos": [b["pos"][0] + bullet_speed * math.cos(b["dir"]),
                    b["pos"][1] + bullet_speed * math.sin(b["dir"])],
            "dir": b["dir"]
        }
        for b in bullets
    ]

    # Remove bullets that are off-screen
    bullets = [b for b in bullets if (0 <= b["pos"][0] <= SCREEN_WIDTH) and (0 <= b["pos"][1] <= SCREEN_HEIGHT)]

    # Update enemy positions and move toward the player
    for enemy in enemies:
        angle = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
        enemy[0] += enemy_speed * math.cos(angle)
        enemy[1] += enemy_speed * math.sin(angle)

    # Draw to the screen
    screen.fill(WHITE)

    # Draw the player
    screen.blit(player_image, player_pos)

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, [int(bullet["pos"][0]), int(bullet["pos"][1])], 5)

    # Draw the enemies
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Collision detection between bullets and enemies
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet["pos"][0], bullet["pos"][1], 5, 5)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(*enemy, enemy_size[0], enemy_size[1])
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemies.append(spawn_enemy())

    # Collision detection between player and enemies
    player_rect = pygame.Rect(*player_pos, player_size[0], player_size[1])
    # for enemy in enemies:
    #     enemy_rect = pygame.Rect(*enemy, enemy_size[0], enemy_size[1])
    #     if player_rect.collides with enemy_rect:
    #         running = False  # Game over if player collides with an enemy

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

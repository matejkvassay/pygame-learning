import pygame
import random
import math

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
GREEN = (25, 210, 25)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Shooter Game")

# Player settings
player_size = 40
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Bullet settings
bullet_speed = 40
bullets = []

# Enemy settings
enemy_size = 40
enemy_speed = 2
enemies = []

# Game loop
running = True
clock = pygame.time.Clock()


def spawn_enemy():
    # Spawn enemies at a random location on the edges of the screen
    spawn_edge = random.choice(["top", "bottom", "left", "right"])
    if spawn_edge == "top":
        x = random.randint(0, SCREEN_WIDTH)
        y = -enemy_size
    elif spawn_edge == "bottom":
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT
    elif spawn_edge == "left":
        x = -enemy_size
        y = random.randint(0, SCREEN_HEIGHT)
    elif spawn_edge == "right":
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT)

    return [x, y]


# Initial enemy spawn
enemies.append(spawn_enemy())

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot a bullet toward the mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = math.atan2(mouse_y - player_pos[1], mouse_x - player_pos[0])
                bullet = {
                    "pos": [player_pos[0] + player_size // 2, player_pos[1] + player_size // 2],
                    "dir": direction
                }
                bullets.append(bullet)


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
    player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - player_size))
    player_pos[1] = max(0, min(player_pos[1], SCREEN_HEIGHT - player_size))

    # Update bullet positions
    for bullet in bullets:
        bullet["pos"][0] += bullet_speed * math.cos(bullet["dir"])
        bullet["pos"][1] += bullet_speed * math.sin(bullet["dir"])

    # Remove bullets that are off-screen
    bullets = [b for b in bullets if 0 <= b["pos"][0] <= SCREEN_WIDTH and 0 <= b["pos"][1] <= SCREEN_HEIGHT]

    # Update enemy positions and move toward the player
    for enemy in enemies:
        angle = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
        enemy[0] += enemy_speed * math.cos(angle)
        enemy[1] += enemy_speed * math.sin(angle)

    # Draw to the screen
    screen.fill(BLACK)

    # Draw the player
    pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, (int(bullet["pos"][0]), int(bullet["pos"][1]), 3, 3))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (*enemy, enemy_size, enemy_size))

    # Collision detection between bullets and enemies
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet["pos"][0], bullet["pos"][1], 5, 5)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(*enemy, enemy_size, enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemies.append(spawn_enemy())  # Spawn a new enemy on destruction

    # Collision detection between player and enemies
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(*enemy, enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            running = False  # Game over if player collides with an enemy

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

# generated with GPT3.5
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

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Player settings
player_size = 40
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_size]
player_speed = 5

# Bullet settings
bullet_speed = 70
bullets = []

# Enemy settings
enemy_size = 40
enemy_speed = 3
enemies = []


# Function to spawn enemies at random positions
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_size)
    y = random.randint(-200, -50)  # Spawns above the screen
    return [x, y]


# Spawn initial enemies
for _ in range(5):
    enemies.append(spawn_enemy())

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot a bullet
                bullets.append([player_pos[0] + player_size // 2, player_pos[1]])

    # Key input for player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed

    # Keep the player within screen bounds
    player_pos[0] = max(0, min(player_pos[0], SCREEN_WIDTH - player_size))

    # Update bullet positions
    bullets = [[x, y - bullet_speed] for x, y in bullets]

    # Remove bullets that are off-screen
    bullets = [b for b in bullets if b[1] > 0]

    # Update enemy positions
    for enemy in enemies:
        enemy[1] += enemy_speed

    # Spawn new enemies as needed
    while len(enemies) < 5:
        enemies.append(spawn_enemy())

    # Collision detection between bullets and enemies
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(*bullet, 5, 10)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(*enemy, enemy_size, enemy_size)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

    # Collision detection between player and enemies
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(*enemy, enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            running = False  # Game over if player hits an enemy

    # Drawing
    screen.fill(BLACK)  # Clear the screen with black

    # Draw the player
    pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (*bullet, 5, 10))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (*enemy, enemy_size, enemy_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Clean up
pygame.quit()

# generated with GPT3.5
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Top-Down Game")

# Player settings
player_size = 30
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Obstacle settings
obstacle_size = 40
obstacle_pos = [random.randint(0, SCREEN_WIDTH - obstacle_size), random.randint(0, SCREEN_HEIGHT - obstacle_size)]
obstacle_color = RED

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key input
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

    # Drawing
    screen.fill(BLACK)  # Clear the screen with black

    # Draw the player
    pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))

    # Draw the obstacle
    pygame.draw.rect(screen, RED, (*obstacle_pos, obstacle_size, obstacle_size))

    # Check for collision between player and obstacle
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    obstacle_rect = pygame.Rect(*obstacle_pos, obstacle_size, obstacle_size)

    if player_rect.colliderect(obstacle_rect):
        # If a collision occurs, change the obstacle's position
        obstacle_pos = [random.randint(0, SCREEN_WIDTH - obstacle_size), random.randint(0, SCREEN_HEIGHT - obstacle_size)]

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Clean up
pygame.quit()
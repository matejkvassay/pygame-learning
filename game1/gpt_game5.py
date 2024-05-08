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
pygame.display.set_caption("2D Shooter Game with Rotating Sprites")

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
bullet_speed = 10
bullets = []

# Burst settings
burst_count = 3  # Number of bullets in a burst
burst_delay = 0.1  # Delay between each bullet in a burst
burst_in_progress = False
burst_bullets = []  # To track bullets in the burst
burst_start_time = 0  # To track when the burst starts

# Enemy settings
enemy_speed = 2
enemies = []

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

    angle = math.atan2(player_pos[1] - y, player_pos[0] - x)
    rotated_enemy_image = pygame.transform.rotate(enemy_image, -math.degrees(angle))

    return {
        "pos": [x, y],
        "angle": angle,
        "image": rotated_enemy_image,
    }

# Initial enemy spawn
enemies.append(spawn_enemy())

running = True
clock = pygame.time.Clock()

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
                burst_bullets = []  # Reset bullets in the burst

    # Player movement logic
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

    # Rotate player image to point towards mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_angle = math.degrees(math.atan2(mouse_y - player_pos[1], mouse_x - player_pos[0]))  # Angle towards mouse
    rotated_player_image = pygame.transform.rotate(player_image, -player_angle)  # Rotate image to face mouse

    # Burst shooting logic
    if burst_in_progress:
        # Add new bullets at the correct intervals
        if len(burst_bullets) < burst_count:
            if current_time - burst_start_time >= burst_delay * len(burst_bullets):
                bullet_direction = math.atan2(mouse_y - player_pos[1], mouse_x - player_pos[0])
                angle_spread = math.radians(10)  # Spread angle

                # Create burst bullets with slight spread
                bullet_offset = len(burst_bullets) - 1
                new_bullet = {
                    "pos": [player_pos[0] + player_size[0] // 2, player_pos[1] + player_size[1] // 2],
                    "dir": bullet_direction + bullet_offset * angle_spread
                }

                bullets.append(new_bullet)  # Add to list of bullets
                burst_bullets.append(new_bullet)  # Track this bullet in the burst
        else:
            burst_in_progress = False  # Burst complete

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
    bullets = [b for b in bullets if 0 <= b["pos"][0] <= SCREEN_WIDTH and 0 <= b["pos"][1] <= SCREEN_HEIGHT]

    # Update enemy positions and rotate based on movement towards the player
    for enemy in enemies:
        enemy_angle = math.atan2(player_pos[1] - enemy["pos"][1], player_pos[0] - enemy["pos"][0])
        enemy["pos"][0] += enemy_speed * math.cos(enemy_angle)
        enemy["pos"][1] += enemy_speed * math.sin(enemy_angle)

        # Rotate the enemy image to face towards the player
        rotated_enemy_image = pygame.transform.rotate(enemy_image, -math.degrees(enemy_angle))
        enemy["image"] = rotated_enemy_image  # Rotate to face the player

    # Draw to the screen
    screen.fill(BLACK)

    # Adjust position to center the rotated image (since rotation changes the rect)
    player_center_offset = (rotated_player_image.get_width() - player_size[0], rotated_player_image.get_height() - player_size[1])
    screen.blit(rotated_player_image, (player_pos[0] - player_center_offset[0] / 2, player_pos[1] - player_center_offset[1] / 2))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, [int(bullet["pos"][0]), int(bullet["pos"][1])], 5)

    # Draw the enemies
    for enemy in enemies:
        enemy_center_offset = (enemy["image"].get_width() - enemy_size[0], enemy["image"].get_height() - enemy_size[1])
        screen.blit(enemy["image"], (enemy["pos"][0] - enemy_center_offset[0] / 2, enemy["pos"][1] - enemy_center_offset[1] / 2))

    # Collision detection between bullets and enemies
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet["pos"][0], bullet["pos"][1], 5, 5)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy["image"].get_width(), enemy["image"].get_height())
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemies.append(spawn_enemy())  # Spawn a new enemy when one is destroyed

    # Collision detection between player and enemies
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size[0], player_size[1])
    for enemy in enemies:
        pass
        # if player_rect.collides with enemy_rect:
        #     running = False  # Game over if the player collides with an enemy

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

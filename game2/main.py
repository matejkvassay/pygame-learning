import pygame
from game_renderer import GameRenderer
from game_environment import GameEnvironment
from characters.player import Player
from guns.pistol_9mm import Pistol9MM

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_POS_X = SCREEN_WIDTH // 2
PLAYER_POS_Y = SCREEN_HEIGHT // 2
PLAYER_MOVEMENT_SPEED = 3
PLAYER_DIRECTION = 0
CAPTION = "GAME2"

pygame_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_env = GameEnvironment()
pistol = Pistol9MM(game_env)
player = Player(PLAYER_POS_X,
                PLAYER_POS_Y,
                rotation_angle=PLAYER_DIRECTION,
                equipped_gun=pistol,
                movement_speed=PLAYER_MOVEMENT_SPEED)
game_env.add(player)
game_renderer = GameRenderer(pygame_screen, game_env, CAPTION)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for game_obj in game_env:
        game_obj.act()
    game_renderer.render()
    clock.tick(FPS)

pygame.quit()

import pygame
from .action_types import (
    SHOOT_GUN,
    RELOAD_GUN,
    MOVE_UP,
    MOVE_DOWN,
    MOVE_LEFT,
    MOVE_RIGHT,
    TURN_TOWARDS_MOUSE
)
import math


class PlayerBrain:
    KEY_BINDINGS = {
        pygame.K_SPACE: SHOOT_GUN,
        pygame.K_r: RELOAD_GUN,
        pygame.K_w: MOVE_UP,
        pygame.K_s: MOVE_DOWN,
        pygame.K_a: MOVE_LEFT,
        pygame.K_d: MOVE_RIGHT
    }

    def decide_actions(self):
        pressed_keys = pygame.key.get_pressed()
        for key in self.KEY_BINDINGS.keys():
            if pressed_keys[key]:
                yield self.KEY_BINDINGS[key]
        yield TURN_TOWARDS_MOUSE


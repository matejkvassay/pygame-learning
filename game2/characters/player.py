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
from .player_brain import PlayerBrain
import math


class Player:
    MOVEMENT_ACTIONS = {MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT}

    def __init__(self, pos_x, pos_y, rotation_angle, equipped_gun, brain=PlayerBrain(), movement_speed=3,
                 sprite='./assets/player.png'):

        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x, self.size_y = self.sprite.get_rect().size
        self.rotation_angle = rotation_angle

        self.brain = brain
        self.movement_speed = movement_speed
        self.equipped_gun = equipped_gun

    def act(self):
        for action in self.brain.decide_actions():
            if self.is_movement_action(action):
                self.move(action)
            elif action == SHOOT_GUN:
                self.shoot_gun()
            elif action == RELOAD_GUN:
                self.reload_gun()
            elif action == TURN_TOWARDS_MOUSE:
                self.turn_towards_mouse()
            else:
                brain_cls = self.brain.__class__.__name__
                raise ValueError(f"Brain {brain_cls} selected unrecognized action: {action}")

    def reload_gun(self):
        self.equipped_gun.change_magazine()

    def shoot_gun(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.equipped_gun.trigger(self.pos_x, self.pos_y, mouse_x, mouse_y)

    def move(self, action):
        if action == MOVE_LEFT:
            self.pos_x -= self.movement_speed
        elif action == MOVE_DOWN:
            self.pos_y += self.movement_speed
        elif action == MOVE_RIGHT:
            self.pos_x += self.movement_speed
        elif action == MOVE_UP:
            self.pos_y -= self.movement_speed
        else:
            raise ValueError(f"Unrecognized movement action: {action}")

    def turn_towards_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rotation_angle = math.degrees(math.atan2(mouse_y - self.pos_y, mouse_x - self.pos_x))

    def is_movement_action(self, action):
        if action in self.MOVEMENT_ACTIONS:
            return True
        return False

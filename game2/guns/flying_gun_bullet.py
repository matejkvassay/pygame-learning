import pygame
import math


class FlyingGunBullet:
    def __init__(self, pos_x, pos_y, damage_rate, rotation_angle, movement_speed, size_x, size_y,
                 sprite='./assets/bullet_green.png'):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rotation_angle = rotation_angle
        self.size_x, self.size_y = size_x, size_y
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.damage_rate = damage_rate
        self.movement_speed = movement_speed

    def act(self):
        self.pos_x += self.movement_speed * math.cos(self.rotation_angle)
        self.pos_y += self.movement_speed * math.sin(self.rotation_angle)

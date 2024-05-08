from .flying_gun_bullet import FlyingGunBullet
import math
from time import time


class Pistol9MM:
    def __init__(self, game_env, damage_rate=0.3, magazine_size=15, ammo_in_magazine=15, bullet_movement_speed=10,
                 bullet_size_x=2, bullet_size_y=3, fire_rate=2):
        self.damage_rate = damage_rate
        self.magazine_size = magazine_size
        self.ammo_in_magazine = ammo_in_magazine
        self.fire_rate_min_dur = 1/fire_rate
        self.bullet_movement_speed = bullet_movement_speed
        self.bullet_size_x, self.bullet_size_y = bullet_size_x, bullet_size_y
        self.game_env = game_env
        self.last_fired = time()

    def trigger(self, shooter_pos_x, shooter_pos_y, aim_direction_x, aim_direction_y):
        dur_since_last_bullet = time() - self.last_fired

        if dur_since_last_bullet > self.fire_rate_min_dur:
            bullet_direction = math.atan2(aim_direction_y - shooter_pos_y, aim_direction_x - shooter_pos_x)
            bullet = FlyingGunBullet(shooter_pos_x, shooter_pos_y, self.damage_rate, bullet_direction,
                                     self.bullet_movement_speed,
                                     size_x=self.bullet_size_x,
                                     size_y=self.bullet_size_y)
            self.game_env.add(bullet)
            self.last_fired = time()

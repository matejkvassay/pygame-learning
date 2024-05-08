from .flying_gun_bullet import FlyingGunBullet


class Pistol9MM:
    def __init__(self, game_env, damage_rate=0.3, magazine_size=15, ammo_in_magazine=15, bullet_movement_speed=50,
                 bullet_size_x=2, bullet_size_y=3):
        self.damage_rate = damage_rate
        self.magazine_size = magazine_size
        self.ammo_in_magazine = ammo_in_magazine
        self.bullet_movement_speed = bullet_movement_speed
        self.bullet_size_x, self.bullet_size_y = bullet_size_x, bullet_size_y
        self.game_env = game_env

    def trigger(self, shooter_pos_x, shooter_pos_y, shooter_direction):
        bullet = FlyingGunBullet(shooter_pos_x, shooter_pos_y, self.damage_rate, shooter_direction,
                                 self.bullet_movement_speed,
                                 size_x=self.bullet_size_x,
                                 size_y=self.bullet_size_y)
        self.game_env.add(bullet)

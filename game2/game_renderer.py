import pygame


class GameRenderer:
    BACKGROUND_COLOR = (255, 255, 255)

    def __init__(self, pygame_screen, game_env, caption):
        self.game_env = game_env
        self.screen = pygame_screen
        pygame.display.set_caption(caption)

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        for obj in self.game_env:
            rotated_image = pygame.transform.rotate(obj.sprite, -obj.rotation_angle)
            obj_center_offset_x = rotated_image.get_width() - obj.size_x
            obj_center_offset_y = rotated_image.get_height() - obj.size_y
            area_x = obj.pos_x - obj_center_offset_x / 2
            area_y = obj.pos_y - obj_center_offset_y / 2
            self.screen.blit(rotated_image, (area_x, area_y))
        pygame.display.flip()

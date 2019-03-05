import pygame


class Character(pygame.sprite.Sprite):
    HEIGHT = 50
    WIDTH = 80
    hitbox = None

    def __init__(self, screen, level_floor, *groups):
        super().__init__(*groups)
        self.default_y = screen.get_height() - self.HEIGHT / 2.0 - level_floor
        self.position_x = screen.get_width() / 2.0
        self.position_y = self.default_y
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox = (
            self.position_x - self.WIDTH / 4, self.position_y - self.HEIGHT / 2, self.WIDTH / 2, self.HEIGHT)

from math import fabs

import pygame
import character


class Monster(character.Character):
    def __init__(self, screen, spawn_point_x, level_y, *groups):
        super().__init__(screen, spawn_point_x, level_y, *groups)
        self.IDLE_LENGTH = 4
        self.RUN_LENGTH = 4
        self.character_textures.update({
            self.IDLE_TILES: [
                pygame.image.load('./assets/hell-ghost/ghost-1.png'),
                pygame.image.load('./assets/hell-ghost/ghost-2.png'),
                pygame.image.load('./assets/hell-ghost/ghost-3.png'),
                pygame.image.load('./assets/hell-ghost/ghost-4.png'),
            ],
            self.RUN_TILES: [
                pygame.image.load('./assets/hell-ghost/ghost-halo-1.png'),
                pygame.image.load('./assets/hell-ghost/ghost-halo-2.png'),
                pygame.image.load('./assets/hell-ghost/ghost-halo-3.png'),
                pygame.image.load('./assets/hell-ghost/ghost-halo-4.png'),
            ]
        })
        self.walk_speed = 80
        self.image = self.get_current_tile()
        self.target_x = 0

    def update(self, target_x, dt, *args):
        super().update(*args)
        self.update_rect()
        self.target_x = target_x
        self.follow_player(dt)

    def follow_player(self, dt):
        if fabs(self.position_x - self.target_x) > self.MARGIN:
            self.is_running = True
            if self.position_x < self.target_x:
                self.move_right(dt)
            else:
                self.move_left(dt)
        else:
            self.is_running = False

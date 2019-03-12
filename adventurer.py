from math import floor, fabs

import pygame

import character


class Adventurer(character.Character):

    def __init__(self, screen, spawn_point_x, level_y, *groups):
        super().__init__(screen, spawn_point_x, level_y, *groups)
        self.set_character_size(screen, level_y, 50, 40)

        self.character_textures.update({
            self.IDLE_TILES: [
                pygame.image.load('./assets/adventurer/adventurer-idle-00.png'),
                pygame.image.load('./assets/adventurer/adventurer-idle-01.png'),
                pygame.image.load('./assets/adventurer/adventurer-idle-02.png'),
                pygame.image.load('./assets/adventurer/adventurer-idle-03.png')
            ],
            self.RUN_TILES: [
                pygame.image.load('./assets/adventurer/adventurer-run-00.png'),
                pygame.image.load('./assets/adventurer/adventurer-run-01.png'),
                pygame.image.load('./assets/adventurer/adventurer-run-02.png'),
                pygame.image.load('./assets/adventurer/adventurer-run-03.png'),
                pygame.image.load('./assets/adventurer/adventurer-run-04.png'),
                pygame.image.load('./assets/adventurer/adventurer-run-05.png'),
            ],
            self.JUMP_TILES: [
                pygame.image.load('./assets/adventurer/adventurer-jump-00.png'),
                pygame.image.load('./assets/adventurer/adventurer-jump-01.png'),
                pygame.image.load('./assets/adventurer/adventurer-jump-02.png'),
                pygame.image.load('./assets/adventurer/adventurer-jump-03.png')
            ],
            self.FALL_TILES: [
                pygame.image.load('./assets/adventurer/adventurer-fall-00.png'),
                pygame.image.load('./assets/adventurer/adventurer-fall-01.png')
            ]
        })
        self.IDLE_LENGTH = 4
        self.RUN_LENGTH = 6
        self.JUMP_LENGTH = 4
        self.FALL_LENGTH = 2
        self.image = self.get_current_tile()

    def move_to_click(self, clicker, dt):
        if clicker.position is not None:
            if fabs(self.position_x - clicker.position[0]) > self.MARGIN:
                self.is_facing_left = clicker.position[0] < self.position_x
                self.position_x = self.position_x + (
                        (self.walk_speed * dt) * (-1 if self.is_facing_left else 1))
                self.is_running = True
            else:
                clicker.position = None
                self.is_running = False

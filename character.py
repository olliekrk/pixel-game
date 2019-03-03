from math import floor, fabs

import pygame


class Character(object):
    TILES_IDLE_LEFT = 0
    TILES_IDLE_RIGHT = 1
    TILES_RUN_LEFT = 2
    TILES_RUN_RIGHT = 3

    SEQUENCE_LENGTH_IDLE = 4
    SEQUENCE_LENGTH_WALK = 6

    TILES_CHANGE_SPEED = 0.01
    WALK_SPEED = 100
    MARGIN = 3

    position_x = None
    position_y = None
    is_facing_left = False
    is_running = False

    textures = {
        TILES_IDLE_LEFT: [
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-idle-2-00.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-idle-2-01.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-idle-2-02.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-idle-2-03.png'), True, False)
        ],
        TILES_IDLE_RIGHT: [
            pygame.image.load('./assets/adventurer/adventurer-idle-2-00.png'),
            pygame.image.load('./assets/adventurer/adventurer-idle-2-01.png'),
            pygame.image.load('./assets/adventurer/adventurer-idle-2-02.png'),
            pygame.image.load('./assets/adventurer/adventurer-idle-2-03.png')
        ],
        TILES_RUN_LEFT: [
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-run-00.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-run-01.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-run-02.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-run-03.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-run-04.png'), True, False),
            pygame.transform.flip(pygame.image.load('./assets/adventurer/adventurer-run-05.png'), True, False)
        ],
        TILES_RUN_RIGHT: [
            pygame.image.load('./assets/adventurer/adventurer-run-00.png'),
            pygame.image.load('./assets/adventurer/adventurer-run-01.png'),
            pygame.image.load('./assets/adventurer/adventurer-run-02.png'),
            pygame.image.load('./assets/adventurer/adventurer-run-03.png'),
            pygame.image.load('./assets/adventurer/adventurer-run-04.png'),
            pygame.image.load('./assets/adventurer/adventurer-run-05.png'),
        ]
    }

    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y

    def get_tile(self):
        if self.is_running:
            sequence_frame = int((floor(pygame.time.get_ticks() * self.TILES_CHANGE_SPEED) % self.SEQUENCE_LENGTH_WALK))
            if self.is_facing_left:
                tiles = self.TILES_RUN_LEFT
            else:
                tiles = self.TILES_RUN_RIGHT
        else:
            sequence_frame = int((floor(pygame.time.get_ticks() * self.TILES_CHANGE_SPEED) % self.SEQUENCE_LENGTH_IDLE))
            if self.is_facing_left:
                tiles = self.TILES_IDLE_LEFT
            else:
                tiles = self.TILES_IDLE_RIGHT
        return self.textures[tiles][sequence_frame]

    def go_to(self, clicker, dt):
        if clicker.position is not None:
            if fabs(self.position_x - clicker.position[0]) > self.MARGIN:
                self.is_facing_left = clicker.position[0] < self.position_x
                self.position_x = self.position_x + ((self.WALK_SPEED * dt) * (-1 if self.is_facing_left else 1))
                self.is_running = True
            else:
                clicker.position = None
                self.is_running = False

from math import floor, fabs

import pygame


class Character(object):
    TILES_IDLE_LEFT = 0
    TILES_IDLE_RIGHT = 1
    TILES_RUN_LEFT = 2
    TILES_RUN_RIGHT = 3
    TILES_JUMP = 4
    TILES_FALL = 5

    SEQUENCE_LENGTH_IDLE = 4
    SEQUENCE_LENGTH_WALK = 6
    SEQUENCE_LENGTH_JUMP = 4
    SEQUENCE_LENGTH_FALL = 2

    TILES_CHANGE_SPEED = 0.01
    WALK_SPEED = 100

    BASE_VELOCITY = 14
    VELOCITY_DROP = 2
    velocity = BASE_VELOCITY

    MARGIN = 3

    position_x = None
    position_y = None

    is_facing_left = False
    is_running = False
    is_jumping = False

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
        ],
        TILES_JUMP: [
            pygame.image.load('./assets/adventurer/adventurer-jump-00.png'),
            pygame.image.load('./assets/adventurer/adventurer-jump-01.png'),
            pygame.image.load('./assets/adventurer/adventurer-jump-02.png'),
            pygame.image.load('./assets/adventurer/adventurer-jump-03.png')
        ],
        TILES_FALL: [
            pygame.image.load('./assets/adventurer/adventurer-fall-00.png'),
            pygame.image.load('./assets/adventurer/adventurer-fall-01.png')
        ]
    }

    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y
        self.default_y = y

    def get_tile(self):
        # character is jumping
        if self.is_jumping:
            # character is going up
            if self.velocity > 0:
                tiles = self.TILES_JUMP
                velocity_per_frame = 1 / (self.SEQUENCE_LENGTH_JUMP + 1)
                velocity_level = 1 - self.velocity / self.BASE_VELOCITY
                sequence_frame = min(int(floor(velocity_level / velocity_per_frame)), self.SEQUENCE_LENGTH_JUMP - 1)
            # character is falling
            else:
                tiles = self.TILES_FALL
                sequence_frame = int(
                    (floor(pygame.time.get_ticks() * self.TILES_CHANGE_SPEED) % self.SEQUENCE_LENGTH_FALL))

            image = self.textures[tiles][sequence_frame]

            if self.is_facing_left:
                return pygame.transform.flip(image, True, False)
            else:
                return image
        else:
            # character is running
            if self.is_running:
                sequence_length = self.SEQUENCE_LENGTH_WALK
                if self.is_facing_left:
                    tiles = self.TILES_RUN_LEFT
                else:
                    tiles = self.TILES_RUN_RIGHT
            # character is waiting
            else:
                sequence_length = self.SEQUENCE_LENGTH_IDLE
                if self.is_facing_left:
                    tiles = self.TILES_IDLE_LEFT
                else:
                    tiles = self.TILES_IDLE_RIGHT

            sequence_frame = int((floor(pygame.time.get_ticks() * self.TILES_CHANGE_SPEED) % sequence_length))
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

    def move_right(self, dt):
        self.is_running = True
        self.is_facing_left = False
        self.position_x += self.WALK_SPEED * dt

    def move_left(self, dt):
        self.is_running = True
        self.is_facing_left = True
        self.position_x -= self.WALK_SPEED * dt

    def jump(self):
        self.is_jumping = True

    def jump_loop(self):
        if self.is_jumping:
            self.position_y -= self.velocity

            self.velocity -= self.VELOCITY_DROP
            if self.velocity < -self.BASE_VELOCITY:
                self.velocity = -self.BASE_VELOCITY

            if self.position_y >= self.default_y:
                self.position_y = self.default_y
                self.is_jumping = False
                self.velocity = self.BASE_VELOCITY

    def wait(self):
        self.is_running = False

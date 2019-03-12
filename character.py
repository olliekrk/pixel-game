from random import randint
from math import floor

import pygame


class Character(pygame.sprite.DirtySprite):
    DEFAULT_WALK_SPEED = 150
    TILES_CHANGE_SPEED = 0.01
    BASE_VELOCITY = 10
    VELOCITY_DROP = 0.7
    MARGIN = 5

    def __init__(self, screen, spawn_point_x, level_y, *groups):
        super().__init__(*groups)

        self.character_width, self.character_height = None, None
        self.default_y = None
        self.position_y = None
        self.set_character_size(screen, level_y, 60, 60)

        self.walk_speed = self.DEFAULT_WALK_SPEED
        self.IDLE_TILES, self.IDLE_LENGTH = 1, 0
        self.RUN_TILES, self.RUN_LENGTH = 2, 0
        self.JUMP_TILES, self.JUMP_LENGTH = 3, 0
        self.FALL_TILES, self.FALL_LENGTH = 4, 0
        self.character_textures = {
            self.IDLE_TILES: [],
            self.RUN_TILES: [],
            self.JUMP_TILES: [],
            self.FALL_TILES: []
        }

        self.velocity = self.BASE_VELOCITY
        self.is_facing_left = False
        self.is_running = False
        self.is_jumping = False

        self.screen_x, self.screen_y = screen.get_width(), screen.get_height()
        self.position_x = spawn_point_x

        self.rect = None
        self.image = None
        self.update_rect()

    def set_character_size(self, screen, level_y, width, height):
        self.character_width, self.character_height = width, height
        self.default_y = screen.get_height() - self.character_height / 2.0 - level_y
        self.position_y = self.default_y

    def update_rect(self):
        self.rect = (
            self.position_x - self.character_width / 4,
            self.position_y - self.character_height / 2,
            self.character_width / 2,
            self.character_height
        )

    def get_current_tile(self):
        sequence_frame = None
        sequence_length = None

        # character is jumping
        if self.is_jumping:
            # character is going up
            if self.velocity > 0:
                tiles = self.JUMP_TILES
                velocity_per_frame = 1 / (self.JUMP_LENGTH + 1)
                velocity_level = 1 - self.velocity / self.BASE_VELOCITY
                sequence_frame = min(int(floor(velocity_level / velocity_per_frame)), self.JUMP_LENGTH - 1)
            # character is falling
            else:
                tiles = self.FALL_TILES
                sequence_length = self.FALL_LENGTH
        else:
            # character is running
            if self.is_running:
                tiles = self.RUN_TILES
                sequence_length = self.RUN_LENGTH
            # character is waiting
            else:
                tiles = self.IDLE_TILES
                sequence_length = self.IDLE_LENGTH

        if sequence_frame is None:
            sequence_frame = int((floor(pygame.time.get_ticks() * self.TILES_CHANGE_SPEED) % sequence_length))

        image = self.character_textures[tiles][sequence_frame]
        image = pygame.transform.scale(image, (self.character_width, self.character_height))

        if self.is_facing_left:
            image = pygame.transform.flip(image, True, False)

        self.image = image
        return image

    def move_right(self, dt):
        self.is_running = True
        self.is_facing_left = False
        if self.position_x < self.screen_x:
            self.position_x += self.walk_speed * dt

    def move_left(self, dt):
        self.is_running = True
        self.is_facing_left = True
        if self.position_x > 0:
            self.position_x -= self.walk_speed * dt

    def jump(self):
        self.is_jumping = True

    def jump_loop(self):
        self.position_y -= self.velocity
        self.velocity -= self.VELOCITY_DROP
        # if maximum falling velocity is reached
        if self.velocity < -self.BASE_VELOCITY:
            self.velocity = -self.BASE_VELOCITY
        # if we already hit the ground
        if self.position_y >= self.default_y:
            self.position_y = self.default_y
            self.is_jumping = False
            self.velocity = self.BASE_VELOCITY

    def stop_running(self):
        self.is_running = False

    def update(self, *args):
        self.update_rect()
        self.get_current_tile()
        self.dirty = 1

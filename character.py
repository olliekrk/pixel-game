from random import randint
from math import floor

import pygame


class Character(pygame.sprite.DirtySprite):
    SPAWN_TICKS = 200
    DEFAULT_WALK_SPEED = 200
    TILES_CHANGE_SPEED = 0.012
    BASE_VELOCITY = 8
    VELOCITY_DROP = 0.5
    MARGIN = 3

    def __init__(self, screen, spawn_point_x, level_y, *groups):
        super().__init__(*groups)

        # position
        self.character_width, self.character_height = None, None
        self.default_y = None
        self.position_y = None
        self.set_character_size(screen, level_y, 120, 120)

        self.screen_x, self.screen_y = screen.get_width(), screen.get_height()
        self.position_x = spawn_point_x

        # textures
        self.walk_speed = self.DEFAULT_WALK_SPEED
        self.IDLE_TILES, self.IDLE_LENGTH = 1, 0
        self.RUN_TILES, self.RUN_LENGTH = 2, 0
        self.JUMP_TILES, self.JUMP_LENGTH = 3, 0
        self.FALL_TILES, self.FALL_LENGTH = 4, 0
        self.SPAWN_TILES, self.SPAWN_LENGTH = 5, 0

        self.character_textures = {
            self.IDLE_TILES: [],
            self.RUN_TILES: [],
            self.JUMP_TILES: [],
            self.FALL_TILES: []
        }

        self.rect = None
        self.image = None
        self.set_rect()

        # movement
        self.velocity = self.BASE_VELOCITY
        self.is_facing_left = False
        self.is_running = False
        self.is_jumping = False

        # game stats
        self.health_points = 0
        self.attack_points = 0
        self.alive_time = pygame.time.get_ticks()

    def set_character_size(self, screen, level_y, width, height):
        self.character_width, self.character_height = width, height
        self.default_y = screen.get_height() - self.character_height - level_y
        self.position_y = self.default_y

    def set_rect(self):
        self.rect = pygame.Rect(self.position_x, self.position_y, self.character_width / 2, self.character_height / 2)

    def set_current_image(self):
        sequence_frame = None
        sequence_length = None

        # spawn animation
        if pygame.time.get_ticks() - self.alive_time < self.SPAWN_TICKS \
                and self.SPAWN_LENGTH > 0:
            tiles = self.SPAWN_TILES
            sequence_length = self.SPAWN_LENGTH
        else:
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

    def move_right(self, dt):
        self.is_running = True
        self.is_facing_left = False
        self.position_x += self.walk_speed * dt
        self.position_x = min(self.position_x, self.screen_x - self.character_width / 2)  # not to leave the screen

    def move_left(self, dt):
        self.is_running = True
        self.is_facing_left = True
        self.position_x -= self.walk_speed * dt
        self.position_x = max(self.position_x, - self.character_width / 2)  # not to leave the screen

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
        self.set_rect()
        self.set_current_image()
        self.dirty = 1

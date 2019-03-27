import sys
from random import randint

import pygame

import adventurer
import clicker
import level
import monster


class Game(object):
    ENEMIES_LIMIT = 10
    SPAWN_BORDER = 20
    alive_characters = pygame.sprite.LayeredDirty()
    alive_enemies = pygame.sprite.LayeredDirty()

    def __init__(self, level_name, game_screen, game_clock):
        self.fps = 90
        self.done = False
        self.screen = game_screen
        self.screen_width, self.screen_height = game_screen.get_size()
        self.clock = game_clock
        self.click_pointer = clicker.Clicker()
        self.level = level.Level(level_name, self.screen_width, self.screen_height)
        self.player = adventurer.Adventurer(self.screen, 0, self.level.floor)
        self.alive_characters.add(self.player)

    def game_loop(self):
        self.alive_characters.clear(self.screen, self.level.background)
        while not self.done:
            dt = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.spawn_enemies()
            self.draw_characters(dt)
            self.update_player_position(dt)
            self.check_for_player_collisions()
        sys.exit()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_pointer.click(pygame.mouse.get_pos())

    def update_player_position(self, dt):
        # moving with mouse
        if self.click_pointer.position is not None:
            self.player.move_to_click(self.click_pointer, dt)
        # moving with arrows
        else:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP] and not self.player.is_jumping:
                self.player.jump()
            if self.player.is_jumping:
                self.player.jump_loop()
            if keys_pressed[pygame.K_RIGHT]:
                self.player.move_right(dt)
            elif keys_pressed[pygame.K_LEFT]:
                self.player.move_left(dt)
            else:
                self.player.stop_running()

    def spawn_enemies(self):
        if len(self.alive_enemies.sprites()) < self.ENEMIES_LIMIT:
            spawn_location = randint(-self.SPAWN_BORDER, 0)
            spawn_side = randint(0, 1)

            # spawn on the right side, otherwise on left
            if spawn_side == 1:
                spawn_location = self.screen_width - 2 * self.SPAWN_BORDER

            monster.Monster(self.screen,
                            spawn_location,
                            self.level.floor,
                            self.alive_enemies,
                            self.alive_characters)

    def draw_characters(self, dt):
        self.alive_characters.update(self.player.position_x, dt)
        dirty_rects = self.alive_characters.draw(self.screen)
        pygame.display.update(dirty_rects)

    def check_for_player_collisions(self):
        pygame.sprite.spritecollide(self.player, self.alive_enemies, True)

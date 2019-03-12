import sys

import pygame

import adventurer
import clicker
import level
import monster


class Game(object):
    ENEMIES_LIMIT = 1
    alive_characters = pygame.sprite.LayeredDirty()
    alive_enemies = pygame.sprite.LayeredDirty()

    def __init__(self, level_name, game_resolution, game_clock):
        self.ENEMIES_COUNT = 0
        self.fps = 60
        self.done = False
        self.screen = game_resolution
        self.clock = game_clock
        self.click_pointer = clicker.Clicker()
        self.screen_width, self.screen_height = game_resolution.get_size()
        self.level = level.Level(level_name, (self.screen_width, self.screen_height))
        self.player = adventurer.Adventurer(self.screen, 0, self.level.FLOOR)
        self.alive_characters.add(self.player)

    def game_loop(self):
        dt = 0
        while not self.done:
            self.event_loop()
            self.spawn_enemies()
            self.draw_level()
            self.draw_characters(dt)
            self.update_player_position(dt)
            dt = self.clock.tick(self.fps) / 1000.0
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

        self.player.update_rect()

    def spawn_enemies(self):
        if self.ENEMIES_COUNT < self.ENEMIES_LIMIT:
            monster.Monster(self.screen, 0, self.level.FLOOR, self.alive_characters, self.alive_enemies)
            self.ENEMIES_COUNT += 1

    def draw_level(self):
        self.level.draw_background(self.screen)
        self.level.draw_foreground(self.screen)

    def draw_characters(self, dt):
        target_x = self.player.position_x
        self.alive_characters.update(target_x, dt)
        dirty_rects = self.alive_characters.draw(self.screen)
        pygame.display.update(dirty_rects)

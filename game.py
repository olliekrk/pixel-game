import sys

import pygame

import adventurer
import clicker


class Game(object):
    # TODO: add rendering 'dirty' rectangles
    RENDER_AROUND_ADVENTURER_SIZE = 100

    def __init__(self, level, game_resolution, game_clock):
        self.fps = 60
        self.done = False
        self.level = level
        self.screen = game_resolution
        self.clock = game_clock
        self.click_pointer = clicker.Clicker()
        self.screen_width, self.screen_height = game_resolution.get_size()
        self.adventurer = adventurer.Adventurer(self.screen, self.level.FLOOR)
        self.RENDER_AROUND_ADVENTURER_SIZE = self.adventurer.HEIGHT * 3

    def game_loop(self):
        dt = 0
        self.initial_draw()
        while not self.done:
            self.event_loop()
            self.update_position(dt)
            self.draw()
            dt = self.clock.tick(self.fps) / 1000.0
        sys.exit()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click_pointer.click(pygame.mouse.get_pos())

    def update_position(self, dt):
        # moving with mouse
        if self.click_pointer.position is not None:
            self.adventurer.move_to_click(self.click_pointer, dt)

        # moving with arrows
        else:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP] and not self.adventurer.is_jumping:
                self.adventurer.jump()
            if self.adventurer.is_jumping:
                self.adventurer.jump_loop()
            if keys_pressed[pygame.K_RIGHT]:
                self.adventurer.move_right(dt)
            elif keys_pressed[pygame.K_LEFT]:
                self.adventurer.move_left(dt)
            else:
                self.adventurer.wait()

        self.adventurer.update_hitbox()

    def initial_draw(self):
        self.level.draw_background(self.screen)
        self.adventurer.draw_adventurer(self.screen)
        self.level.draw_foreground(self.screen)
        pygame.display.flip()

    def draw(self):
        self.level.draw_background(self.screen)
        self.adventurer.draw_adventurer(self.screen)
        self.level.draw_foreground(self.screen)
        update_rectangle = pygame.Rect(self.adventurer.position_x - self.RENDER_AROUND_ADVENTURER_SIZE,
                                       self.adventurer.position_y - self.RENDER_AROUND_ADVENTURER_SIZE,
                                       2 * self.RENDER_AROUND_ADVENTURER_SIZE,
                                       2 * self.RENDER_AROUND_ADVENTURER_SIZE)
        pygame.display.update(update_rectangle)

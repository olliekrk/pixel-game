import sys

import pygame

import character
import clicker


class Game(object):
    RENDER_AROUND_CHARACTER_SIZE = 50

    def __init__(self, level, game_resolution, game_clock):
        self.fps = 60
        self.done = False
        self.level = level
        self.screen = game_resolution
        self.clock = game_clock
        self.click_pointer = clicker.Clicker()
        (self.screen_width, self.screen_height) = game_resolution.get_size()
        self.character = character.Character(self.screen_width / 2, self.screen_height - self.level.FLOOR)

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
            self.character.go_to(self.click_pointer, dt)

        else:
            # moving with arrows
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP] and not self.character.is_jumping:
                self.character.jump()
            if keys_pressed[pygame.K_RIGHT]:
                self.character.move_right(dt)
            elif keys_pressed[pygame.K_LEFT]:
                self.character.move_left(dt)
            else:
                self.character.wait()

        self.character.jump_loop()

    def initial_draw(self):
        self.level.draw_background(self.screen)
        self.draw_character()
        self.level.draw_foreground(self.screen)
        pygame.display.flip()

    def draw(self):
        self.level.draw_background(self.screen)
        self.draw_character()
        self.level.draw_foreground(self.screen)
        update_rectangle = pygame.Rect(self.character.position_x - self.RENDER_AROUND_CHARACTER_SIZE,
                                       self.character.position_y - self.RENDER_AROUND_CHARACTER_SIZE,
                                       2 * self.RENDER_AROUND_CHARACTER_SIZE,
                                       2 * self.RENDER_AROUND_CHARACTER_SIZE)
        pygame.display.update(update_rectangle)

    def draw_character(self):
        self.screen.blit(self.character.get_tile(), (self.character.position_x, self.character.position_y))

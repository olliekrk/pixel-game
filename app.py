import os

import pygame

import game
import level

TITLE = "My Pixel Game"
RESOLUTION = (900, 600)
pygame.init()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.display.set_caption(TITLE)

    game_resolution = pygame.display.set_mode(RESOLUTION)
    game_clock = pygame.time.Clock()

    game.Game(level.Level("whisky", game_resolution), game_resolution, game_clock).game_loop()

    pygame.quit()

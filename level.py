import pygame


class Level(object):
    resolution = None
    background_color = None
    background_images = None
    foreground_images = None

    def __init__(self, name, screen_width, screen_height, floor=50):
        self.floor = floor
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_images = [
            pygame.image.load('./assets/forest/Layer_0010_1.png'),
            pygame.image.load('./assets/forest/Layer_0009_2.png'),
            pygame.image.load('./assets/forest/Layer_0008_3.png'),
            pygame.image.load('./assets/forest/Layer_0007_Lights.png'),
            pygame.image.load('./assets/forest/Layer_0006_4.png'),
            pygame.image.load('./assets/forest/Layer_0005_5.png')
        ]
        self.foreground_images = [
            pygame.image.load('./assets/forest/Layer_0004_Lights.png'),
            pygame.image.load('./assets/forest/Layer_0003_6.png'),
            pygame.image.load('./assets/forest/Layer_0002_7.png'),
            pygame.image.load('./assets/forest/Layer_0001_8.png'),
            pygame.image.load('./assets/forest/Layer_0000_9.png')
        ]
        self.background, self.foreground = None, None
        self.set_foreground()
        self.set_background()

    def set_background(self):
        self.background = pygame.Surface((self.screen_width, self.screen_height))  #
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        for image in self.background_images:
            self.background.blit(pygame.transform.scale(image, (self.screen_width, self.screen_height)), (0, 0))
        self.background.blit(self.foreground, (0, 0))

    def set_foreground(self):
        self.foreground = pygame.Surface((self.screen_width, self.screen_height))
        self.foreground = self.foreground.convert()
        for image in self.foreground_images:
            self.foreground.blit(pygame.transform.scale(image, (self.screen_width, self.screen_height)), (0, 0))

import pygame


class Level(object):
    RESOLUTION = (900, 600)
    background_color = None
    background_images = None
    foreground_images = None

    FLOOR = 50  # where the character should be standing on current floor

    def __init__(self):
        self.background_images = [
            # pygame.image.load('./assets/forest/Layer_0010_1.png'),
            # pygame.image.load('./assets/forest/Layer_0009_2.png'),
            # pygame.image.load('./assets/forest/Layer_0008_3.png'),
            # pygame.image.load('./assets/forest/Layer_0007_Lights.png'),
            # pygame.image.load('./assets/forest/Layer_0006_4.png'),
            pygame.image.load('./assets/forest/Layer_0005_5.png')
        ]
        self.foreground_images = [
            # pygame.image.load('./assets/forest/Layer_0004_Lights.png'),
            pygame.image.load('./assets/forest/Layer_0003_6.png'),
            pygame.image.load('./assets/forest/Layer_0002_7.png'),
            pygame.image.load('./assets/forest/Layer_0001_8.png'),
            pygame.image.load('./assets/forest/Layer_0000_9.png')
        ]

    def draw_background(self, screen):
        screen.fill((0, 0, 0))
        for image in self.background_images:
            screen.blit(pygame.transform.scale(image, (900, 600)), (0, 0))

    def draw_foreground(self, screen):
        for image in self.foreground_images:
            screen.blit(pygame.transform.scale(image, (900, 600)), (0, 0))

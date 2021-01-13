import pygame


class Paddle(pygame.sprite.Sprite):

    def __init__(self):
        super(Paddle, self).__init__()
        self.paddle_width = 300
        self.paddle_height = 20
        self.image = pygame.transform.scale(pygame.image.load("data/paddle.png"), (self.paddle_width, self.paddle_height))
        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

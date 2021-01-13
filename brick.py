import pygame

image = pygame.image.load("./data/brick.jpg")


class Brick(pygame.sprite.Sprite):
    def __init__(self, brick_width, brick_height):
        super(Brick, self).__init__()
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.image = pygame.transform.scale(pygame.image.load("./data/brick.jpg"), (self.brick_width, self.brick_height))
        self.rect = self.image.get_rect()

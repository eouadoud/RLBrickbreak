from main import *
from graphicalItems import *


class Player(pygame.sprite.Sprite):
    """ Player object """

    # constructor

    def __init__(self, x, y):
        # what the heck is this for?
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_item_image('paddle.png')
        self.rect.x = x
        self.rect.y = y
        pygame.sprite.Sprite.__init__(self)

    # paddle's move function

    def move(self, dirx):
        self.rect.x += dirx
        # make sure paddle can't go off screen
        if self.rect.x < 0:
            self.rect.x = 1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

from main import *
from graphicalItems import *


class Brick(pygame.sprite.Sprite):
    """ brick object """

    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_item_image('brick.png')
        self.rect.x = posx
        self.rect.y = posy
        pygame.sprite.Sprite.__init__(self)

import os
import pygame


##fonction chargement de l'image d'objet (Bale, Barre, brick)
def load_item_image(name):
    """ load image and return image object """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit() + message
    return image, image.get_rect()

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print("couldn't load module.")
    sys.exit(2)

##fonction chargement de l'image d'objet (Bale, Barre, brick)
def load_item_image(name):
    fileName = os.path.join('data', name)
    try:
        image = pygame.image.load(fileName)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fileName)
    raise SystemExit(message)
    return image, image.get_rect()

from main import *


##fonction chargement de l'image d'objet (Bale, Barre, brick)
def load_item_image(name):
    global message
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

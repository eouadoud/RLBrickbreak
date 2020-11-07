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


class Brick(pygame.sprite.Sprite):
    ## Représentation des bricks
    def __init__(self, pos_x, pos_y, bricks):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_item_image('brick.png')
        self.rect.x = pos_x
        self.rect.y = pos_y
        pygame.sprite.Sprite.__init__(self, bricks)

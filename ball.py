from main import *
from graphicalItems import *


class Ball(pygame.sprite.Sprite):
    """ ball object to control movement and collision """

    # constructor
    def __init__(self, x, y, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_item_image('ball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0
        self.oob = False
        self.rect.x = x
        self.rect.y = y

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        # if the display screen does not contain the ball's new position
        if not self.area.contains(newpos):
            # is ball's new position topleft corner not contained in the display screen?
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            # if both ball's top right and top left corners are not in the display's area, collision with top, bounce ball horizontally
            if tr and tl:
                angle = -angle
            if tl and bl:
                angle = math.pi - angle
            if tr and br:
                angle = math.pi - angle
            if bl and br:
                self.oob = True

        # check for collision with paddle
        if self.rect.colliderect(self.rect):
            # fix ball's y
            self.rect.y = self.rect.y - self.rect.height
            # horizontal bounce
            angle = -angle
        # check for collision with bricks
        for brick in pygame.sprite.Group():
            if self.rect.colliderect(brick.rect) == 1 and not self.hit:
                pygame.sprite.Group().remove(brick)
                pygame.sprite.Group().remove(brick)
                quad = ((angle * (180 / math.pi)) % 360) // 90
                bt = Rect(brick.rect.x, brick.rect.y, brick.rect.width, 1)
                bb = Rect(brick.rect.x, brick.rect.y +
                          brick.rect.height, brick.rect.width, 1)
                bl = Rect(brick.rect.x, brick.rect.y, 1,
                          brick.rect.y + brick.rect.height)
                br = Rect(brick.rect.x + brick.rect.width, brick.rect.y,
                          1, brick.rect.y + brick.rect.height)
                if self.rect.colliderect(bt):
                    # handle top left corner
                    if self.rect.colliderect(bl):
                        # if both top and left are colliding....
                        print("hit brick top and left")
                        # if more ball x is overlapping than ball y, horiz bounce
                        if abs(self.rect.centerx - brick.rect.left) > abs(self.rect.centery - brick.rect.top):
                            angle = math.pi - angle
                            # reset the y position of the ball so ball is not inside the brick
                            self.rect.y = brick.rect.y - self.rect.height - 1
                        # if more ball y is overlapping than ball x, vert bounce
                        elif abs(self.rect.centerx - brick.rect.left) < abs(self.rect.centery - brick.rect.top):
                            angle = -angle
                            # set the ball's x value so we are not inside the brick
                            self.rect.x = brick.rect.x - self.rect.width - 1
                        elif quad == 2:
                            angle = angle - math.pi
                            self.rect.y = brick.rect.y - self.rect.height
                            self.rect.x = brick.rect.x - self.rect.width
                            print("hit brick top and left perfectly")
                        else:
                            angle = -angle
                    # handle top right corner
                    elif self.rect.colliderect(br):
                        # if both top and right are colliding...
                        print("hit brick top and right")
                        # if more ball x overlaps brick than ball y, horiz bounce
                        if abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.top):
                            angle = math.pi - angle
                            # reset the ball's y so as to not overlap brick
                            self.rect.y = brick.rect.y - self.rect.height
                        # if more ball y overlaps brick than ball x, vert bounce
                        elif abs(self.rect.centerx - brick.rect.right) < abs(self.rect.centery - brick.rect.top):
                            angle = -angle
                            # reset the ball's x so as to not overlap brick
                            self.rect.x = brick.rect.right + 1
                        else:
                            print("hit brick top and right perfectly")
                            angle = angle - math.pi
                            self.rect.y = brick.rect.y - self.rect.height
                            self.rect.x = brick.rect.right + 1
                    else:
                        angle = -angle
                        self.rect.y = brick.rect.y - self.rect.height - 1
                        print("hit brick top")
                    self.hit = not self.hit

                if self.rect.colliderect(bb):
                    # handle bottom left corner
                    if self.rect.colliderect(bl):
                        print("hit brick bottom and left")
                        # if both bottom and left are colliding...
                        # if more ball x overlaps than y, horiz bounce
                        if abs(self.rect.centerx - brick.rect.left) > abs(self.rect.centery - brick.rect.bottom):
                            angle = math.pi - angle
                            # reset the ball's y
                            self.rect.y = brick.rect.bottom + 1
                        # if more ball y overlaps brick than x, vert bounce
                        elif abs(self.rect.centerx - brick.rect.left) < abs(self.rect.centery - brick.rect.bottom):
                            angle = -angle
                            # reset ball's x
                            self.rect.x = brick.rect.x - self.rect.width - 1
                        else:
                            print("hit brick bottom and left perfectly")
                            angle = angle - math.pi
                            self.rect.y = brick.rect.bottom + 1
                            self.rect.x = brick.rect.x - self.rect.width - 1
                    # handle bottom right corner
                    elif self.rect.colliderect(br):
                        print("hit brick bottom and right")
                        # if both bottom and right are colliding...
                        # if more ball x overlaps brick than y, horiz bounce
                        if abs(self.rect.centerx - brick.rect.right) > abs(self.rect.centery - brick.rect.bottom):
                            angle = math.pi - angle
                            # set ball's y value
                            self.rect.y = brick.rect.bottom + 1
                        # if more ball y overlaps brick than ball x, vert bounce
                        elif abs(self.rect.centerx - brick.rect.right) < abs(self.rect.centery - brick.rect.bottom):
                            angle = -angle
                            # reset ball's x
                            self.rect.x = brick.rect.right + 1
                        else:
                            print("hit brick bottom and right perfectly")
                            angle = angle - math.pi
                            self.rect.x = brick.rect.right + 1
                            self.rect.y = brick.rect.bottom + 1
                    else:
                        angle = -angle
                        # reset ball's y
                        self.rect.y = brick.rect.bottom + 1
                        print("hit brick bottom")
                    self.hit = not self.hit
                if self.rect.colliderect(br) and not self.hit:
                    print("hit right")
                    angle = math.pi - angle
                    self.hit = not self.hit
                    self.rect.x = brick.rect.right + 1
                elif self.rect.colliderect(bl) and not self.hit:
                    print("hit left")
                    angle = math.pi - angle
                    self.hit = not self.hit
                    self.rect.x = brick.rect.x - 1

            elif self.hit:
                self.hit = not self.hit

        # update the ball's vector
        self.vector = (angle, z)

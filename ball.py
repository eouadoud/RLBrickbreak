import pygame
import random
from paddle import Paddle


class Ball(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Ball, self).__init__()
        self.ball_width = 25
        self.ball_height = 25
        self.image = pygame.transform.scale(pygame.image.load("./data/basketball.png"), (self.ball_width, self.ball_height))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.speed = 0
        self.direction = 1
        self.count = 4
        self.reset(x, y)

    def reset(self, x, y):
        random_number = [-1, 1]
        self.rect.x = x
        self.rect.y = y
        self.speed = random.choice(random_number)
        self.direction = 2
        self.count -= 1

    def wall_bounce(self):
        self.direction = -self.direction
        self.speed *= 1.01

    def right_bounce(self):
        self.speed = -self.speed
        self.direction = -self.direction

    def left_bounce(self):
        self.speed = -self.speed

        self.speed *= 1.01

    # def __init__(self, vector):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = pygame.transform.scale(pygame.image.load("basketball.png"), (25, 25))
    #     self.rect = self.image.get_rect()
    #     screen = pygame.display.get_surface()
    #     self.area = screen.get_rect()
    #     self.vector = vector
    #     self.hit = 0

    def update(self, x, y):

        # direction_radians = math.radians(self.direction)
        # self.rect.x += self.speed * math.sin(direction_radians)
        # self.rect.y += self.speed * math.cos(direction_radians)

        self.rect.x += self.speed
        self.rect.y -= self.direction

        if self.rect.y > self.screenheight:
            if self.count > 0:
                self.reset(x, y)

        if self.rect.y < 0:
            self.direction = -self.direction

        if self.rect.x <= 0:
            self.speed = -self.speed

        if self.rect.x > self.screenwidth - self.rect.width:
            self.speed = -self.speed

    # def move(self):
    #     self.rect.x += ball_speed_x
    #     self.rect.y += ball_speed_y
    #     if self.rect.x >= 1000 or self.rect.x <= 0:
    #         self.rect.x += -ball_speed_x
    #     if self.rect.y >= 500 or self.rect.y <=0:
    #         self.rect.y += ball_speed_y

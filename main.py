#!/usr/bin/env python
#
# brick break game
#
# OUADOUD and SAIDI  and FAHRAOUI , 20/10/2020

# Full playable

# Constants

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640
PLAYER_HEIGHT = 8
PLAYER_WIDTH = 85
PLAYER_SPEED = 5
BALL_WIDTH = 11
BALL_HEIGHT = 11
SCORE = 0
LIVES = 3


try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from graphicalItems import *
    from player import *
    from ball import *
    from level import *
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('b r i c k b r e a k e r')

    # fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    make_level(level)

    # initialize player
    player = Player((SCREEN_WIDTH / 2) - (PLAYER_WIDTH / 2),
                    SCREEN_HEIGHT - PLAYER_HEIGHT)
    pygame.sprite.Group().add(player)

    # initialize ball
    speed = 4
    rand = ((0.1*(random.randint(5, 8))))
    ball = Ball(player.rect.centerx - (BALL_WIDTH / 2), player.rect.y - BALL_HEIGHT, (.743723, speed))
    pygame.sprite.Group().add(ball)


    # blit background to screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # initialize clock
    clock = pygame.time.Clock()

    # event loop
    while 1:
        # controls the speed at which the game run (fps)
        clock.tick(120)

        # keyboard input
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        # get list of keys, handle input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED)

        # clear screen to produce illusion of animation
        screen.fill((0, 0, 0))

        # blit all sprites (can we do this another way? ie, only draw sprites when they are needed?) blitting is resource intensive
        # for sprite in all_sprites_list:
        #	screen.blit(background, sprite.rect, sprite.rect)
        # check for movement of ball
        pygame.sprite.RenderPlain(ball).update()
        if ball.oob:
            print("ball out of bounds. you suck")
            #lives -= 1
            # reset()
            break

        # why is this here?
        pygame.sprite.Group().draw(screen)

        # And this?
        pygame.display.flip()


if __name__ == '__main__':
    main()
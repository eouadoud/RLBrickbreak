import pygame
from text import text_to_screen

pygame.init()

screen_width = 1500
screen_height = 700
screen_gameover = pygame.display.set_mode((screen_width, screen_height))

black = (0, 0, 0)
# white = (255, 255, 255)

clock = pygame.time.Clock()


def gameover_screen():

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            run = False
        # if keys[pygame.K_r]:
        #     game_init()

        screen_gameover.fill(black)
        text_to_screen(screen_gameover, "Game Over", screen_width/2 - 100, screen_height/2-100)
        text_to_screen(screen_gameover, "Press c to restart", screen_width / 2 - 150, screen_height / 2)
        pygame.display.update()
        clock.tick(60)

import pygame

from game_run import game_init
from startscreen import start_screen

pygame.init()
screen_width = 1500
screen_height = 700
screen_start = pygame.display.set_mode((screen_width, screen_height))


def main():
    start_screen()
    run = True
    black = (0, 0, 0)
    screen_start.fill(black)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_init()


main()

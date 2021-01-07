import pygame
from text import text_to_screen

pygame.init()

screen_width = 1500
screen_height = 700
screen_start = pygame.display.set_mode((screen_width, screen_height))

black = (0, 0, 0)
# white = (255, 255, 255)

clock = pygame.time.Clock()


def start_screen():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_c]:
            run = False
        screen_start.fill(black)
        text_to_screen(screen_start, "Welcome to Brick Breaker", screen_width / 2 - 200, screen_height / 2 - 200)
        text_to_screen(screen_start, "Press c to start", screen_width / 2 - 150, screen_height / 2 - 50)
        pygame.display.update()
        clock.tick(60)


start_screen()

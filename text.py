import pygame


def text_to_screen(surface, text, x, y):
    # set size of text
    size = 30

    # set color
    color = (255, 255, 255)

    # try to update and print text
    try:

        # print text
        text = str(text)

        # set font
        font = pygame.font.Font("Roboto-Regular.ttf", size)

        # render text
        text = font.render(text, True, color)

        # print to screen
        surface.blit(text, (x, y))

    # prints Error if there is an error
    except:
        print("Error")

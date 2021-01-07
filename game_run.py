import pygame
from brick import Brick
from ball import Ball
from paddle import Paddle
from text import text_to_screen

from gameover import gameover_screen


def game_init():
    black = (0, 0, 0)

    pygame.init()
    run = True
    screen_width = 1500
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    all_sprites_list = pygame.sprite.Group()

    bricks_list = pygame.sprite.Group()
    for i in range(0, 12):
        for j in range(0, 5):
            bricks = Brick(100, 25)

            bricks.rect.x = (screen_width - 1300) + (i * 100)
            bricks.rect.y = (screen_height - 600) + (j * 50)

            bricks_list.add(bricks)
            all_sprites_list.add(bricks)

    paddle_list = pygame.sprite.Group()
    paddle = Paddle()
    paddle.rect.x = screen_width / 2
    paddle.rect.y = screen_height - 20
    paddle_list.add(paddle)
    all_sprites_list.add(paddle)

    ball = Ball(paddle.rect.x + paddle.paddle_width / 2, paddle.rect.y - (paddle.paddle_height + 10))
    ball.count = 4
    all_sprites_list.add(ball)

    clock = pygame.time.Clock()
    while run:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:

            paddle.moveLeft(5)

            if paddle.rect.x <= 0:
                paddle.rect.x = 0

        if keys[pygame.K_RIGHT]:

            paddle.moveRight(5)

            if paddle.rect.x >= screen_width - paddle.paddle_width:
                paddle.rect.x = screen_width - paddle.paddle_width

        # ball.update(paddle.rect.x, paddle.rect.y)

        if pygame.sprite.spritecollide(ball, bricks_list, True):

            if ball.speed > 0:
                ball.wall_bounce()

            if ball.speed < 0:
                ball.wall_bounce()

        if pygame.sprite.spritecollide(ball, paddle_list, False):

            if ball.speed > 0:
                if ball.rect.x + ball.ball_width / 2 < paddle.rect.x + paddle.paddle_width / 2:
                    ball.left_bounce()
                if ball.rect.x + ball.ball_width / 2 == paddle.rect.x + paddle.paddle_width / 2:
                    ball.wall_bounce()
                if ball.rect.x + ball.ball_width / 2 > paddle.rect.x + paddle.paddle_width / 2:
                    ball.wall_bounce()
            if ball.speed < 0:
                if ball.rect.x + ball.ball_width / 2 < paddle.rect.x + paddle.paddle_width / 2:
                    ball.wall_bounce()
                if ball.rect.x + ball.ball_width / 2 == paddle.rect.x + paddle.paddle_width / 2:
                    ball.wall_bounce()
                if ball.rect.x + ball.ball_width / 2 > paddle.rect.x + paddle.paddle_width / 2:
                    ball.right_bounce()
        if ball.count == 0:
            run = False
            gameover_screen()

        if not bricks_list:
            run = False
            gameover_screen()

        all_sprites_list.update(paddle.rect.x + paddle.paddle_width / 2, paddle.rect.y - (paddle.paddle_height + 10))
        all_sprites_list.draw(screen)
        text_to_screen(screen, "Balls left: " + str(ball.count - 1), 10, 10)
        pygame.display.flip()
        clock.tick(120)

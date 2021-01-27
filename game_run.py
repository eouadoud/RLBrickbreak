import atexit
import random
import sys

import numpy as np
import pygame

grey_bc = [180, 180, 180]
brown_color = [120, 80, 60]

block_width = 60
block_height = 12

fname = 'RL_Brik_Breaker'

resolution = 10
alpha = 0.5
lmbd = 0.9

STATES = {
    'Alive': 0,
    'Dead': -100,
    'Scores': 10,
    'Hit': 1
}

ball_radius = 10
paddle_width = 80
paddle_height = 10


class Brick():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, block_width, block_height)


class Envirement(object):

    def __init__(self, data):

        self.highscore = 0
        self.isAuto = True
        self.command = 0
        self.iteration = 0
        self.Q = np.zeros((1280 // resolution, 480 // resolution, 3))

        if data is not None:
            try:
                self.iteration = int(data['iter'])
                self.highscore = int(data['high'])
                self.Q = data['trainedQ']
            except:
                print("Can't load data from input file, wrong format.")
                raise

        pygame.init()

        pygame.key.set_repeat(1, 0)

        self.resetGame()

        self.screen = pygame.display.set_mode([800, 480])
        self.myfont = pygame.font.SysFont("Arial", 30)

    def initBricks(self):
        self.bricks = []
        for i in range(1, 9):
            for j in range(1, 5):
                temp = Brick(90 * i - 35, 50 + 20 * j)
                self.bricks.append(temp)

    def resetGame(self):

        self.ball_x = 300
        self.ball_y = 450 - ball_radius
        self.ball_speed_x = 3
        self.ball_speed_y = 5

        self.randomAngle()

        self.paddle_x = 300
        self.paddle_y = 470
        self.paddle_speed = 10

        self.com_vec = 0

        self.score = 0
        self.ball_hit_count = 0
        self.paddle_hit_count = 0

        self.initBricks()

    def update(self):

        if self.paddle_x < 0:
            self.paddle_x = 0

        if self.paddle_x > self.screen.get_width() - paddle_width:
            self.paddle_x = self.screen.get_width() - paddle_width

        self.current_reward = STATES['Alive']
        # Mouvement du ballon
        self.ball_y += self.ball_speed_y
        self.ball_x += self.ball_speed_x

        self.hitDetect()

    def randomAngle(self):
        self.ball_y = 450 - ball_radius
        ran = random.randint(0, 4)
        self.ball_speed_x = (7 - ran) * self.ball_speed_x / abs(self.ball_speed_x)
        self.ball_speed_y = (3 + ran) * self.ball_speed_y / abs(self.ball_speed_y)
        self.ball_hit_count = 0

    def hitDetect(self):
        ##Detections des collisions
        ball_rect = pygame.Rect(self.ball_x - ball_radius, self.ball_y - ball_radius, ball_radius * 2,
                                ball_radius * 2)
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, paddle_width, paddle_height)

        # vérification si la balle touche le bas (perte)
        if self.ball_y > self.screen.get_height() - ball_radius:
            self.current_reward = STATES['Dead']
            self.iteration += 1
            s = 'Iteration: ' + repr(self.iteration) + ', score : ' + repr(self.score) + ', hits: ' + repr(
                self.paddle_hit_count)

            if self.score > self.highscore:
                self.highscore = self.score
                s += ' Nouveau score!'

            print(s)
            self.resetGame()

        # border de la vue
        if self.ball_y < ball_radius:
            self.ball_y = ball_radius
            self.ball_speed_y = -self.ball_speed_y

        if self.ball_x < ball_radius:
            self.ball_x = ball_radius
            self.ball_speed_x = -self.ball_speed_x
        if self.ball_x > self.screen.get_width() - ball_radius:
            self.ball_x = self.screen.get_width() - ball_radius
            self.ball_speed_x = -self.ball_speed_x

        # le pagaye
        if ball_rect.colliderect(paddle_rect):
            self.ball_speed_y = -self.ball_speed_y
            self.current_reward = STATES['Hit']
            self.ball_hit_count += 1
            self.paddle_hit_count += 1

            if len(self.bricks) == 0:
                self.initBricks()
        # les bricks
        for brick in self.bricks:
            if brick.rect.colliderect(ball_rect):
                self.score = self.score + 1
                self.bricks.remove(brick)
                self.ball_speed_y = - self.ball_speed_y

        if self.ball_hit_count > 3:
            self.randomAngle()

    def input(self):
        self.isPressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.command = 1
                    self.isPressed = True

                elif event.key == pygame.K_RIGHT:
                    self.command = 2
                    self.isPressed = True
                elif event.key == pygame.K_a:
                    self.isAuto = not self.isAuto

        if not self.isPressed:
            self.command = 0

        return True

    def decision(self):
        self.prev = [(self.ball_x - self.paddle_x + 640) / resolution, self.ball_y / resolution]

        actions = self.Q[int((self.ball_x - self.paddle_x + 640) / resolution), int(self.ball_y / resolution), :]

        maxs = [i for i, x in enumerate(actions) if x == np.argmax(actions)]
        if len(maxs) > 1:
            if self.command in maxs:
                com_command = self.command
            else:
                com_command = random.choice(maxs)
        else:
            com_command = np.argmax(actions)

        if self.isAuto is True:
            self.command = com_command

        if self.command == 1:
            self.paddle_x -= self.paddle_speed
        elif self.command == 2:
            self.paddle_x += self.paddle_speed

    def observe(self):
        prev_Q = self.Q[int(self.prev[0]), int(self.prev[1]), int(self.command)]

        self.Q[int(self.prev[0]), int(self.prev[1]), int(self.command)] = (
                prev_Q + alpha * (self.current_reward + lmbd *
                                  max(self.Q[int((self.ball_x - self.paddle_x + 640) / resolution),
                                      int(self.ball_y / resolution), :])
                                  - prev_Q))

    def draw(self):
        self.screen.fill(grey_bc)

        score_label = self.myfont.render(str(self.score), 100, pygame.color.THECOLORS['red'])
        self.screen.blit(score_label, (5, 10))

        count_label = self.myfont.render(str(self.paddle_hit_count), 100, pygame.color.THECOLORS['blue'])
        self.screen.blit(count_label, (70, 10))

        if self.isAuto is True:
            auto_label = self.myfont.render("", 100, pygame.color.THECOLORS['blue'])
            self.screen.blit(auto_label, (570, 10))
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brown_color, brick.rect, 0)
        pygame.draw.circle(self.screen, brown_color, [int(self.ball_x), int(self.ball_y)], ball_radius, 0)
        pygame.draw.rect(self.screen, brown_color, [self.paddle_x, self.paddle_y, paddle_width, paddle_height], 0)

        pygame.display.update()

    def quit(self):
        pygame.quit()

    def saveData(self):
        data = [int(self.iteration), int(self.highscore), self.Q]
        return data


@atexit.register
def save():
    savedata = game.saveData()
    np.savez(fname, iter=savedata[0], high=savedata[1], trainedQ=savedata[2])
    print("Donnes enregistres.")


if len(sys.argv) > 1:
    fName = str(sys.argv[1]).replace('.npz', '')

    try:
        data = np.load(str(fName) + '.npz')
        game = Envirement(data)
    except IOError:
        game = Envirement(None)

    while game.input():
        game.decision()
        game.update()
        game.observe()
        game.draw()

    game.quit()
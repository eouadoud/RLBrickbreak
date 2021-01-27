import atexit
import random
import sys

import numpy as np

import pygame

black = [0, 0, 0]
white = [255, 255, 255]
grey = [180, 180, 180]

block_width = 60
block_height = 12

fname = 'dataset_breakout'

resolution = 10
alpha = 0.5
l = 0.9  # lambda

STATES = {
    'Alive': 0,
    'Dead': -100,
    'Scores': 10,
    'Hit': 1
}

# the game's constant variables
ball_radius = 10
paddle_width = 200
paddle_height = 10


class Brick:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, block_width, block_height)


class Environment:

    def __init__(self, myData):
        self.highscore = 0
        self.isAuto = True
        self.command = 0
        self.iteration = 0
        self.Q = np.zeros((int(1299 / resolution), int(490 / resolution), 3))

        if myData is not None:
            try:
                self.iteration = int(myData['iter'])
                self.highScore = int(myData['high'])
                self.Q = myData['trainedQ']
            except:
                print("Can't load data from input file, wrong format.")
                raise

        pygame.init()

        # allows for holding of key
        pygame.key.set_repeat(1, 0)

        self.resetGame()

        self.screen = pygame.display.set_mode([800, 490])
        self.myfont = pygame.font.SysFont("Arial", 30)

    def initBricks(self):
        self.bricks = []
        for i in range(1, 9):
            for j in range(1, 5):
                temp = Brick(90 * i - 35, 50 + 20 * j)
                self.bricks.append(temp)

    def resetGame(self):
        # pygame.time.wait(2000)
        self.ball_x = 300
        self.ball_y = 450 - ball_radius
        self.ball_speed_x = 3
        self.ball_speed_y = 5

        self.randomAngle()
        self.paddle_x = 300
        self.paddle_y = 470
        self.paddle_speed = 10
        # self.paddle_vec = 0
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
        # Move ball
        self.ball_y += self.ball_speed_y
        self.ball_x += self.ball_speed_x
        self.hitDetect()

    def randomAngle(self):
        self.ball_y = 450 - ball_radius
        ran = random.randint(-1, 0)
        self.ball_speed_x = (7 - ran) * self.ball_speed_x / abs(self.ball_speed_x)
        self.ball_speed_y = (3 + ran) * self.ball_speed_y / abs(self.ball_speed_y)
        self.ball_hit_count = 0

    def hitDetect(self):
        # COLLISION DETECTION
        # circles are measured from the center, so have to subtract 1 radius from the x and y
        ball_rect = pygame.Rect(self.ball_x - ball_radius, self.ball_y - ball_radius, ball_radius * 2,
                                ball_radius * 2)
        paddle_rect = pygame.Rect(self.paddle_x, self.paddle_y, paddle_width, paddle_height)

        # check if ball is off the bottom of the self.screen
        if self.ball_y > self.screen.get_height() - ball_radius:

            self.current_reward = STATES['Dead']
            self.iteration += 1
            screen = 'Iteration: ' + repr(self.iteration) + ', max score: ' + repr(self.score) + ', hit count: ' + repr(
                self.paddle_hit_count)

            if self.score > self.highScore:
                self.highScore = self.score
                screen += ' NEW HIGHSCORE!'

            print(screen)
            self.resetGame()

        # for screen border
        if self.ball_y < ball_radius:
            self.ball_y = ball_radius
            self.ball_speed_y = -self.ball_speed_y

        if self.ball_x < ball_radius:
            self.ball_x = ball_radius
            self.ball_speed_x = -self.ball_speed_x

        if self.ball_x > self.screen.get_width() - ball_radius:
            self.ball_x = self.screen.get_width() - ball_radius
            self.ball_speed_x = -self.ball_speed_x

        # for paddle
        if ball_rect.colliderect(paddle_rect):
            self.ball_speed_y = -self.ball_speed_y
            self.current_reward = STATES['Hit']
            self.ball_hit_count += 1
            self.paddle_hit_count += 1
            # if pygame.display.get_active():

            if len(self.bricks) == 0:
                self.initBricks()
        # for bricks
        for brick in self.bricks:
            if brick.rect.colliderect(ball_rect):
                self.score = self.score + 1
                self.bricks.remove(brick)
                self.ball_speed_y = - self.ball_speed_y
                # self.current_reward = STATES['Scores']

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
                    # self.paddle_vec -= self.paddle_speed

                elif event.key == pygame.K_RIGHT:
                    self.command = 2
                    self.isPressed = True
                    # self.paddle_vec += self.paddle_speed
                elif event.key == pygame.K_a:
                    self.isAuto = not self.isAuto

        if not self.isPressed:
            self.command = 0

        return True

    def draw(self):
        self.screen.fill(white)

        score_label = self.myfont.render(str(self.score), 100, pygame.color.THECOLORS['black'])
        self.screen.blit(score_label, (5, 10))

        count_label = self.myfont.render(str(self.paddle_hit_count), 100, pygame.color.THECOLORS['grey'])
        self.screen.blit(count_label, (70, 10))

        if self.isAuto is True:
            auto_label = self.myfont.render("Mode = Auto", 100, pygame.color.THECOLORS['blue'])
            self.screen.blit(auto_label, (570, 10))
        for brick in self.bricks:
            pygame.draw.rect(self.screen, grey, brick.rect, 0)
        pygame.draw.circle(self.screen, grey, [int(self.ball_x), int(self.ball_y)], ball_radius, 0)
        pygame.draw.rect(self.screen, grey, [self.paddle_x, self.paddle_y, paddle_width, paddle_height], 0)

        pygame.display.update()

    def quit(self):
        pygame.quit()

    def saveData(self):
        data = [int(self.iteration), int(self.highScore), self.Q]
        return data


@atexit.register
def save():
    savedata = game_run.saveData()
    np.savez(fname, iter=savedata[0], high=savedata[1], trainedQ=savedata[2])
    print("Data saved successfully.")


class Agent:

    def __init__(self):
        self.bricks = []
        self.ball_speed_y = 5
        self.ball_speed_x = 3
        self.ball_y = 450 - ball_radius
        self.ball_x = 300
        self.paddle_x = 470
        self.paddle_y = 470
        self.paddle_speed = 10
        self.com_vec = 0
        self.current_reward = STATES['Alive']
        self.score = 0
        self.ball_hit_count = 0
        self.paddle_hit_count = 0
        self.highScore = 0
        self.isAuto = True
        self.command = 0
        self.iteration = 0
        self.Q = np.zeros((int(1299 / resolution), int(490 / resolution), 3))
        self.prev = [int((self.ball_x - self.paddle_x + 640) / resolution), int(self.ball_y / resolution)]

    def decision(self):

        # Observe what state is in and perform the action that maximizes expected reward.
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

        print(f"actions: {actions}")
        print(f"maxs: {maxs}")

    def observe(self):
        prev_Q = self.Q[self.prev[0], self.prev[1], self.command]

        self.Q[self.prev[0], self.prev[1], self.command] = (
                prev_Q + alpha * (self.current_reward + l *
                                  max(self.Q[int(self.ball_x - self.paddle_x + 640 / resolution),
                                      int(self.ball_y / resolution), :]) - prev_Q))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fname = str(sys.argv[1]).replace('.npz', '')

        try:
            data = np.load(str(fname) + '.npz')
            game_run = Environment(data)
            s = "Q loaded from " + str(fname) + " successfully."
            print(s)

        except IOError:
            s = "Error: can't find file or read data from " + str(fname) + ".npz, initializing a new Q matrix"
            print(s)
            game_run = Environment(None)

        agent = Agent()
        # game loop
        while game_run.input():
            agent.decision()
            game_run.update()
            agent.observe()
            game_run.draw()

        game_run.quit()
    else:
        print('INPUT ERROR: no file name provided. Read README.md for help.')
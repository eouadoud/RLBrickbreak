from random import seed

import pygame
import argparse

from environment import Environment
from game_run import game_init
from qlearning.agent_dnq import Agent_DQN
from startscreen import start_screen

pygame.init()
screen_width = 1500
screen_height = 700
screen_start = pygame.display.set_mode((screen_width, screen_height))


# ## input arguments
# parser = argparse.ArgumentParser()
# parser.add_argument('--epsilon', dest='epsilon', default=0.05, required=False, type=float, help='exploration rate for epsilon-greedy')
# parser.add_argument('--gamma', default=0.99, required=False, type=float, help='discount factor')
# parser.add_argument('--alpha', default=0.02, required=False, type=float, help='learning rate')
# parser.add_argument('--numtrain', default=10000, required=False, type=int, help='number of training episodes')
#
# parser.add_argument('--lambd', default=0.9, required=False, type=float, help='decay rate of eligibility traces')
# parser.add_argument('--version', default=1, required=False, type=int, help='1 for QLearner; 2 for QLearnerPlus; 3 for QLearnerPlusLambda')
#
# args = parser.parse_args()

# epsilon = args.epsilon
# gamma = args.gamma
# alpha = args.alpha
# numTraining = args.numtrain
# lambd = args.lambd
# version = args.version

def parse():
	parser = argparse.ArgumentParser(description="runner")
	parser.add_argument('--env_name', default=None, help='environment name')
	parser.add_argument('--train_pg', action='store_true', help='whether train policy gradient')
	parser.add_argument('--train_dqn', action='store_true', help='whether train DQN')
	parser.add_argument('--test_pg', action='store_true', help='whether test policy gradient')
	parser.add_argument('--test_dqn', action='store_true', help='whether test DQN')
	parser.add_argument('--video_dir', default=None, help='output video directory')
	parser.add_argument('--do_render', action='store_true', help='whether render environment')
	args = parser.parse_args()
	return args


def run(args):
	if args.train_dqn:
		env_name = args.env_name or 'BreakoutNoFrameskip-v4'
		env = Environment(env_name, args, True)
		agent = Agent_DQN(env, args)
		agent.train()

	if args.test_dqn:
		env = Environment('BreakoutNoFrameskip-v4', args, True, test=True)
		agent = Agent_DQN(env, args)
		test(agent, env, total_episodes=100)


def test(agent, env, total_episodes=30):
	rewards = []
	env.seed(seed)
	for i in range(total_episodes):
		state = env.reset()
		done = False
		episode_reward = 0.0

		# playing one game
		while not done:
			action = agent.make_action(state, test=True)
			state, reward, done, info = env.step(action)
			episode_reward += reward

		rewards.append(episode_reward)
	print('Run %d episodes'%(total_episodes))
	# print('Mean:', np.mean(rewards))

# def main():
#     start_screen()
#     run = True
#     black = (0, 0, 0)
#     screen_start.fill(black)
#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#         game_init()

def main():
    start_screen()
    args = parse()
    run(args)
    black = (0, 0, 0)
    screen_start.fill(black)

    # while run:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #     game_init()


main()

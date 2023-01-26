import time
import matplotlib.pyplot as plt
import numpy

from agent import Agent
from environment import Environment

env = Environment(20, 7)
agent = Agent(200, 20, alpha=.01, gamma=.95, epsilon=1, epsilon_lower=.3, epsilon_decay=.99)
observation = env.snapshot()
game_over = False
episode_reward = 0
episode_steps = 0
episode_rewards = []
episode_steps_list = []
episode_shortest_paths = []


def process_frame(frame):
    """
    maps the values in `[0, 10]` to values in `[0, 1]`
    """
    return [[val / 10 for val in row] for row in frame]


def take_action(action):
    """
    passed to `agent.step`\\
    uses `environment.step`\\
    updates stats for the current episode
    """
    global env, agent, observation, game_over, episode_reward, episode_steps

    observation, reward, game_over = env.step(action)
    episode_reward += reward
    episode_steps += 1

    return observation, reward, game_over


def main():
    global env, agent, observation, game_over, episode_reward, episode_steps, episode_rewards, \
        episode_steps_list, episode_shortest_paths

    number_of_episodes = 500
    max_steps = 80
    successful_episodes = 0

    for episode in range(number_of_episodes):
        env.reset(True)
        # GOOD TO HAVE: reset only for agent position

        episode_shortest_paths.append(env.shortest_path())

        while not game_over and episode_steps < max_steps:
            state = process_frame(observation)
            agent.step(state, take_action)
            if episode < number_of_episodes * .8 and episode_steps % 5 == 0:
                agent.train()
            if env.shortest_path() < 16:
                env.render(f'Stage: Training - Episode: {episode + 1}/{number_of_episodes} - Reward: {episode_reward} '
                           f'- Steps: {episode_steps} - Shortest path: {episode_shortest_paths[-1]} '
                           f'\nAgent position: {env.agent_position}'
                           f'\nHyper-parameters: Alpha={agent.alpha:.3f}, Gamma={agent.gamma:.3f}, '
                           f'Epsilon={agent.epsilon:.3f} ')
                # time.sleep(.1)

        # agent.replay()
        if (episode + 1) % 10 == 0:
            # agent.update_target()
            agent.save()

        # if (episode + 1) % 500 == 0:
        #     print(f'Number of successful episodes: {successful_episodes} / 500 ({successful_episodes / 500 * 100:.2f}%)')

        if game_over:
            successful_episodes += 1
            print(f'Stage: Training - Episode: {episode + 1}/{number_of_episodes} - Reward: {episode_reward} '
                  f'- Steps: {episode_steps} - Shortest path: {episode_shortest_paths[-1]}'
                  f'\nHyper-parameters: Alpha={agent.alpha:.3f}, Gamma={agent.gamma:.3f}, Epsilon={agent.epsilon:.3f} ')
        else:
            print(f'Stage: Training - Episode: {episode + 1}/{number_of_episodes} - Reward: {episode_reward} FAILED ')

        episode_rewards.append(episode_reward)
        episode_steps_list.append(episode_steps)
        episode_reward = 0
        episode_steps = 0
        game_over = False

    print(f'Number of successful episodes: {successful_episodes} / {number_of_episodes} ({successful_episodes / number_of_episodes * 100:.2f}%)')

    # plot the rewards
    plt.figure(figsize=(10, 10))
    plt.plot([episode + 1 for episode in range(number_of_episodes)],
             [numpy.mean([episode_rewards[i]
                          for i in range(min(ep, number_of_episodes - 30), min(ep + 30, number_of_episodes))])
              for ep in range(number_of_episodes)])
    plt.gca().xaxis.set_ticks_position('top')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.savefig('rewards.png')

    # plot the steps
    plt.figure(figsize=(10, 10))
    plt.plot([episode + 1 for episode in range(number_of_episodes)],
             [numpy.mean([episode_shortest_paths[i]
                          for i in range(min(ep, number_of_episodes - 30), min(ep + 30, number_of_episodes))]) /
              numpy.mean([episode_steps_list[i]
                          for i in range(min(ep, number_of_episodes - 30), min(ep + 30, number_of_episodes))])
              for ep in range(number_of_episodes)])
    plt.xlabel('Episode')
    plt.ylabel('Shortest path / Total steps')
    plt.savefig('steps.png')

    # test the model on a new environment
    # input('Press enter to test the model on a new environment')
    # plt.close('all')
    # # plt.figure(figsize=(10, 10))
    # while not game_over:
    #     env.reset(True)
    #     shortest_path = env.shortest_path()
    #     episode_reward = 0
    #     episode_steps = 0
    #     while not game_over and episode_steps < 100:
    #         state = process_frame(env.snapshot())
    #         agent.step(state, take_action)
    #         env.render(
    #             f'Stage: Testing - Reward: {episode_reward} - Steps: {episode_steps} - Shortest path: {shortest_path}'
    #             f'\nAgent position: {env.agent_position}'
    #             f'\nHyper-parameters: Alpha={agent.alpha:.3f}, Gamma={agent.gamma:.3f}, Epsilon={agent.epsilon:.3f} ')
    #         # time.sleep(.1)
    #         episode_steps += 1


if __name__ == '__main__':
    main()

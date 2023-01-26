import numpy as np
import matplotlib.pyplot as plt

from agent import Agent
from environment import Environment

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
    global env, observation, episode_reward, episode_steps, game_over
    observation, reward, game_over = env.step(action)
    episode_reward += reward
    episode_steps += 1
    return observation, reward, game_over

def plot_stats(number_of_episodes, rewards, steps_list, shortest_paths):
    plt.figure(figsize=(10, 10))
    plt.plot(
        range(1, number_of_episodes + 1),
        [np.mean([rewards[i] for i in range(
            min(episode, number_of_episodes - 5),
            min(episode + 5, number_of_episodes)
        )]) for episode in range(1, number_of_episodes + 1)]
    )
    plt.gca().xaxis.set_ticks_position('top')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.savefig('rewards.png')

    plt.figure(figsize=(10, 10))
    plt.plot(
        range(1, number_of_episodes + 1),
        [np.mean([shortest_paths[i] for i in range(
            min(episode, number_of_episodes - 5),
            min(episode + 5, number_of_episodes)
        )]) / np.mean([steps_list[i] for i in range(
            min(episode, number_of_episodes - 5),
            min(episode + 5, number_of_episodes)
        )]) for episode in range(1, number_of_episodes + 1)]
    )
    plt.xlabel('Episode')
    plt.ylabel('Shortest path / Total steps')
    plt.savefig('steps.png')

if __name__ == '__main__':
    env = Environment(20, 7)
    agent = Agent(1000, 100, alpha=.1, gamma=.618, epsilon=1, epsilon_lower=.1, epsilon_decay=.9)

    episode_rewards = []
    episode_steps_list = []
    episode_shortest_paths = []

    number_of_episodes = 500
    max_steps = 100

    for episode in range(1, number_of_episodes + 1):
        game_over = False
        episode_steps = 0
        episode_reward = 0

        env.reset(True)
        episode_shortest_paths.append(env.shortest_path_length())

        choice = 'n'
        if episode % 50 == 0:
            choice = input('>>> Do you want to view the training process on the next episode? [Y/N] ').lower()
            if choice != 'y': choice = 'n'

        observation = env.snapshot()
        while not game_over and episode_steps < max_steps:
            state = process_frame(observation)
            agent.step(state, take_action)
            if choice == 'y':
                env.render(
                    f'Stage: Training - Episode: {episode}/{number_of_episodes} - Reward: {episode_reward} '
                    f'- Steps: {episode_steps} - Shortest path: {episode_shortest_paths[-1]}'
                    f'\nAgent position: {env.agent_position} - Epsilon: {agent.epsilon:.3f}'
                )
        episode_rewards.append(episode_reward)
        episode_steps_list.append(episode_steps)

        agent.replay()
        agent.save()
        
        print(
            f'Stage: Training - Episode: {episode}/{number_of_episodes} - Reward: {episode_reward} '
            f'- Steps: {episode_steps} - Shortest path: {episode_shortest_paths[-1]}'
            f'\nAgent position: {env.agent_position} - Epsilon: {agent.epsilon:.3f}'
        )

    plot_stats(number_of_episodes, episode_rewards, episode_steps_list, episode_shortest_paths)

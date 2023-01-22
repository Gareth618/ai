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
    ...

env = Environment(20, 7)
agent = Agent(100, 25, alpha=.01, gamma=.95, epsilon=1, epsilon_lower=.1, epsilon_decay=.99)
env.render()

from agent import Agent
from environment import Environment

# training

def process_frame(frame):
    # maps the values in [0, 9] to values in [0, 1]
    ...

def take_action(action):
    # passed to `agent.step`
    # uses `environment.step`
    # updates stats for the current episode
    ...

environment = Environment(...)
agent = Agent(...)
...

class Agent:
    def __init__(self, memory_size, batch_size, **hyper):
        self.alpha = hyper['alpha']
        self.gamma = hyper['gamma']
        self.epsilon = hyper['epsilon']
        self.epsilon_lower = hyper['epsilon_lower']
        self.epsilon_decay = hyper['epsilon_decay']
        self.memory = ...
        self.batch_size = batch_size
        self.model = ...

    def step(self, state, take_action):
        ...

    def replay(self):
        ...

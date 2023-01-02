class Environment:
    def __init__(self, image_size, window_size):
        self.image_size = image_size
        self.window_size = window_size
        self.reset(False)

    def reset(self, use_gradient):
        self.image = self._random_gradient_image() if use_gradient else self._random_image()
        self.target_position = ...
        self.agent_position = ...
        self.agent_path = [self.agent_position]

    def _random_image(self):
        ...

    def _random_gradient_image(self):
        ...

    def _snapshot(self):
        # returns a matrix of the current observable image
        ...

    def render(self):
        # renders the entire image along with `self.agent_path` too
        # the pixels are mapped from [0, 9] to [0, 255]
        ...

    def step(self, action):
        # `action = (delta_x, delta_y)`
        # updates `self.agent_path`
        # returns `(observation = _snapshot(), reward, finished)`
        ...

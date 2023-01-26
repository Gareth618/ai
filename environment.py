import math
import random
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from PIL import Image

class Environment:
    def __init__(self, image_size, window_size):
        self.image = None
        self.agent_path = None
        self.agent_position = None
        self.initial_agent_position = None
        self.target_position = None
        self.image_size = image_size
        self.window_size = window_size
        self.figure = None
        plt.ion()

    def reset(self, use_gradient):
        self.target_position = (random.randrange(self.image_size), random.randrange(self.image_size))

        self.image = self._random_gradient_image() if use_gradient else self._random_image()
        self.image[self.target_position[0]][self.target_position[1]] = 9

        while True:
            self.agent_position = (random.randrange(self.image_size), random.randrange(self.image_size))
            if self.target_position != self.agent_position: break
        
        self.initial_agent_position = self.agent_position
        self.agent_path = [self.agent_position]

    def _random_image(self):
        return [[random.randrange(9) for _ in range(self.image_size)] for _ in range(self.image_size)]

    def _random_gradient_image(self):
        factors = [1.10963, 1.2712, 1.36552, 1.43312, 1.48623, 1.53015, 1.56771, 1.60059, 1.62987, 1.65631]
        factor = factors[min(self.image_size // 10 - 1, 9)]
        temp = [1]
        for i in range(1, 9):
            temp.append(temp[i - 1] * factor)
        borders = [1]
        for i in range(1, 9):
            borders.append(borders[i - 1] + temp[i - 1])
        borders = borders[1:]
        borders.append(self.image_size * 2)

        image = []
        for i in range(self.image_size):
            t = []
            for j in range(self.image_size):
                d = math.sqrt((self.target_position[0] - i) ** 2 + (self.target_position[1] - j) ** 2)
                k = 0
                while d > borders[k]:
                    k = k + 1
                color = 8 - k
                t.append(color)
            image.append(t)

        for i in range(self.image_size):
            for j in range(self.image_size):
                x = random.choices([0, -1, 1], weights=[13, 2, 1], k=1)
                image[i][j] = max(0, min(8, image[i][j] + x[0]))
        return image

    def snapshot(self):
        """
        returns a matrix of the current observable image
        """

        border_value = 10
        window = []
        for i in range(self.window_size):
            window.append([border_value] * self.window_size)

        pos_x = self.agent_position[0] - self.window_size // 2
        pos_y = self.agent_position[1] - self.window_size // 2
        for i in range(self.window_size):
            for j in range(self.window_size):
                new_x = pos_x + i
                new_y = pos_y + j
                if 0 <= new_x < self.image_size and 0 <= new_y < self.image_size:
                    window[i][j] = self.image[new_x][new_y]
        return window

    def render(self, title=None):
        """
        renders the entire image along with `self.agent_path` too\\
        the pixels are mapped from `[0, 9]` to `[0, 255]`
        """

        zoom_factor = 6
        path_color = (0, 53, 153)

        norm = mpl.colors.Normalize(vmin=0, vmax=9)
        cmap = cm.CMRmap
        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        image_size = self.image_size * zoom_factor
        img = Image.new(mode='RGBA', size=(image_size, image_size))
        pixels = img.load()
        for i in range(self.image_size):
            for j in range(self.image_size):
                color = m.to_rgba(self.image[i][j], bytes=True)
                for k in range(zoom_factor):
                    for u in range(zoom_factor):
                        pixels[j * zoom_factor + u, i * zoom_factor + k] = color

        for i in range(1, len(self.agent_path)):
            path_color = (0, 53 + i * 200 // len(self.agent_path), 153)
            first = self.agent_path[i - 1]
            second = self.agent_path[i]
            if first[0] == second[0]:
                left = first[1] if first[1] < second[1] else second[1]
                for j in range(zoom_factor + 2):
                    x = first[0] * zoom_factor + zoom_factor / 2
                    y = left * zoom_factor + zoom_factor / 2 + j - 1
                    pixels[y, x] = path_color
                    pixels[y, x - 1] = path_color
            else:
                up = first[0] if first[0] < second[0] else second[0]
                for j in range(zoom_factor + 2):
                    x = up * zoom_factor + zoom_factor / 2 + j - 1
                    y = first[1] * zoom_factor + zoom_factor / 2
                    pixels[y, x] = path_color
                    pixels[y - 1, x] = path_color

        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.agent_position[1] * zoom_factor + zoom_factor // 2 + i
                y = self.agent_position[0] * zoom_factor + zoom_factor // 2 + j
                pixels[x, y] = (255, 255, 255)

        if self.figure is None:
            self.figure, ax = plt.subplots()
            ax.xaxis.set_ticks_position('top')
        plt.imshow(img)
        plt.title(title)
        self.figure.canvas.flush_events()

    def step(self, action):
        """
        `action = (delta_x, delta_y)`\\
        updates `self.agent_path`\\
        returns `(observation = snapshot(), reward, finished)`
        """

        new_position = (self.agent_position[0] + action[0], self.agent_position[1] + action[1])
        if not 0 <= new_position[0] < self.image_size or not 0 <= new_position[1] < self.image_size:
            return self.snapshot(), -100, False
        
        prev_value = self.image[self.agent_position[0]][self.agent_position[1]]
        next_value = self.image[new_position[0]][new_position[1]]
        step_reward = 2 * (next_value - prev_value) - 1
        self.agent_position = new_position
        self.agent_path.append(new_position)
        if new_position == self.target_position:
            return self.snapshot(), 200, True        
        return self.snapshot(), step_reward, False

    def shortest_path_length(self):
        """
        returns the length of the shortest path from `self.agent_position` to `self.target_position`
        """
        return abs(self.agent_position[0] - self.target_position[0]) + abs(self.agent_position[1] - self.target_position[1])

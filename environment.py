import math
import random

from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as mplpp
import matplotlib.cm as cm


class Environment:
    zoom_factor = 6
    path_color = (0, 153, 153)
    figure = None

    def __init__(self, image_size, window_size):
        self.agent_path = None
        self.agent_position = None
        self.image = None
        self.target_position = None
        self.image_size = image_size
        self.window_size = window_size
        self.reset(True)
        mplpp.ion()

<<<<<<< Updated upstream
    def reset(self, use_gradient):
        self.target_position = (random.randint(0, self.image_size - 1), random.randint(0, self.image_size - 1))
=======
    def reset(self, use_gradient, min_path_length):
        if self.target_position is None:
            self.target_position = (random.randrange(self.image_size), random.randrange(self.image_size))
>>>>>>> Stashed changes

        if self.image is None:
            self.image = self._random_gradient_image() if use_gradient else self._random_image()
            self.image[self.target_position[0]][self.target_position[1]] = 9

<<<<<<< Updated upstream
        self.agent_position = (random.randint(0, self.image_size - 1), random.randint(0, self.image_size - 1))
        while self.target_position == self.agent_position:
            self.agent_position = (random.randint(0, self.image_size - 1), random.randint(0, self.image_size - 1))
=======
        while True:
            self.agent_position = (random.randrange(self.image_size), random.randrange(self.image_size))
            if self.target_position != self.agent_position: break
            # length = abs(self.target_position[0] - self.agent_position[0]) + abs(self.target_position[1] - self.agent_position[1])
            # if length <= min_path_length: break

        self.initial_agent_position = self.agent_position
>>>>>>> Stashed changes
        self.agent_path = [self.agent_position]

    def _random_image(self):
        image = []
        for i in range(0, self.image_size):
            t = []
            for j in range(0, self.image_size):
                t.append(random.randint(0, 8))
            image.append(list(t))
        return image

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
        for i in range(0, self.image_size):
            t = []
            for j in range(0, self.image_size):
                d = math.sqrt((self.target_position[0] - i) ** 2 + (self.target_position[1] - j) ** 2)
                k = 0
                while d > borders[k]:
                    k = k + 1
                color = 8 - k
                t.append(color)
            image.append(t)
        for i in range(0, self.image_size):
            for j in range(0, self.image_size):
                x = random.choices([0, -1, 1], weights=[13, 2, 1], k=1)
                image[i][j] = max(0, min(8, image[i][j] + x[0]))
        return image

    def snapshot(self):
        """
        returns a matrix of the current observable image
        """

        border_value = 10
        window = []
        for i in range(0, self.window_size):
            window.append([border_value] * self.window_size)

        poz_x = self.agent_position[0] - self.window_size // 2
        poz_y = self.agent_position[1] - self.window_size // 2
        for i in range(0, self.window_size):
            for j in range(0, self.window_size):
                new_x = poz_x + i
                new_y = poz_y + j
                if 0 <= new_x < self.image_size and 0 <= new_y < self.image_size:
                    window[i][j] = self.image[new_x][new_y]
        return window

    def render(self, title=None):
        """ 
        renders the entire image along with `self.agent_path` too\\
        the pixels are mapped from `[0, 9]` to `[0, 255]`
        """

        self.path_color = (0, 53, 153)
        norm = mpl.colors.Normalize(vmin=0, vmax=9)
        # https://matplotlib.org/stable/tutorials/colors/colormaps.html
        # cmap = cm.nipy_spectral
        # cmap = cm.hot
        cmap = cm.CMRmap
        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        image_size = self.image_size * self.zoom_factor
        img = Image.new(mode="RGBA", size=(image_size, image_size))
        pixels = img.load()
        for i in range(0, self.image_size):
            for j in range(0, self.image_size):
                color = m.to_rgba(self.image[i][j], bytes=True)
                for k in range(0, self.zoom_factor):
                    for u in range(0, self.zoom_factor):
                        pixels[j * self.zoom_factor + u, i * self.zoom_factor + k] = color

        # self.agent_path = [(0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4)]
        for i in range(1, len(self.agent_path)):
            self.path_color = (0, 53 + i * 200 // len(self.agent_path), 153)
            first = self.agent_path[i - 1]
            second = self.agent_path[i]

            if first[0] == second[0]:
                if first[1] < second[1]:
                    st = first[1]
                else:
                    st = second[1]

                for j in range(0, self.zoom_factor + 2):
                    x = first[0] * self.zoom_factor + self.zoom_factor / 2
                    y = st * self.zoom_factor + self.zoom_factor / 2 + j - 1
                    pixels[y, x] = self.path_color
                    pixels[y, x - 1] = self.path_color
            else:
                if first[0] < second[0]:
                    up = first[0]
                else:
                    up = second[0]
                for j in range(0, self.zoom_factor + 2):
                    x = up * self.zoom_factor + self.zoom_factor / 2 + j - 1
                    y = first[1] * self.zoom_factor + self.zoom_factor / 2
                    pixels[y, x] = self.path_color
                    pixels[y - 1, x] = self.path_color

        # make agent position with white color
        for i in range(-1, 2):
            for j in range(-1, 2):
                pixels[self.agent_position[1] * self.zoom_factor + self.zoom_factor // 2 + i,
                       self.agent_position[0] * self.zoom_factor + self.zoom_factor // 2 + j] = (255, 255, 255)

        if self.figure is None:
            self.figure, ax = mplpp.subplots()
            ax.xaxis.set_ticks_position('top')

        mplpp.imshow(img)
        mplpp.title(title)
        self.figure.canvas.flush_events()
        # mplpp.show()

    def step(self, action):
        """
        `action = (delta_x, delta_y)`\\
        updates `self.agent_path`\\
        returns `(observation = _snapshot(), reward, finished)`
        """

        new_position = (self.agent_position[0] + action[0], self.agent_position[1] + action[1])
<<<<<<< Updated upstream

        # if not 0 <= new_position[0] < self.image_size or not 0 <= new_position[1] < self.image_size:
        #     return self.snapshot(), -100, False

=======
        if not 0 <= new_position[0] < self.image_size or not 0 <= new_position[1] < self.image_size:
            # self.agent_position = self.initial_agent_position
            # self.agent_path = [self.agent_position]
            return self.snapshot(), -10, True

        # prev_value = self.image[self.agent_position[0]][self.agent_position[1]]
        self.agent_position = new_position
>>>>>>> Stashed changes
        self.agent_path.append(new_position)
        self.agent_position = new_position
        if new_position == self.target_position:
<<<<<<< Updated upstream
            return self.snapshot(), 100, True
        elif new_position in self.agent_path[:-1]:
            return self.snapshot(), -100, False
        else:
            return self.snapshot(), -1, False

=======
            return self.snapshot(), 10, True
        # next_value = self.image[new_position[0]][new_position[1]]
        # step_reward = min(math.exp(next_value - prev_value), 100) if next_value > prev_value else max(math.exp(prev_value - next_value), -100)
        return self.snapshot(), -1, False
>>>>>>> Stashed changes

    def test(self):
        print(self.snapshot())

    def shortest_path(self):
        """
        returns the length of the shortest path from `self.agent_position` to `self.target_position`
        """
        length = abs(self.agent_position[0] - self.target_position[0]) + abs(self.agent_position[1] - self.target_position[1])
        return length

    def is_valid_action(self, action):
        """
        returns `True` if `action` is valid
        """
        new_position = (self.agent_position[0] + action[0], self.agent_position[1] + action[1])
        return 0 <= new_position[0] < self.image_size and 0 <= new_position[1] < self.image_size

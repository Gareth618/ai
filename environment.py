import random
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as mplpp
import matplotlib.cm as cm


class Environment:
    zoom_factor = 6

    def __init__(self, image_size, window_size):
        self.image_size = image_size
        self.window_size = window_size
        self.reset(False)

    def reset(self, use_gradient):
        self.image = self._random_gradient_image() if use_gradient else self._random_image()

        self.target_position = (random.randint(0, self.image_size - 1), random.randint(0, self.image_size - 1))
        self.image[self.target_position[0]][self.target_position[1]] = 9

        self.agent_position = (random.randint(0, self.image_size - 1), random.randint(0, self.image_size - 1))
        while self.target_position == self.agent_position:
            self.agent_position = (random.randint(0, self.image_size - 1), random.randint(0, self.image_size - 1))
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
        ...
        # target -> 9
        # 75549
        # 76544
        # 76555

    def _snapshot(self):
        # returns a matrix of the current observable image
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

    def render(self):
        # renders the entire image along with `self.agent_path` to
        # the pixels are mapped from [0, 9] to [0, 255]
        norm = mpl.colors.Normalize(vmin=0, vmax=9)
        # https://matplotlib.org/stable/tutorials/colors/colormaps.html
        # cmap = cm.nipy_spectral
        cmap = cm.hot
        # cmap = cm.CMRmap
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

        #self.agent_path = [(0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4)]
        for i in range(1, len(self.agent_path)):
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
                    pixels[y, x] = (0, 0, 255)
                    pixels[y, x - 1] = (0, 0, 255)
            else:
                if first[0] < second[0]:
                    up = first[0]
                else:
                    up = second[0]
                for j in range(0, self.zoom_factor + 2):
                    x = up * self.zoom_factor + self.zoom_factor / 2 + j - 1
                    y = first[1] * self.zoom_factor + self.zoom_factor / 2
                    pixels[y, x] = (0, 0, 255)
                    pixels[y - 1, x] = (0, 0, 255)
        mplpp.imshow(img)
        mplpp.show()

    def step(self, action):
        # `action = (delta_x, delta_y)`
        # updates `self.agent_path`
        # returns `(observation = _snapshot(), reward, finished)`
        ...

    def test(self):
        print(self._snapshot())


obj = Environment(10, 3)
obj.render()
# obj.test()

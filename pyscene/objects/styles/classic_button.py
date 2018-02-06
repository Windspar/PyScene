import pygame
import numpy as np
from ... import twist
from ..objects import PySceneImage
from .base import create_surface, ButtonStyle
from .style_color import color_tones

class ClassicButtonStyle(ButtonStyle):
    def __init__(self, color, disabled_color, reverse=False, intensity=12, border=3):
        self.border = border
        self.reverse = reverse
        self.intensity = intensity
        self.color = twist.color(color)
        self.disabled_color = twist.color(disabled_color)

    def get_image(self, rect):
        self.rect = rect
        return self.build_simple()

    def build_simple(self):
        bright, normal, dark = map(twist.color, color_tones(self.color, self.intensity))

        return PySceneImage(
            self.create_simple(normal),
            self.create_simple(bright),
            self.create_simple(normal, True),
            self.create_simple(self.disabled_color),
        )

    def create_simple(self, color, reverse=False):
        bright, normal, dark = map(twist.color, color_tones(color, self.intensity))
        bright_decimal = np.sum(np.array(bright) << np.array((16, 8, 0, 24)))
        dark_decimal = np.sum(np.array(dark) << np.array((16, 8, 0, 24)))
        image = create_surface(normal, self.rect.size)
        array = pygame.surfarray.pixels2d(image)
        w, h = array.shape

        for y in range(self.border):
            for x in range(y, w - y):
                if reverse:
                    array[x][y] = dark_decimal
                    array[x][h - y - 1] = bright_decimal
                else:
                    array[x][y] = bright_decimal
                    array[x][h - y - 1] = dark_decimal

        for x in range(self.border):
            for y in range(x, h - x):
                if reverse:
                    array[x][y] = dark_decimal
                    array[w - x - 1][y] = bright_decimal
                else:
                    array[x][y] = bright_decimal
                    array[w - x - 1][y] = dark_decimal

        return image

import numpy as np
import pygame

from .properties import ArrayProperty
from .functions import rgba_to_hsla, hsla_to_rgba

# under construction
def new_color(cls, class_type, *args):
    if len(args) == 1:
        if isinstance(args[0], str):
            red, green, blue, alpha = pygame.Color(args[0])
            if class_type == 'HSL':
                print('HSL')
                rgba = rgba_to_hsla(np.array((red, green, blue, alpha)))
                obj = np.asarray(rgba)
            else:
                obj = np.asarray((red, green, blue, alpha)).view(cls)
        elif isinstance(args[0], pygame.Color):
            if class_type == 'HSL':
                obj = np.asarray(args[0].hsla).view(cls)
            elif class_type == 'HSV':
                obj = np.asarray(args[0].hsva).view(cls)
            else:
                red, green, blue, alpha = args[0]
                obj = np.asarray((red, green, blue, alpha)).view(cls)
        elif isinstance(args[0], np.ndarray):
            if len(args[0]) == 3:
                obj = np.asarray((*args[0][0:3], 255)).view(cls)
            elif len(args[0]) == 4:
                obj = np.asarray(args[0][0:4]).view(cls)
        elif isinstance(args[0], (tuple, list)):
            if len(args[0]) == 3:
                obj = np.asarray((*args[0], 255)).view(cls)
            elif len(args[0]) == 4:
                obj = np.asarray(args[0]).view(cls)
        else:
            print('Wrong color format')
            obj = np.asarray((0, 0, 0, 0)).view(cls)
    elif len(args) == 3:
        obj = np.asarray((*args, 255)).view(cls)
    elif len(args) == 4:
        obj = np.asarray((*args)).view(cls)
    else:
        print('Wrong color format')
        obj = np.asarray((0, 0, 0, 0)).view(cls)

    return obj

class ColorRGB(np.ndarray):
    def __new__(cls, red, green=None, blue=None, alpha=255):
        if not green:
            return new_color(cls, 'RGB', red)
        else:
            return new_color(cls, 'RGB', red, green, blue, alpha)

    def pygame_color(self):
        data = self.astype(int)
        return pygame.Color(*data)

    def tup(self, cast=None):
        if cast:
            data = self.astype(cast)
            return tuple(data.tolist())

        return tuple(self.tolist())

    def to_decimal(self):
        data = self.astype(int)
        return np.sum(data << np.array((16, 8, 0, 24)))

    def from_decimal(self, value):
        self.b = value & 255
        self.g = (value & (255 << 8)) / 256
        self.r = (value & (255 << 16)) / (256 << 8)
        self.a = (value & (255 << 24)) / (256 << 16)

    r = ArrayProperty(0)
    g = ArrayProperty(1)
    b = ArrayProperty(2)
    a = ArrayProperty(3)

    red = ArrayProperty(0)
    green = ArrayProperty(1)
    blue = ArrayProperty(2)
    alpha = ArrayProperty(3)
    #hsla = RGBA_HSLA_Property()
    decimal = property(to_decimal, from_decimal)

class ColorHSL(np.ndarray):
    def __new__(cls, hue, sat=None, lum=None, alpha=255):
        if not s:
            return new_color(cls, 'HSL', hue)
        else:
            return new_color(cls, 'HSL', hue, sat, lum, alpha)

    def tup(self, cast=None):
        if cast:
            self.astype(cast)
        return tuple(self.tolist())

    h = ArrayProperty(0)
    s = ArrayProperty(1)
    l = ArrayProperty(2)
    a = ArrayProperty(3)

    hue = ArrayProperty(0)
    saturation = ArrayProperty(1)
    lightness = ArrayProperty(2)
    alpha = ArrayProperty(3)

class ColorHSV(np.ndarray):
    def __new__(cls, hue, sat=None, val=None, alpha=255):
        if s is None:
            if len(h) == 3:
                h = (*hue, alpha)
            obj = np.asarray(h).view(cls)
        else:
            obj = np.asarray((hue, sat, val, alpha)).view(cls)
        return obj

    def tup(self, cast=None):
        if cast:
            data = self.astype(cast)
            return tuple(data.tolist())
        return tuple(self.tolist())

    h = ArrayProperty(0)
    s = ArrayProperty(1)
    v = ArrayProperty(2)
    a = ArrayProperty(3)

    hue = ArrayProperty(0)
    saturation = ArrayProperty(1)
    value = ArrayProperty(2)
    alpha = ArrayProperty(3)

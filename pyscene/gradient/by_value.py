import numpy as np
import pygame
from .base import RGBA_FORMULA, pure_color

class HSL:
    H = 0
    HUE = 0
    S = 1
    SAT = 1
    SATURATION = 1
    L = 2
    LUM = 2
    LIGHT = 2
    LIGHTNESS = 2

class RGB:
    R = 0
    RED = 0
    G = 1
    GREEN = 1
    B = 2
    BLUE = 2

class HSV:
    H = 0
    HUE = 0
    S = 1
    SAT = 1
    SATURATION = 1
    V = 2
    VALUE = 2

def by_value(horizontal, value, color, value_begin, value_end, decimal, flip):
    length = value_end - value_begin

    if horizontal:
        surface = pygame.Surface((1, length))
    else:
        surface = pygame.Surface((length, 1))

    surface = surface.convert_alpha()
    surface_array = pygame.surfarray.pixels2d(surface)

    np_color = color
    for val in range(value_begin, value_end):
        pos = val - value_begin
        np_color[value] = val
        if horizontal:
            surface_array[0][pos] = decimal(np_color)
        else:
            surface_array[pos][0] = decimal(np_color)

    if flip:
        if horizontal:
            surface = pygame.transform.flip(surface, False, True)
        else:
            surface = pygame.transform.flip(surface, True, False)

    return surface

def hsl_by_value(horizontal, value, color, offset_begin, offset_end, flip=False):
    color = np.array(pure_color(color).hsla)
    base = int(color[value] + 0.5)

    if base - offset_begin < 0:
        offset_begin = base
    else:
        offset_begin = base - offset_begin

    if value == 0:
        if base + offset_end > 360:
            offset_end = 360 - base
        else:
            offset_end = base + offset_end
    else:
        if base + offset_end > 100:
            offset_end = 100 - base
        else:
            offset_end = base + offset_end

    def decimal(color):
        pcolor = pygame.Color(0,0,0)
        pcolor.hsla = color
        return np.sum(np.array(pcolor, int) << RGBA_FORMULA)

    return by_value(horizontal, value, color, offset_begin, offset_end, decimal, flip)

def hsv_by_value(horizontal, value, color, offset_begin, offset_end, flip=False):
    color = np.array(pure_color(color).hsva)
    base = color[value]

    if base - offset_begin < 0:
        offset_begin = base

    if value == 0:
        if base + offset_end > 360:
            offset_end = 360 - base
    else:
        if base + offset_end > 100:
            offset_end = 100 - base

    def decimal(color):
        pcolor = pygame.Color(0,0,0)
        pcolor.hsva = color
        return np.sum(np.array(pcolor, int) << RGBA_FORMULA)

    return by_value(horizontal, value, color, offset_begin, offset_end, decimal, flip)

def rgb_by_value(horizontal, value, color, value_begin, value_end, flip=False):
    color = np.array(pure_color(color))

    def decimal(color):
        return np.sum(color.astype(int) << RGBA_FORMULA)

    return by_value(horizontal, value, color, value_begin, value_end, decimal, flip)

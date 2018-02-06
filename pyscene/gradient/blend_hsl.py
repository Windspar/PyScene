import numpy as np
import pygame
from .base import RGBA_FORMULA, pure_colors

def blend_hsl(horizontal, colors, length=255, inverse=False):
    arrays = [np.array(c.hsla) for c in pure_colors(colors)]

    if horizontal:
        surface = pygame.Surface((1, length))
    else:
        surface = pygame.Surface((length, 1))
    surface = surface.convert_alpha()
    surface_array = pygame.surfarray.pixels2d(surface)

    offset = len(arrays) - 1
    depth = int(length / offset)
    gap = 0

    for i in range(offset):
        color = np.copy(arrays[i])
        color2 = np.copy(arrays[i + 1])

        for d in range(depth):
            if gap + d < length:
                mix = d / depth
                mix_color = color * (1.0 - mix) + color2 * mix
                if inverse:
                    polar = lambda v: (v - 360 if v > 0 else v + 360)
                    polarmix = polar(color[0] - color2[0]) * mix
                    mix_color[0] = (360 + color[0] - polarmix) % 360
                np_color = pygame.Color(0,0,0)
                np_color.hsla = mix_color.astype(int).tolist()
                np_color = np.array(np_color, np.int32)
                if horizontal:
                    surface_array[0][d + gap] = np.sum(np_color << RGBA_FORMULA)
                else:
                    surface_array[d + gap][0] = np.sum(np_color << RGBA_FORMULA)
        gap += depth
    return surface

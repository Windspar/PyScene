import numpy as np
import pygame
from .base import RGBA_FORMULA, pure_colors

def blend_rgb(horizontal, colors, length=255):
    arrays = [np.array(c) for c in pure_colors(colors)]

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
        color = np.copy(arrays[i]).astype(np.float32)
        color2 = np.copy(arrays[i + 1]).astype(np.float32)

        for d in range(depth):
            if gap + d < length:
                mix = d / depth
                np_color = (color * (1.0 - mix) + color2 * mix).astype(np.int32)
                if horizontal:
                    surface_array[0][d + gap] = np.sum(np_color << RGBA_FORMULA)
                else:
                    surface_array[d + gap][0] = np.sum(np_color << RGBA_FORMULA)
        gap += depth
    return surface

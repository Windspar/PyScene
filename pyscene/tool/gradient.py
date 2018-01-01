import pygame
import numpy as np

# RGB_FORMULA = np.array((16, 8, 0))
RGBA_FORMULA = np.array((16, 8, 0, 24))

# source needs to be in alpha
def apply_surface(source, gradient):
    rect = source.get_rect()
    surface = pygame.transform.scale(gradient, rect.size)
    surface = surface.convert_alpha()

    for i in range(rect.size[0]):
        for j in range(rect.size[1]):
            color = source.get_at((i,j))
            gcolor = surface.get_at((i,j))
            gcolor.a = color.a
            surface.set_at((i,j), gcolor)

    return surface

def pure_color(colors):
    result = []
    for color in colors:
        if isinstance(color, (tuple, list)):
            result.append(pygame.Color(*color))
        elif isinstance(color, str):
            result.append(pygame.Color(color))
        elif isinstance(color, np.ndarray):
            color = color.astype(int)
            result.append(pygame.Color(*color.tolist()))
        else:
            result.append(color)
    return result

# inverse is a dummy variable for now
def rgb(horizontal, colors, length=255, inverse=None):
    arrays = [np.array(c) for c in pure_color(colors)]

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

def hsl(horizontal, colors, length=255, inverse=False):
    arrays = [np.array(c.hsla) for c in pure_color(colors)]

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

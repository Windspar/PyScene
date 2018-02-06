import numpy as np
import pygame

def fade(surface, direction):
    keys = {
        'up': lambda v, d: v * d,
        'down': lambda v, d: 1.0 - v * d,
        'left': lambda v, d: v * d,
        'right': lambda v, d: 1.0 - v * d
    }
    value_h = (255 / surface.get_height()) / 255.0
    value_w = (255 / surface.get_width()) / 255.0
    array = pygame.surfarray.pixels_alpha(surface)
    w, h = array.shape
    for y in range(h):
        if direction in ['up', 'down']:
            fading = keys[direction](value_h, y)

        for x in range(w):
            if direction in ['left', 'right']:
                fading = keys[direction](value_w, x)

            array[x][y] = int(array[x][y] * fading)

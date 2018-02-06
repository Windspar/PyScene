import numpy as np
import pygame

RGB_FORMULA = np.array((16, 8, 0))
RGBA_FORMULA = np.array((16, 8, 0, 24))

def pure_color(color):
    if isinstance(color, (tuple, list)):
        return pygame.Color(*color)
    elif isinstance(color, str):
        return pygame.Color(color)
    elif isinstance(color, np.ndarray):
        color = color.astype(int)
        return pygame.Color(*color.tolist())
    return color

def pure_colors(colors):
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

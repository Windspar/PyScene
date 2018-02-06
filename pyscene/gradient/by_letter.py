import numpy as np
import pygame
from .base import pure_colors

def by_letter(font, text, colors, repeat=False):
    colors = pure_colors(colors)
    size = font.size(text)
    surface = pygame.Surface(size)

    last_width = 0
    rect = pygame.Rect(0, 0, 0, size[1])
    for i in range(1, len(text) + 1):
        rect.width = font.size(text[:i])[0] - last_width
        if repeat:
            value = (i - 1) % len(colors)
        else:
            value = min(i - 1, len(colors) - 1)

        surface.fill(colors[value], rect)
        rect.x += rect.width
        last_width += rect.width

    return surface

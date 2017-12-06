import pygame
from tool.point import Vector

# pack colors top to bottom
def horizontal(colors, length=255):
    return create(True, colors, length)

# pack colors left to right
def vertical(colors, length=255):
    return create(False, colors, length)

# colors can be list or tuples of (list, tuple, Vector).
def create(horizontal, colors, length=255):
    vectors = []
    for color in colors:
        if isinstance(color, str):
            vcolor = pygame.Color(color)
            vectors.append(Vector(vcolor.r, vcolor.g, vcolor.b))
        if isinstance(color, (tuple, list)):
            vectors.append(Vector(*color))
        elif isinstance(color, Vector):
            vectors.append(color)

    # balance the length for there an even number
    offset = len(vectors) - 1
    if length % offset != 0:
        length += offset - (length % offset)

    if horizontal:
        surface = pygame.Surface((1, length))
    else:
        surface = pygame.Surface((length, 1))


    depth = int(length / offset)
    gap = 0
    # offset is already 1 less then vectors length.
    # blending color
    for i in range(offset):
        color = vectors[i]
        blend = (color - vectors[i + 1]) / depth

        for d in range(depth):
            if gap + 1 < length:
                if horizontal:
                    surface.set_at((0, d + gap), pygame.Color(*map(int, color.tup())))
                else:
                    surface.set_at((d + gap, 0), pygame.Color(*map(int, color.tup())))
                color -= blend

        gap += depth
    return surface

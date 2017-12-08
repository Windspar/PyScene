import pygame
from tool.point import Vector

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
        if isinstance(color, Vector):
            vectors.append(color.cast())
        else:
            vectors.append(Vector(color).cast())

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
                    surface.set_at((0, d + gap), pygame.Color(*color.tup_cast()))
                else:
                    surface.set_at((d + gap, 0), pygame.Color(*color.tup_cast()))
                color -= blend

        gap += depth
    return surface

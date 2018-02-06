import pygame

def shift(surface, value, direction):
    shifts = value / 45
    size = surface.get_size()
    dtype = {'up': 0, 'down': 1, 'left': 2, 'right': 3, 'top': 0, 'bottom': 1}[direction]
    if dtype < 2:
        extend = int(shifts * size[1] + 0.5 + shifts)
        size = size[0] + extend, size[1]
    else:
        extend = int(shifts * size[0] + 0.5 + shifts)
        size = size[0], size[1] + extend

    surf = pygame.Surface(size)
    surf = surf.convert_alpha()
    surf.fill((0,0,0,0))
    surf_array = pygame.surfarray.pixels2d(surf)
    array = pygame.surfarray.pixels2d(surface)

    w, h = array.shape
    for y in range(h):
        if dtype == 0:
            offset = size[0] - w - shifts * y
        elif dtype == 1:
            offset = shifts * y

        for x in range(w):
            if dtype == 2:
                offset = size[1] - h - shifts * x
            elif dtype == 3:
                offset = shifts * x

            if dtype  < 2:
                surf_array[int(offset) + x][y] = array[x][y]
            else:
                surf_array[x][int(offset) + y] = array[x][y]

    return surf

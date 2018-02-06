import pygame

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

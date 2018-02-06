import pygame

def create_surface(color, size):
    surface = pygame.Surface(size)
    surface = surface.convert_alpha()
    surface.fill(color)
    return surface

class ButtonStyle:
    pass

class TextboxStyle:
    pass

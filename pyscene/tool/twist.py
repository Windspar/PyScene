import pygame
from pyscene.tool import gradient
from pyscene.tool.point import Vector

def color(color):
    if isinstance(color, pygame.Color):
        return color
    elif isinstance(color, str):
        return pygame.Color(color)
    elif isinstance(color[0], Vector):
        return pygame.Color(*color.tup_cast())
    elif isinstance(color, (tuple, list)):
        if isinstance(color[0], (int, float)):
            return pygame.Color(*color)
        elif isinstance(color[0], str):
            if color[0] == 'v':
                return gradient.vertical(color[1:])
            elif color[0] == 'h':
                return gradient.horizontal(color[1:])
            else:
                return gradient.vertical(color)
        elif isinstance(color[0], Vector):
            return gradient.vertical(color)
        else:
            print("Wrong format !", color)
            return pygame.Color('white')
    elif isinstance(color, pygame.Surface):
        return color.convert_alpha()
    else:
        print("Wrong format !", color)
        return pygame.Color('white')

def make_color(color, shade, reverse, allow_dimmer, flow):
    color = Vector(color).cast()
    if allow_dimmer:
        dimmer = (color * 0.20).cast()
        bright = color - dimmer
    else:
        bright = color
    dark = (bright * shade).cast()
    if flow:
        if reverse:
            return bright, dark, dark, bright
        return dark, bright, bright, dark
    else:
        if reverse:
            return dark, bright
        return bright, dark

def make_brightcolor(color, shade, reverse, flow):
    color = Vector(color).cast()
    dimmer = (color * 0.20).cast()
    bright = color
    dark = ((bright - dimmer) * shade).cast()
    dark += (dark * 0.20).cast()
    if flow:
        if reverse:
            return bright, dark, dark, bright
        return dark, bright, bright, dark
    else:
        if reverse:
            return dark, bright
        return bright, dark

def gkey(color, disabled_color, shade=0.5, reverse=False, flow=True):
    if isinstance(color, (str, Vector)):
        bright = make_brightcolor(color, shade, reverse, flow)
        dim = make_color(color, shade, reverse, True, flow)
        dark = make_color(color, shade, not reverse, True, flow)
    else:
        bright = [Vector(c) for c in color]
        dim = [c * shade for c in bright]
        if flow:
            mid = int(len(color) / 2)
            if mid == len(color) / 2:
                dark = dim[:mid][::-1] + dim[mid:][::-1]
            else:
                dark = [dim[mid]] + dim[:mid][::-1] + dim[mid + 1:][::-1] + [dim[mid]]
        else:
            dark = dim[::-1]

    if isinstance(disabled_color, (str, Vector)):
        dcolor = make_color(disabled_color, shade, reverse, False, flow)
    else:
        dcolor = disabled_color

    return bright, dim, dark, dcolor

# expensive operation
def ghost(surface, alpha):
    alpha = alpha / 255.0
    rect = surface.get_rect()
    for x in range(rect.w):
        for y in range(rect.h):
            color = surface.get_at((x,y))
            color.a = int(color.a * alpha)
            surface.set_at((x,y), color)

# expensive operation
# op = 'add','sub','set'
def pixel_alpha(surface, alpha, op='set'):
    rect = surface.get_rect()
    for x in range(rect.w):
        for y in range(rect.h):
            color = surface.get_at((x,y))
            if op == 'set':
                color.a = alpha
            elif op == 'sub':
                color.a -= alpha
                if color.a < 0: color.a = 0
            elif op == 'add':
                color.a += alpha
                if color.a > 255: color.a = 255
            else:
                return surface
            surface.set_at((x,y), color)

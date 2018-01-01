import pygame
from pyscene.tool import gradient
import numpy as np

def colorx(color):
    if isinstance(color, pygame.Color):
        return color
    elif isinstance(color, str):
        return pygame.Color(color)
    elif isinstance(color, np.ndarray):
        return pygame.Color(*color.tolist())
    elif isinstance(color, (tuple, list)):
        if isinstance(color[0], (int, float)):
            return pygame.Color(*color)
        elif isinstance(color[0], str):
            if color[0] == 'v-rgb':
                return gradient.rgb(False, color[1:])
            elif color[0] == 'v-hsl':
                return gradient.hsl(False, color[1:])
            elif color[0] == 'v-hsli':
                return gradient.hsl(False, color[1:], inverse=True)
            elif color[0] == 'h-rgb':
                return gradient.rgb(True, color[1:])
            elif color[0] == 'h-hsl':
                return gradient.hsl(True, color[1:])
            elif color[0] == 'h-hsli':
                return gradient.hsl(True, color[1:], inverse=True)
            else:
                return gradient.hsl(False, color[1:])
        elif isinstance(color[0], np.ndarray):
            return gradient.hsl(Fasle, color)
        else:
            print("Twist.colorx. Wrong format!", color)
            return pygame.Color('white')
    elif isinstance(color, pygame.Surface):
        return color.convert_alpha()
    else:
        print("Twist.colorx. Wrong format !", color)
        return pygame.Color('white')

def make_color(color, shade, reverse, allow_dimmer, flow):
    color = np.array(colorx(color), int)
    if allow_dimmer:
        dimmer = (color * 0.20).astype(int)
        bright = color - dimmer
    else:
        bright = color
    dark = (bright * shade).astype(int)
    if flow:
        if reverse:
            return bright, dark, dark, bright
        return dark, bright, bright, dark
    else:
        if reverse:
            return dark, bright
        return bright, dark

def make_brightcolor(color, shade, reverse, flow):
    color = np.array(colorx(color), int)
    dimmer = (color * 0.20).astype(int)
    bright = color
    dark = ((bright - dimmer) * shade).astype(int)
    dark += (dark * 0.20).astype(int)
    if flow:
        if reverse:
            return bright, dark, dark, bright
        return dark, bright, bright, dark
    else:
        if reverse:
            return dark, bright
        return bright, dark

def gkey(color, disabled_color, shade=0.5, reverse=False, flow=True):
    if isinstance(color, (str, np.ndarray)):
        bright = make_brightcolor(color, shade, reverse, flow)
        dim = make_color(color, shade, reverse, True, flow)
        dark = make_color(color, shade, not reverse, True, flow)
    else:
        bright = [np.array(c) for c in color]
        dim = [c * shade for c in bright]
        if flow:
            mid = int(len(color) / 2)
            if mid == len(color) / 2:
                dark = dim[:mid][::-1] + dim[mid:][::-1]
            else:
                dark = [dim[mid]] + dim[:mid][::-1] + dim[mid + 1:][::-1] + [dim[mid]]
        else:
            dark = dim[::-1]

    if isinstance(disabled_color, (str, np.ndarray)):
        dcolor = make_color(disabled_color, shade, reverse, False, flow)
    else:
        dcolor = disabled_color

    return bright, dim, dark, dcolor

def ghost(surface, alpha):
    alpha = alpha / 255.0
    array = pygame.surfarray.pixels_alpha(surface)
    w, h = array.shape
    for x in range(w):
        for y in range(h):
            array[x][y] = int(array[x][y] * alpha)

def pixel_alpha(surface, alpha, op='set'):
    array = pygame.surfarray.pixels_alpha(surface)
    w, h = array.shape
    for x in range(w):
        for y in range(h):
            if op == 'set':
                array[x][y] = alpha
            elif op == 'sub':
                if array[x][y] - alpha < 0:
                    array[x][y] = 0
                else:
                    array[x][y] = array[x][y] - alpha
            elif op == 'add':
                if array[x][y] + alpha > 255:
                    array[x][y] = 255
                else:
                    array[x][y] = array[x][y] + alpha
            else:
                return

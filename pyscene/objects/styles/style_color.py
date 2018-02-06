import numpy as np
import pygame
from ... import twist

def hsl_to_rgb(color):
    rgb = pygame.Color(0,0,0)
    rgb.hsla = color.tolist()
    return rgb

def style_colors(color, brighten=10):
    color = twist.color(color)
    hsl = np.array(color.hsla)
    if hsl[2] < 101 - brighten:
        # hover, normal
        return (hsl_to_rgb(hsl + np.array((0,0,brighten,0))),
            hsl_to_rgb(hsl))
    else:
        return (hsl_to_rgb(hsl),
            hsl_to_rgb(hsl - np.array((0,0,brighten,0))))

def saturation_tone(color, offset):
    color = twist.color(color)
    hsl = np.array(color.hsla)
    if offset < 0:
        if hsl[1] > offset:
            return hsl_to_rgb(hsl + np.array((0,offset,0,0)))
        else:
            hsl[1] = 0
            return hsl_to_rgb(hsl)

    elif offset > 0:
        if hsl[1] < 101 - offset:
            return hsl_to_rgb(hsl + np.array((0,offset,0,0)))
        else:
            hsl[1] = 100
            return hsl_to_rgb(hsl)

def lightness_tone(color, offset):
    color = twist.color(color)
    hsl = np.array(color.hsla)
    if offset < 0:
        if hsl[2] > offset:
            return hsl_to_rgb(hsl + np.array((0,0,offset,0)))
        else:
            hsl[2] = 0
            return hsl_to_rgb(hsl)

    elif offset > 0:
        if hsl[2] < 101 - offset:
            return hsl_to_rgb(hsl + np.array((0,0,offset,0)))
        else:
            hsl[2] = 100
            return hsl_to_rgb(hsl)

def color_tones(color, offset):
    # return (bright, normal, dark)
    return (
        lightness_tone(color, offset),
        color,
        lightness_tone(color, -offset)
    )

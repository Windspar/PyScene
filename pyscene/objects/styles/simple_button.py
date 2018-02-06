import pygame
import numpy as np
from .base import create_surface, ButtonStyle
from .style_color import style_colors
from ..objects import PySceneImage
from ... import gradient
from ... import twist

class SimpleButtonStyle(ButtonStyle):
    def __init__(self, color, disabled_color, gradient_args=[False, 2, 10, 10, True]):
        self.disabled_color = twist.color(disabled_color)
        self.gradient_args = gradient_args
        self.color = twist.color(color)

    def get_image(self, rect):
        self.rect = rect
        return self.build_simple().scale(rect.size)

    def build_simple(self):
        hover, normal = style_colors(self.color)
        dhover, dnormal = style_colors(self.disabled_color)

        return PySceneImage(
            self.flow(normal),
            self.flow(hover),
            self.flow(normal, True),
            self.flow(dnormal)
        )


    def flow(self, color, reverse=False):
        args = self.gradient_args[:]
        args.insert(2, color)
        image = gradient.hsl_by_value(*args)
        w, h = image.get_size()

        if w > 1:
            over = (w, 0)
            flips = True, False
            w *= 2
        else:
            over = (0, h)
            flips = False, True
            h *= 2

        image_surface = create_surface((0,0,0,0), (w,h))
        if reverse:
            image_surface.blit(image, (0,0))
            flip_image = pygame.transform.flip(image, *flips)
            image_surface.blit(flip_image, over)
        else:
            image_surface.blit(image, over)
            flip_image = pygame.transform.flip(image, *flips)
            image_surface.blit(flip_image, (0,0))

        return image_surface

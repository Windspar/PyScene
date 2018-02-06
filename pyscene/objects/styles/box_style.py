import pygame
import numpy as np
from ... import twist
from ..objects import PySceneImage
from .base import create_surface, ButtonStyle, TextboxStyle
from .style_color import color_tones

class BoxStyle(ButtonStyle, TextboxStyle):
    def __init__(self, color, disabled_color, intensity=20):
        self.color = twist.color(color)
        self.disabled_color = twist.color(disabled_color)
        self.intensity = intensity

    def get_image(self, rect):
        self.size = rect.size
        self.rect = rect.copy()
        self.rect.topleft = 0,0
        self.rect.inflate_ip(-2, -2)
        return self.build_simple()

    def build_simple(self):
        def create_image(fg, bg):
            image = create_surface((0,0,0,0), self.size)
            pygame.draw.rect(image, fg, self.rect, 3)
            pygame.draw.rect(image, bg, self.rect, 1)
            return image

        bright, normal, dark = map(twist.color, color_tones(self.color, self.intensity))
        dbright, dnormal, ddark = map(twist.color, color_tones(self.disabled_color, self.intensity))

        return PySceneImage(
            create_image(normal, dark),
            create_image(bright, dark),
            create_image(dark, normal),
            create_image(dnormal, ddark),
        )

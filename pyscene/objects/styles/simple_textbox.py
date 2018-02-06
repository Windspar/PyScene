import pygame
import numpy as np
from .base import create_surface, TextboxStyle
from .style_color import style_colors
from ..objects import PySceneImage
from ...gradient import hsl_by_value
from ... import gradient
from ... import twist

class SimpleTextboxStyle(TextboxStyle):
    def __init__(self, color, disabled_color, thickness=4, intensity=10):
        self.disabled_color = disabled_color
        self.thickness = thickness * 2
        self.intensity = intensity
        self.color = color

    def get_image(self, rect):
        self.rect = rect
        self.overlay_size = rect.inflate(-self.thickness, -self.thickness).size
        return self.build_simple()

    def build_simple(self):
        hover, normal = style_colors(self.color)
        dhover, dnormal = style_colors(self.disabled_color)

        return PySceneImage(
            self.overlay_simple(normal),
            self.overlay_simple(hover),
            self.overlay_simple(normal, True),
            self.overlay_simple(dnormal)
        )

    def overlay_simple(self, color, reverse=False):
        image = gradient.hsl_by_value(True, 2, color, self.intensity, self.intensity, reverse)
        image = pygame.transform.scale(image, self.rect.size)
        overlay = gradient.hsl_by_value(True, 2, color, self.intensity, self.intensity, not reverse)
        overlay = pygame.transform.scale(overlay, self.overlay_size)
        thickness = self.thickness * 0.5
        image.blit(overlay, (thickness, thickness))
        return image

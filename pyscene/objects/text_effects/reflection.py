import pygame
import numpy as np
from .base import BaseEffect
from ... import twist

class Reflection(BaseEffect):
    def __init__(self, parent, distance, fades, shifts, color):
        BaseEffect.__init__(self, parent, color, None)
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.parent._rect.copy()
        self.rect.y += self.rect.h + distance

        if fades:
            twist.fade(self.image, fades)

        if shifts:
            self.image = twist.shift(self.image, *shifts)

    def blit(self, surface, clip_rect=None):
        if self.rotation_image:
            self.build_rotation_image(clip_rect)
            surface.blit(self.image, self.rotation_rect, clip_rect)
        else:
            surface.blit(self.image, self.rect, clip_rect)

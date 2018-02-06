import pygame
from .base import BaseEffect
from ...arrays.point import Point

class Shadow(BaseEffect):
    def __init__(self, parent, color, offset_point, trail=False, step=1, alpha=None):
        self.offset = Point(offset_point)
        self.trail = trail
        self.step = step
        BaseEffect.__init__(self, parent, color, alpha)
        self.position = (Point(self.parent._rect.topleft) - self.offset).tup()

    def render(self, allow_effects=True):
        BaseEffect.render(self, allow_effects)
        if self.trail:
            w, h = Point(self.parent._rect.size) + self.offset
            surface = pygame.Surface((w, h))
            surface = surface.convert_alpha()
            surface.fill((0,0,0,0))

            value = max(self.offset.tup())
            x_move = self.offset.x / value
            y_move = self.offset.y / value
            x, y = self.offset
            for m in range(0, value, self.step):
                surface.blit(self.image, (int(x), int(y)))
                x = self.offset.x - x_move * m
                y = self.offset.y - y_move * m

            self.image = surface

    def blit(self, surface, clip_rect=None):
        if self.rotation_image:
            self.build_rotation_image(clip_rect)
            surface.blit(self.rotation_image, self.position, clip_rect)
        else:
            surface.blit(self.image, self.position, clip_rect)

import pygame
from ..arrays import Point

class Grid:
    def __init__(self, rect, chop, gap=Point(0,0)):
        if isinstance(rect, pygame.Rect):
            self._rect = rect
        else:
            self._rect = pygame.Rect(rect)

        self.gap = Point(gap)
        self.chop = Point(chop)
        self.size = Point(self._rect.size) / Point(chop)

    def get_size(self):
        return (Point(self._rect.size) - self.gap * self.chop * 2).tup()

    def position_offset(self, x, y, offx=0, offy=0):
        return (self._rect.x + self.size.x * x + offx,
                self._rect.y + self.size.y * y + offy)

    def position(self, x, y):
        return (self._rect.x + self.size.x * x,
                self._rect.y + self.size.y * y)

    def align(self, x, y, w=1, h=1, pad=(0,0)):
        pad = Point(pad)
        w = self.size.x * w - self.gap.x * 2
        h = self.size.y * h - self.gap.y * 2

        return pygame.Rect(
            self._rect.x + self.size.x * x + self.gap.x + pad.x,
            self._rect.y + self.size.y * y + self.gap.y + pad.y,
            w - pad.x * 2, h - pad.y * 2
            )

    def rect(self, x, y, pad=(0,0)):
        pad = Point(pad)
        return pygame.Rect(
            self._rect.x + self.size.x * x + self.gap.x + pad.x,
            self._rect.y + self.size.y * y + self.gap.y + pad.y,
            self.size.x - self.gap.x * 2 - pad.x * 2,
            self.size.y - self.gap.y * 2 - pad.y * 2
        )

    def location(self, x, y):
        p = Point (
            int((x - self._rect.x) / (self._rect.w / self.chop.x)),
            int((y - self._rect.y) / (self._rect.h / self.chop.y)))

        if self.rect(p.x, p.y).collidepoint(x, y):
            return p.tup(int)
        return None, None

    def location_close(self, x, y):
        return (int((x - self._rect.x) / (self._rect.w / self.chop.x)),
                int((y - self._rect.y) / (self._rect.h / self.chop.y)))

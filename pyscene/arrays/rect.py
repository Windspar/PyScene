from pygame import Rect as GameRect
from . import properties as prop
from .dimension import Dimension
from .point import Point
import numpy as np

class Rect(np.ndarray):
    def __new__(cls, x, y, w, h):
        return np.asarray((x, y, w, h)).view(cls)

    @classmethod
    def by_dimension(cls, dim):
        return Rect(0, 0, dim.w, dim.h)

    @classmethod
    def by_size(cls, w, h):
        return Rect(0, 0, w, h)

    def clamp(self, rect, in_place=False):
        clamp_x, clamp_y = self[:2]

        if self[2] >= rect[2]:
            clamp_x = rect[0] + rect[2] / 2 - self[2] / 2
        elif self[0] < rect[0]:
            clamp_x = rect[0]
        elif self[0] + self[2]:
            clamp_x = rect[0] + rect[2] - self[2]

        if self[3] >= rect[3]:
            clamp_y = rect[1] + rect[3] / 2 - self[3] / 2
        elif self[1] < rect[1]:
            clamp_y = rect[1]
        elif self[1] + self[3]:
            clamp_y = rect[1] + rect[3] - self[3]

        if in_place:
            self[0] = clamp_x
            self[1] = clamp_y
        else:
            return Rect(clamp_x, clamp_y, self[2], self[3])

    def clamp_ip(self, rect):
        self.clamp(rect, True)

    def collidepoint(self, x, y):
        return self[0] < x < self[0] + self[2] and self[1] < y < self[1] + self[3]

    def colliderect(self, rect):
        return (((self[0] > rect[0] and self[0] < rect[2] + rect[0]) or
                (rect[0] > self[0] and rect[0] < self[2] + self[0])) and
                ((self[1] > rect[1] and self[1] < rect[3] + rect[1]) or
                (rect[1] > self[1] and rect[1] < self[3] + self[1])))

    def copy(self):
        return Rect(*self[:4])

    def inflate(self, x, y):
        rect = self.copy()
        if x != 0:
            rect.x -= (x - np.fmod(x, 2)) / 2
            rect.w += x

        if y != 0:
            rect.y -= (y - np.fmod(y, 2)) / 2
            rect.h += y

        return rect

    def inflate_ip(self, x, y):
        if x != 0:
            self[0] -= (x - np.fmod(x, 2)) / 2
            self[2] += x

        if y != 0:
            self[1] -= (y - np.fmod(y, 2)) / 2
            self[3] += y

    def move(self, x, y):
        return Rect(self[0] + x, self[1] + y, self[2], self[3])

    def move_ip(self, x, y):
        self[0] += x
        self[1] += y

    def normalize(self):
        one = lambda v: [0, np.absolute(v) - 1][v < 0]
        abso = lambda v: [v, np.absolute(v) - 1][v < 0]
        self[0] -= one(self[2])
        self[1] -= one(self[3])
        self[2] = abso(self[2])
        self[3] = abso(self[3])

    def tup(self, cast=None):
        if cast:
            data = self.astype(cast)
            return tuple(data.tolist())
        return tuple(self.tolist())

    @property
    def pygame_rect(self):
        return GameRect(*(self.copy() + .5).astype(int))

    x = prop.ArrayProperty(0)
    y = prop.ArrayProperty(1)
    w = prop.ArrayProperty(2)
    h = prop.ArrayProperty(3)
    left = prop.ArrayProperty(0)
    top = prop.ArrayProperty(1)
    width = prop.ArrayProperty(2)
    height = prop.ArrayProperty(3)
    dimension = prop.ArrayDoubleProperty(2, 3, Dimension)
    topleft = prop.ArrayDoubleProperty(0, 1, Point)
    topright = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineProperty(0, 2),
        prop.ArrayProperty(1),
        Point)

    bottomleft = prop.ArrayTypeDoubleProperty(
        prop.ArrayProperty(0),
        prop.ArrayCombineProperty(1, 3),
        Point)

    bottomright = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineProperty(0, 2),
        prop.ArrayCombineProperty(1, 3),
        Point)

    center = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineCenterProperty(0,2),
        prop.ArrayCombineCenterProperty(1,3),
        Point)

    centerx = prop.ArrayCombineCenterProperty(0,2)
    centery = prop.ArrayCombineCenterProperty(1,3)

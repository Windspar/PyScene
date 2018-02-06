from pygame import Rect as GameRect
from . import properties as prop
import numpy as np

class Rect(np.ndarray):
    def __new__(cls, x, y, w, h):
        return np.asarray((x, y, w, h)).view(cls)

    def clamp(self, rect):
        pass

    def clamp_ip(self, rect):
        pass

    def collidepoint(self, x, y):
        pass

    def colliderect(self, rect):
        pass

    def move(self, x, y):
        return Rect(self.x + x, self.y + y, w, h)

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
            self.astype(cast)
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
    #size = prop.ArrayDoubleProperty(2,3)
    topleft = prop.ArrayDoubleProperty(0,1)
    topright = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineProperty(0, 2),
        prop.ArrayProperty(1))

    bottomleft = prop.ArrayTypeDoubleProperty(
        prop.ArrayProperty(0),
        prop.ArrayCombineProperty(1, 3))

    bottomright = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineProperty(0, 2),
        prop.ArrayCombineProperty(1, 3))

    center = prop.ArrayTypeDoubleProperty(
        prop.ArrayCombineCenterProperty(0,2),
        prop.ArrayCombineCenterProperty(1,3))

    centerx = prop.ArrayCombineCenterProperty(0,2)
    centery = prop.ArrayCombineCenterProperty(1,3)

if __name__ == '__main__':
    r = Rect(50, 50, 50, 50)
    print(r, r.center)

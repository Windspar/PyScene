from .properties import ArrayProperty
import numpy as np

class Vector(np.ndarray):
    def __new__(cls, x, y=None, z=None):
        if y is None:
            obj = np.asarray(x).view(cls)
        else:
            obj = np.asarray((x, y, z)).view(cls)
        return obj

    def tup(self, cast=None):
        if cast:
            self.astype(cast)
        return tuple(self.tolist())

    x = ArrayProperty(0)
    y = ArrayProperty(1)
    z = ArrayProperty(2)

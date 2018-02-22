from .properties import ArrayProperty
import numpy as np

class Dimension(np.ndarray):
    def __new__(cls, x, y=None):
        if y is None:
            obj = np.asarray(x).view(cls)
        else:
            obj = np.asarray((x, y)).view(cls)
        return obj

    def tup(self, cast=None):
        if cast:
            self.astype(cast)
        return tuple(self.tolist())

    w = ArrayProperty(0)
    h = ArrayProperty(1)
    width = ArrayProperty(0)
    height = ArrayProperty(1)

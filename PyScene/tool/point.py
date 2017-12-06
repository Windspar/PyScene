import operator
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def tup(self):
        return int(self.x), int(self.y)

    # overload handle Vector, Point, tuple, list, single number
    def overload(self, op, point):
        if isinstance(point, (Point, Vector)):
            return Point(op(self.x, point.x), op(self.y, point.y))
        elif isinstance(point, (tuple, list)):
            return Point(op(self.x, point[0]), op(self.y, point[1]))
        return Point(op(self.x, point), op(self.y, point))

    def __add__(self, point):
        return self.overload(operator.add, point)

    def __sub__(self, point):
        return self.overload(operator.sub, point)

    def __mul__(self, point):
        return self.overload(operator.mul, point)

    def __truediv__(self, point):
        return self.overload(operator.truediv, point)

    def __repr__(self):
        return "Point({0}, {1}))".format(self.x, self.y)

def direction(angle):
    degree = math.radians(angle)
    return Point(math.cos(degree), math.sin(degree))

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def tup(self):
        return self.x, self.y, self.z

    # overload handle Vector, Point, tuple, list, single number
    def overload(self, op, vector):
        if isinstance(vector, Vector):
            return Vector(op(self.x, vector.x), op(self.y, vector.y), op(self.z, vector.z))
        elif isinstance(vector, Point):
            return Vector(op(self.x, vector.x), op(self.y, vector.y), self.z)
        elif isinstance(vector, (tuple, list)):
            if len(vector) == 2:
                return Vector(op(self.x, vector[0]), op(self.y, vector[1]), self.z)
            return Vector(op(self.x, vector[0]), op(self.y, vector[1]), op(self.z, vector[2]))
        return Vector(op(self.x, vector), op(self.y, vector), op(self.z, vector))

    def __add__(self, vector):
        return self.overload(operator.add, vector)

    def __sub__(self, vector):
        return self.overload(operator.sub, vector)

    def __mul__(self, vector):
        return self.overload(operator.mul, vector)

    def __truediv__(self, vector):
        return self.overload(operator.truediv, vector)

    def __repr__(self):
        return "Vector({0}, {1}, {2})".format(self.x, self.y, self.z)

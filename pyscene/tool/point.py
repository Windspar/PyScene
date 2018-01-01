import numpy as np
import math

class ArrayProperty:
	def __init__(self, position):
		self.position = position

	def __get__(self, instance, owner):
		return instance[self.position]

	def __set__(self, instance, value):
		instance[self.position] = value

class Point(np.ndarray):
	def __new__(cls, x, y=None):
		if y is None:
			obj = np.asarray(x).view(cls)
		else:
			obj = np.asarray((x, y)).view(cls)
		return obj

	def tup(self, cast=int):
		self.astype(cast)
		return tuple(self.tolist())

	x = ArrayProperty(0)
	y = ArrayProperty(1)

class Vector(np.ndarray):
	def __new__(cls, x, y=None, z=None):
		if y is None:
			obj = np.asarray(x).view(cls)
		else:
			obj = np.asarray((x, y, z)).view(cls)
		return obj

	def tup(self, cast=int):
		self.astype(cast)
		return tuple(self.tolist())

	x = ArrayProperty(0)
	y = ArrayProperty(1)
	z = ArrayProperty(2)

class RGBA(np.ndarray):
	def __new__(cls, r, g=None, b=None, a=255):
		if g is None:
			if len(r) == 3:
				r = (*r, a)
			obj = np.asarray(r).view(cls)
		else:
			obj = np.asarray((r, g, b, a)).view(cls)
		return obj

	def tup(self, cast=int):
		self.astype(cast)
		return tuple(self.tolist())

	r = ArrayProperty(0)
	g = ArrayProperty(1)
	b = ArrayProperty(2)
	a = ArrayProperty(3)

class HSLA(np.ndarray):
	def __new__(cls, h, s=None, l=None, a=255):
		if s is None:
			if len(h) == 3:
				h = (*h, a)
			obj = np.asarray(h).view(cls)
		else:
			obj = np.asarray((h, s, l, a)).view(cls)
		return obj

	def tup(self, cast=int):
		self.astype(cast)
		return tuple(self.tolist())

	h = ArrayProperty(0)
	s = ArrayProperty(1)
	l = ArrayProperty(2)
	a = ArrayProperty(3)

class HSVA(np.ndarray):
	def __new__(cls, h, s=None, v=None, a=255):
		if s is None:
			if len(h) == 3:
				h = (*h, a)
			obj = np.asarray(h).view(cls)
		else:
			obj = np.asarray((h, s, v, a)).view(cls)
		return obj

	def tup(self, cast=int):
		self.astype(cast)
		return tuple(self.tolist())

	h = ArrayProperty(0)
	s = ArrayProperty(1)
	v = ArrayProperty(2)
	a = ArrayProperty(3)

def direction(angle):
	degree = math.radians(angle)
	return Point(math.cos(degree), math.sin(degree))

import math

class Vector(object):
    def __init__(self, x, y):
        self._tuple = (x, y)

    @property
    def x(self):
        return self._tuple[0]

    @property
    def y(self):
        return self._tuple[1]

    def __getitem__(self, index):
        return self._tuple[index]

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        try:
            return Vector(self.x * other.x, self.y * other.y)
        except:
            return Vector(self.x * other, self.y * other)

    def __div__(self, other):
        try:
            return Vector(self.x / other.x, self.y / other.y)
        except:
            return Vector(self.x / other, self.y / other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def length(self):
        return self.squared_length() ** 0.5

    def squared_length(self):
        return self.x ** 2 + self.y ** 2

    def unit(self):
        return self / self.length()

    def turn_left(self):
        return Vector(-self.y, self.x)

    def turn_right(self):
        return Vector(self.y, -self.x)

    def rotate(self, angle):
        return Vector(self.x * math.cos(angle) - self.y * math.sin(angle),
            self.x * math.sin(angle) + self.y * math.cos(angle))

    def angle(self):
        return math.atan2(self.y, self.x)


VECTOR_NULL = Vector(0, 0)
VECTOR_NORTH = Vector(0, 1)
VECTOR_EAST = Vector(1, 0)
VECTOR_SOUTH = Vector(0, -1)
VECTOR_WEST = Vector(-1, 0)

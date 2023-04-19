import math


class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.__x: float = x
        self.__y: float = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def position(self):
        return [self.x, self.y]

    @property
    def sqr_magnitude(self):
        return self.x ** 2 + self.y ** 2

    @property
    def magnitude(self):
        return math.sqrt(self.sqr_magnitude)

    @property
    def normalized(self):
        if self.magnitude != 0:
            return Vector2(self.x / self.magnitude, self.y / self.magnitude)
        else:
            return Vector2(0, 0)

    def __str__(self):
        return f"[{self.x},{self.y}]"

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.x * other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.x / other)

    @classmethod
    def zero(cls):
        return Vector2(0, 0)

    @classmethod
    def one(cls):
        return Vector2(1, 1)

    @classmethod
    def up(cls):
        return Vector2(0, 1)

    @classmethod
    def down(cls):
        return Vector2(0, -1)

    @classmethod
    def left(cls):
        return Vector2(-1, 0)

    @classmethod
    def right(cls):
        return Vector2(1, 0)
